import csv
from floyd_warshall import *

# This file is used to parse the CSV files and create data structures to hold that information. The application can then
# use these data structures for many reasons.

locations = {}
num_addresses = 0

# This portion will grab all of the addresses that the application will deliver to and store them in a list.
# Time Complexity: O(N)
# Space Complexity: O(N)
with open("addresses.csv", "r") as csvfile:
    reader = csv.DictReader(csvfile)
    counter = 0
    for row in reader:
        locations[row['Address']] = counter
        counter += 1
        num_addresses += 1

# This distance matrix will store all of the distances between each address in a two-dimensional array.
# Time Complexity: O(N^2)
# Space Complexity: O(N)
distance_matrix = [[0.0 for x in range(num_addresses)] for x in range(num_addresses)]

# This will parse the CSV file and populate the distance matrix with the distances between each address.
# Time Complexity: O(N^2)
# Space Complexity: O(N)
with open("distances.csv", "r") as csvfile:
    reader = csv.reader(csvfile)
    for row_index, row in enumerate(reader):
        for col_index, value in enumerate(row):
            value = value.strip()
            if value == "":
                continue

            distance = float(value)

            distance_matrix[row_index][col_index] = distance
            distance_matrix[col_index][row_index] = distance

# This will calculate the shortest distance between each pair of addresses using the Floyd-Warshall algorithm in the separate file.
# Time Complexity: O(N^3)
# Space Complexity: O(N^2)
all_pairs_shortest_path = floyd_warshall(distance_matrix, num_addresses)

# This will allow us to print the distance matrix to the console if needed.
def print_matrix():
    for row in distance_matrix:
        print(row)