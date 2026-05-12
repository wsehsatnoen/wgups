import csv

locations = {}
num_addresses = 0

with open("addresses.csv", "r") as csvfile:
    reader = csv.DictReader(csvfile)
    counter = 0
    for row in reader:
        locations[row['Address']] = counter
        counter += 1
        num_addresses += 1


print(locations)
print(num_addresses)

distance_matrix = [[0.0 for _ in range(num_addresses)] for _ in range(num_addresses)]

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

distances = distance_matrix

def print_matrix():
    for row in distances:
        print(row)