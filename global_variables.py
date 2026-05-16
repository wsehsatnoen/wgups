import datetime
from hashtable import HashTable
from truck import Truck

# The challenge that I wanted to give myself was to deviate away from OOP (Object-Oriented Programming) and practice FP (Functionality Programming)
# Thus, the use of classes are kept to a minimal: Packages (and empty package buckets), the Hash Table, and Trucks are the
# only objects in this application. Hence, this file is used to set the global variables for the application.

wgups_table = HashTable()
truck_one = Truck(1)
truck_two = Truck(2)
truck_three = Truck(3)

total_miles = 0

addresses = {}
paired_packages = set()
truck_two_packages = set()
delayed_package_ids = set()
loading_queue = set()
priority_set = set()

miles_driven = 0

# Simple print statements
def print_addresses():
    for address in addresses:
        print(f"{address} || Soonest Deadline: {addresses[address][0]} || Package IDs: {addresses[address][1]}")

def print_manifest(manifest):
    for address, info in manifest.items():
        print(f"Address: {address} || Deadline: {info[0]} || Packages: {info[1]}")

def print_route(route, route_distance):
    print(f"Route: {route} || Distance: {route_distance} miles")

def print_loading_queue():
    for package in loading_queue:
        print(f"Package ID: {package} || Deadline: {wgups_table.get_bucket(package).get_deadline()}")
