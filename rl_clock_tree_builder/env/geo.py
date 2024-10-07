# geometry utilities

import math
import numpy as np
import matplotlib.pyplot as plt

def get_phase(x):
    return 1 if x > 0 else (-1 if x < 0 else 0)

def get_steiner_weight(n_points):
    if n_points <= 2:
        return 1.0
    return 3.0 - (2.0 * np.exp(0.025 * (3.0 - n_points)))

def get_hpwl(points):
    min_x = points[:, 0].min()
    max_x = points[:, 0].max()
    min_y = points[:, 1].min()
    max_y = points[:, 1].max()
    return max_x - min_x + max_y - min_y

class Rect():
    def __init__(self, min_x, max_x, min_y, max_y):
        self.min_x = min_x
        self.max_x = max_x
        self.min_y = min_y
        self.max_y = max_y

    def __str__(self):
        return (
            "Rectangle("
            + str(self.min_x)
            + ", "
            + str(self.max_x)
            + ", "
            + str(self.min_y)
            + ", "
            + str(self.max_y)
            + ")"
        )

    def fix(self):
        if self.min_x > self.max_x:
            self.min_x, self.max_x = self.max_x, self.min_x
        if self.min_y > self.max_y:
            self.min_y, self.max_y = self.max_y, self.min_y

    def contains(self, point):
        return (
            self.min_x <= point[0] <= self.max_x
            and self.min_y <= point[1] <= self.max_y
        )

    def intersects(self, other):
        return not (
            self.min_x > other.max_x
            or self.max_x < other.min_x
            or self.min_y > other.max_y
            or self.max_y < other.min_y
        )

    def expand(self, other):
        self.min_x = min(self.min_x, other.min_x)
        self.max_x = max(self.max_x, other.max_x)
        self.min_y = min(self.min_y, other.min_y)
        self.max_y = max(self.max_y, other.max_y)

    def expandPoint(self, point):
        self.min_x = min(self.min_x, point[0])
        self.max_x = max(self.max_x, point[0])
        self.min_y = min(self.min_y, point[1])
        self.max_y = max(self.max_y, point[1])

    
    def expand_to_point_with_target_hpwl(self, point, target_hpwl):
        # expand the rect to include the point, but keep the hpwl the same
        # the point is assumed to be outside the rect
        if self.contains(point) or self.getHpwl() >= target_hpwl:
            return
        corners = [
            [self.min_x, self.min_y],
            [self.min_x, self.max_y],
            [self.max_x, self.min_y],
            [self.max_x, self.max_y],
        ]
        farthest_corner = max(corners, key=lambda c: geo.l2Distance(c, point))
        target_expand_point = geo.l2Split(farthest_corner, point, target_hpwl - self.getHpwl())
        self.expandPoint(target_expand_point)


    def getCenter(self):
        return [(self.min_x + self.max_x) / 2, (self.min_y + self.max_y) / 2]

    def getHpwl(self):
        return self.max_x - self.min_x + self.max_y - self.min_y

    def width(self):
        return self.max_x - self.min_x

    def height(self):
        return self.max_y - self.min_y

    def boundPoint(self, point):
        if self.contains(point):
            return point
        x = point[0]
        y = point[1]
        if x < self.min_x:
            x = self.min_x
        elif x > self.max_x:
            x = self.max_x
        if y < self.min_y:
            y = self.min_y
        elif y > self.max_y:
            y = self.max_y
        return [x, y]
    
    def closestBalancePoint(self, point):
        x = point[0]
        y = point[1]
        if self.width() > self.height():
            x = self.getCenter()[0]
        else:
            y = self.getCenter()[1]
        return self.boundPoint([x, y])

class geo():
    def __init__(self):
        pass

    def l1Distance(a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])
    
    def l2Distance(a, b):
        return math.sqrt((a[0] - b[0])**2 + (a[1] - b[1])**2)
    
    def linfDistance(a, b):
        return max(abs(a[0] - b[0]), abs(a[1] - b[1]))

    def getPointsBBox(points):
        min_x = points[:, 0].min()
        max_x = points[:, 0].max()
        min_y = points[:, 1].min()
        max_y = points[:, 1].max()
        return Rect(min_x, max_x, min_y, max_y)
    
    def l2Split(a, b, m):
        # a, b: two points
        # m: the dist from a to split point
        ab = [b[0] - a[0], b[1] - a[1]]
        ab_len = math.sqrt(ab[0]**2 + ab[1]**2)
        return [a[0] + ab[0] * m / ab_len, a[1] + ab[1] * m / ab_len]


    def l1Split(a, b, m, direction):
        # a, b: two points
        # m: the dist from a to split point
        # direction: 0 for horizontal, 1 for vertical
        dxdy = [0, 0]
        ab = [b[0] - a[0], b[1] - a[1]]
        abp = [get_phase(ab[0]), get_phase(ab[1])]
        dxdy[direction] = ab[direction] if m > abs(ab[direction]) else m * abp[direction]
        m -= abs(ab[direction])
        dxdy[1 - direction] = m * abp[1 - direction] if m > 0 else 0
        return [a[0] + dxdy[0], a[1] + dxdy[1]]


    def l1SplitRatio(a, b, ratio, direction):
        # a, b: two points
        # ratio: the ratio of the dist from a to split point to the dist from a to b
        # direction: 0 for horizontal, 1 for vertical
        m = ratio * (abs(b[0] - a[0]) + abs(b[1] - a[1]))
        return geo.l1Split(a, b, m, direction)

    def borderRect(a:Rect, b:Rect)->Rect:
        rv = Rect(
            max(a.min_x, b.min_x),
            min(a.max_x, b.max_x),
            max(a.min_y, b.min_y),
            min(a.max_y, b.max_y)
        )
        rv.fix()
        return rv
    
    def plot_city_block(ax, a, b, color, linewidth=1):
        hv = abs(a[0] - b[0]) < abs(a[1] - b[1])
        if not hv:
            ax.plot([a[0], b[0], b[0]], [a[1], a[1], b[1]], color, linewidth=linewidth)
        else:
            ax.plot([a[0], a[0], b[0]], [a[1], b[1], b[1]], color, linewidth=linewidth)
    
    def plot_rect(ax, rect, color, linewidth=1):
        ax.plot([rect.min_x, rect.max_x, rect.max_x, rect.min_x, rect.min_x], [rect.min_y, rect.min_y, rect.max_y, rect.max_y, rect.min_y], color, linewidth=linewidth)
    
    def plot_star(ax, center, points, color, linewidth=1):
        for point in points:
            ax.plot([center[0], point[0]], [center[1], point[1]], color, linewidth=linewidth)