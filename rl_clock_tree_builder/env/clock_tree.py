import random
import matplotlib.pyplot as plt
import lib

class ClockNode:
    def __init__(self, x, y, lib, root=False):
        self.x = x
        self.y = y
        self.lib = lib
        self.isroot = root
        self.parent = None
        self.children = []
    
    def add_node(self, node):
        self.children.append(node)
        node.parent = self

    def remove_node(self, node):
        self.children.remove(node)
        node.parent = None

    def is_root(self):
        return self.isroot

    def is_leaf(self):
        return len(self.children) == 0

class ClockTree:
    def __init__(self, num_nodes, root_node):
        self.nodes = [root_node]
        self.root = root_node
        for _ in range(num_nodes):
            x, y = random.uniform(0, 100), random.uniform(0, 100)
            self.nodes.append(ClockNode(x, y, lib.Reg()))
        self.initial_nodes()

    def initial_nodes(self):
        for node in self.nodes:
            if node != self.root:
                self.root.add_node(node)

    # clock tree costs
    def get_skew(self):
        pass

    def get_max_latency(self):
        pass

    def get_min_latency(self):
        pass

    def get_wire_length(self):
        pass

    def get_power(self):
        pass

    def get_max_fout(self):
        pass

    def plot_tree(self):
        plt.figure(figsize=(100, 100))
        for node in self.nodes:
            plt.scatter(node.x, node.y, color='blue')
            for conn in node.children:
                plt.plot([node.x, conn.x], [node.y, conn.y], color='gray')
        plt.scatter(self.root.x, self.root.y, color='red', marker='*', s=200)
        plt.show()

if __name__ == "__main__":
    # 创建一个包含100个节点的时钟树，并指定一个根节点
    root_node = ClockNode(0, 0, None, True)
    tree = ClockTree(100, root_node)

    # 绘制时钟树分布图，并标记根节点
    tree.plot_tree()
