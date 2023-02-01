import heapq


def yen(graph, start, end, k):
    # Initialize the shortest paths
    shortest_paths = []

    # Find the first shortest path
    distances = {node: float("inf") for node in graph}
    distances[start] = 0
    previous = {node: None for node in graph}
    queue = []
    heapq.heappush(queue, (0, start))
    while queue:
        distance, node = heapq.heappop(queue)
        if node == end:
            path = []
            current = end
            while current is not None:
                path.append(current)
                current = previous[current]
            path = list(reversed(path))
            shortest_paths.append(path)
            break
        for neighbor, cost in graph[node].items():
            new_distance = distance + cost
            if new_distance < distances[neighbor]:
                distances[neighbor] = new_distance
                previous[neighbor] = node
                heapq.heappush(queue, (new_distance, neighbor))

    # Find the remaining shortest paths
    for i in range(1, k):
        # Modify the weights of the edges in the graph
        for node, neighbors in graph.items():
            for neighbor, cost in neighbors.items():
                if (node, neighbor) in shortest_paths[i - 1] or (neighbor, node) in shortest_paths[i - 1]:
                    neighbors[neighbor] = float("inf")

        # Find the next shortest path
        distances = {node: float("inf") for node in graph}
        distances[start] = 0
        previous = {node: None for node in graph}
        queue = []
        heapq.heappush(queue, (0, start))
        while queue:
            distance, node = heapq.heappop(queue)
            if node == end:
                path = []
                current = end
                while current is not None:
                    path.append(current)
                    current = previous[current]
                path = list(reversed(path))
                shortest_paths.append(path)
                break
            for neighbor, cost in graph[node].items():
                new_distance = distance + cost
                if new_distance < distances[neighbor]:
                    distances[neighbor] = new_distance
                    previous[neighbor] = node
                    heapq.heappush(queue, (new_distance, neighbor))

    return shortest_paths
