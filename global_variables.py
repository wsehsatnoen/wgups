from hashtable import HashTable

wgups_table = HashTable()
special_case_packages = set()
delayed_package_ids = set()
addresses = {}
loading_queue = []

shipments = []
miles_driven = 0

def print_addresses():
    for address in addresses:
        print(f"{address} || Package IDs: {str(addresses[address])}")

def print_manifest(manifest):
    for package_id, info in manifest.items():
        print(f"Address: {package_id} || Deadline: {info[0]} || Packages: {info[1]}")

def sort_loading_queue():
    loading_queue.sort(key=lambda x: x[1])

def print_loading_queue():
    for package in loading_queue:
        print(f"Package ID: {package[0]} || Deadline: {package[1]}")
