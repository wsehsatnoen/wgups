import datetime

from hashtable import HashTable

wgups_table = HashTable()
special_case_packages = []
delayed_package_ids = set()
addresses = {}
loading_queue = []

shipments = []
miles_driven = 0

current_time = datetime.time(8, 0)

def print_addresses():
    for address in addresses:
        print(f"{address} || Package IDs: {str(addresses[address])}")

def print_shipments():
    for manifest in shipments:
        print_manifest(manifest)
        print("----------------")

def print_manifest(manifest):
    for address, info in manifest.items():
        print(f"Address: {address} || Deadline: {info[0]} || Packages: {info[1]}")

def print_route(route, route_distance):
    print(f"Route: {route} || Distance: {route_distance} miles")

def sort_loading_queue():
    loading_queue.sort(key=lambda x: wgups_table.get_bucket(x).get_deadline())

def print_loading_queue():
    for package in loading_queue:
        print(f"Package ID: {package} || Deadline: {wgups_table.get_bucket(package).get_deadline()}")
