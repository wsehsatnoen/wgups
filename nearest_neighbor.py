import math

from locations import distance_matrix, locations, all_pairs_shortest_path

# Dijkstra's Algorithm used to find the shortest path.
# Time Complexity: O(N^2)
# Space Complexity: O(N)
def nearest_neighbor(nodes):

    current_node = 0
    path = []

    unvisited_nodes = nodes
    while unvisited_nodes:
        min_node = unvisited_nodes[0]
        min_dis = math.inf
        for node in unvisited_nodes:
            if all_pairs_shortest_path[current_node][locations[node]] < min_dis:
                min_node = node
                min_dis = all_pairs_shortest_path[current_node][locations[node]]
        path.append(min_node)
        unvisited_nodes.remove(min_node)
        current_node = locations[min_node]
    return path

# Returns the distance of a route that has been built to ensure that the routes do not exceed the max distance.
# Time Complexity: O(N)
# Space Complexity: O(1)
def get_route_distance(route):
    distance = 0
    for i in range(len(route) - 1):
        distance += all_pairs_shortest_path[locations[route[i]]][locations[route[i + 1]]]
    return distance

# Returns the distance between two addresses.
# Time Complexity: O(1)
# Space Complexity: O(1)
def get_distance(address_one, address_two):
    return all_pairs_shortest_path[locations[address_one]][locations[address_two]]

