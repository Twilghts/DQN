import copy

from net import Net


class Ospf(Net):
    def __init__(self):
        super().__init__()
        self.dynamic_graph = copy.deepcopy(self.G)  # 创建一个副本图，用于体现Ospf的动态性。

    """在传输信息的同时对网络进行动态更新"""
    def update_graph(self):
        """对每一个路由器进行访问，如果它的可用数据量小于一半，就对图中的边相应的权值进行修改，如果它的可用数据量正常，则将边的权值恢复成原图的权值"""
        modificate_edges = {}  # 统计所有被修改过的边。
        for router in self.routers.values():
            """可用数据量不够，进行修改。"""
            if router.get_receive_size() < router.datasize * 0.2:
                """获取直接与该节点相接的链路。"""
                edges: set = {(u, v) for u, v in self.dynamic_graph.edges if u == router.sign or v == router.sign}
                """修改每一条链路的权值。edge为元组"""
                for edge in edges:
                    self.dynamic_graph[edge[0]][edge[1]]['weight'] = 100
                modificate_edges |= edges  # 两个集合做并集。不会有重复元素。
        """获取所有未经修改的边。"""
        dismodificate_edges: set = {(u, v) for u, v in self.dynamic_graph.edges if (u, v) not in modificate_edges}
        """将未修改的边的权值恢复"""
        for u, v in dismodificate_edges:
            self.dynamic_graph[u][v]['weight'] = self.G[u][v]['weight']

    """每次结束一整次传输信息时，对图进行全局复原。"""
    def retry_graph(self):
        self.dynamic_graph = copy.deepcopy(self.G)