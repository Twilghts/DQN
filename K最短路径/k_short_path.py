import networkx as nx


def get_paths_and_length(start, end):
    # 构造图
    G = nx.Graph()
    G.add_weighted_edges_from([(0, 1, 4), (0, 2, 4.5), (1, 2, 4.2), (1, 3, 2.5), (2, 5, 2.0),
                               (3, 4, 7.0), (4, 5, 2.5), (5, 7, 1.5), (4, 8, 3.0), (7, 8, 2.0),
                               (6, 7, 0.5), (6, 10, 2.0), (8, 9, 1.5), (9, 10, 0.5)])
    paths_dict = {}
    # 生成每对节点之间3条不同的路径(if exist)
    for i, path in enumerate(nx.all_simple_paths(G, start, end, cutoff=3)):
        length = nx.shortest_path_length(G, start, end, weight='weight')
        paths_dict[tuple(path)] = length

    return paths_dict


print(get_paths_and_length(0, 8))

# # 构造图
# G = nx.Graph()
# G.add_weighted_edges_from([(0, 1, 4), (0, 2, 4.5), (1, 2, 4.2), (1, 3, 2.5), (2, 5, 2.0),
#                            (3, 4, 7.0), (4, 5, 2.5), (5, 7, 1.5), (4, 8, 3.0), (7, 8, 2.0),
#                            (6, 7, 0.5), (6, 10, 2.0), (8, 9, 1.5), (9, 10, 0.5)])
#
#
# def find_paths(G, start, end):
#     # 生成每对节点间3条不同的路径
#     paths_dict = {}
#     for u, v in itertools.combinations(G.nodes(), 2):
#         print(f'Paths from {u} to {v}:')
#         for i, path in enumerate(nx.all_simple_paths(G, u, v, cutoff=3)):
#             length = nx.shortest_path_length(G, u, v, weight='weight')
#             paths_dict[tuple(path)] = length
#             print(f'  Path {i + 1}: {path}, length: {length}')
#
#     print(paths_dict)
#
#
# find_paths(G, 1, 3)
