# Floyd Warshall Algorithm that finds the shortest path between all points on the map
# Time Complexity: O(N^3)
# Space Complexity: O(N^2)
def floyd_warshall(graph, size):
    for intermediate in range(size):
        for start in range(size):
            for end in range(size):
                new_distance = (graph[start][intermediate] + graph[intermediate][end])
                if new_distance < graph[start][end]:
                    graph[start][end] = new_distance
    return graph

