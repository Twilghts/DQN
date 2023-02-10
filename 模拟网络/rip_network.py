import networkx as nx

from net import Net


class Rip(Net):
    def __init__(self):
        super().__init__()
        for u, v in self.G.edges:
            self.G[u][v]['weight']: float = 1
        """构建每一个路由器的路由表"""
        for _router in self.routers.values():
            _router.routing_table = {
                node: nx.dijkstra_path(self.G, _router.sign, node) for node in self.G.nodes
            }
