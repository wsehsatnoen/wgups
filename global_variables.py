import datetime

from hashtable import HashTable

wgups_table = HashTable()
addresses = {}
paired_packages = set()
truck_two_packages = set()
delayed_package_ids = set()
loading_queue = set()
priority_set = set()

shipments = []
miles_driven = 0

current_time = datetime.time(8, 0)

def print_addresses():
    for address in addresses:
        print(f"{address} || Soonest Deadline: {addresses[address][0]} || Package IDs: {addresses[address][1]}")

def print_shipments():
    for manifest in shipments:
        print("----------------")
        print_manifest(manifest)
        print("----------------")

def print_manifest(manifest):
    for address, info in manifest.items():
        print(f"Address: {address} || Deadline: {info[0]} || Packages: {info[1]}")

def print_route(route, route_distance):
    print(f"Route: {route} || Distance: {route_distance} miles")

def print_loading_queue():
    for package in loading_queue:
        print(f"Package ID: {package} || Deadline: {wgups_table.get_bucket(package).get_deadline()}")
