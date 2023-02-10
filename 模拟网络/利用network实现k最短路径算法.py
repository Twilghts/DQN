from heapq import heappush, heappop


def k_shortest_paths(_G, s, t, K):
    # G: weighted directed graph, with set of vertices V and set of directed edges E
    # s: source node
    # t: destination node
    # K: number of the shortest paths to find
    # w(u, v): cost of directed edge from node u to node v (costs are non-negative)

    # Initialize the set of the shortest paths P to be empty
    _P: set = set()

    # Initialize the count for all nodes u in the graph to be 0
    count: dict = {_u: 0 for _u in _G.nodes}

    # Initialize the heap B with the path Ps = {s} (a path consisting of just the source node s) with a cost of 0
    b: list = [(0, [s])]

    while b and count[t] < K:
        # Retrieve the path Pu with the lowest cost from the heap B
        _C, pu = heappop(b)

        # Increment count for the destination node u of this path by 1
        _u = pu[-1]
        count[_u] += 1

        if _u == t:
            # If the destination node u of the path Pu is the destination node t, add Pu to the set of the shortest
            # paths P
            _P.add(tuple(pu))

        if count[_u] <= K:
            # Iterate through each vertex v adjacent to u
            for _v in _G.neighbors(_u):
                # Create a new path Pv by concatenating the edge (u, v) to the path Pu
                pv = pu + [_v]

                # Insert this new path into the heap B with a cost equal to the cost of Pu plus the weight w(u,
                # v) of the edge (u, v)
                heappush(b, (_C + _G.get_edge_data(_u, _v, default={'weight': 1})['weight'], pv))

    # Return the set of the shortest paths P
    return _P
