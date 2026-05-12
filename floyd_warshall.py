
def floyd_warshall(graph, size):
    for intermediate in range(size):
        for start in range(size):
            for end in range(size):
                new_distance = (graph[start][intermediate] + graph[intermediate][end])
                if new_distance < graph[start][end]:
                    graph[start][end] = new_distance
    return graph

