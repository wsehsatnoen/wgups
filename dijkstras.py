import math

from locations import distance_matrix, locations, all_pairs_shortest_path

def dijkstras(nodes):

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

def get_route_distance(route):
    distance = 0
    for i in range(len(route) - 1):
        distance += all_pairs_shortest_path[locations[route[i]]][locations[route[i + 1]]]
    return distance

