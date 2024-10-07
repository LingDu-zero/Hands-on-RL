import networkx as nx
from clock_tree import *
import geo
import numpy as np
import random
from copy import deepcopy

def steiner_tree(drive_node):
    G = nx.Graph()
    G.add_node(drive_node)
    for node in drive_node.drive_connections:
        G.add_node(node)
        G.add_edge(drive_node, node)
    steiner_tree = nx.algorithms.approximation.steiner_tree(G, G.nodes)
    return steiner_tree

class RCUtil:
    def __init__(self) -> None:
        pass

    @staticmethod
    def calculate_wire_cost(points) -> float:
        steiner_weight = geo.get_steiner_weight(len(points))
        hpwl = geo.get_hpwl(np.array(points))
        return steiner_weight * hpwl * 0.3
    
    @staticmethod
    def calculate_delay_cost(node) -> float:
        """
        计算给定节点的延迟成本。

        参数：
            node：要计算延迟成本的节点。

        返回值：
            float：计算出的延迟成本。

        说明：
            该函数首先检查节点是否为根节点。如果是根节点，则延迟成本为0。
            否则，它获取节点的父节点的所有子节点，并计算这些子节点的Steiner权重和HPWL（Half-Perimeter Wirelength）。
            然后，它计算等效线长（eqwl）和点对点线长（p2pwl），并使用这些值来计算延迟成本。
            延迟成本的计算公式为：sqrt(eqwl * p2pwl) * 1.0。
        """
        if node.is_root():
            return 0
        nodes = node.parent.children
        steiner_weight = geo.get_steiner_weight(len(nodes)+1)
        points = []
        for node in nodes:
            points.append([node.x, node.y])
        points.append([node.parent.x, node.parent.y])
        hpwl = geo.get_hpwl(np.array(points))
        eqwl = steiner_weight * hpwl
        p2pwl = geo.get_hpwl(np.array([[node.x, node.y], [node.parent.x, node.parent.y]]))
        return eqwl * p2pwl * 0.002


if __name__ == "__main__":
    random.seed(42)
    root_node = ClockNode(0, 0, None)
    tree = ClockTree(5, root_node)
    

    while True:
        node = random.sample(tree.nodes, 1)[0]
        if not node.is_root():
            break
    
    delay_cost = RCUtil.calculate_delay_cost(node)
    print(node.x, node.y)
    print(delay_cost)