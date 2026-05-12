import math

from dijkstras import dijkstras, get_route_distance
from global_variables import *
from locations import *
from receiving import address_mixer


def build_special_case_shipment_paired():
    manifest = {}
    remove_from_lists = []
    capacity = 0

    for package_id in paired_packages:
        package = wgups_table.get_bucket(package_id)
        same_address_packages = addresses[package.get_address()]

        if package.get_address() not in manifest:
            manifest[package.get_address()] = [package.get_deadline(), same_address_packages]
            capacity += len(same_address_packages)
            remove_from_lists.extend(same_address_packages)


    for package_id in remove_from_lists:
        loading_queue.remove(package_id) if package_id in loading_queue else None
        if wgups_table.get_bucket(package_id).get_address() in addresses:
            del addresses[wgups_table.get_bucket(package_id).get_address()]

    return manifest

def build_special_case_shipment_truck():
    manifest = {}
    remove_from_lists = []
    current_capacity = 0

    for package_id in truck_two_packages:
        package = wgups_table.get_bucket(package_id)
        same_address_packages = addresses[package.get_address()]

        if current_capacity + len(same_address_packages) <= 16 and package.get_address() not in manifest:
            manifest[package.get_address()] = [package.get_deadline(), same_address_packages]
            current_capacity += len(same_address_packages)
            remove_from_lists.extend(same_address_packages)

    for package_id in remove_from_lists:
        loading_queue.remove(package_id) if package_id in loading_queue else None
        if wgups_table.get_bucket(package_id).get_address() in addresses:
            del addresses[wgups_table.get_bucket(package_id).get_address()]

    return manifest

def build_express_shipment(manifest = None, current_capacity = 0):
    manifest = manifest if manifest else {}
    remove_from_lists = []
    current_capacity = current_capacity if current_capacity else 0

    for package_id in loading_queue:
        package = wgups_table.get_bucket(package_id)
        same_address_packages = addresses[package.get_address()]
        if current_capacity + len(same_address_packages) <= 16 and package.get_address() not in manifest and package.get_deadline() < datetime.time(17, 0):
            manifest[package.get_address()] = [package.get_deadline(), same_address_packages]
            current_capacity += len(same_address_packages)
            remove_from_lists.extend(same_address_packages)

    for package_id in remove_from_lists:
        loading_queue.remove(package_id) if package_id in loading_queue else None
        if wgups_table.get_bucket(package_id).get_address() in addresses:
            del addresses[wgups_table.get_bucket(package_id).get_address()]

    return manifest

def build_regular_shipment(manifest = None, current_capacity = 0):
    manifest = manifest if manifest else {}
    remove_from_lists = []
    current_capacity = current_capacity if current_capacity else 0
    
    for package_id in loading_queue:
        package = wgups_table.get_bucket(package_id)
        same_address_packages = addresses[package.get_address()]
        
        if current_capacity + len(same_address_packages) <= 16 and package.get_address() not in manifest:
            manifest[package.get_address()] = [package.get_deadline(), same_address_packages]
            current_capacity += len(same_address_packages)
            remove_from_lists.extend(same_address_packages)
            
    for package_id in remove_from_lists:
        loading_queue.remove(package_id) if package_id in loading_queue else None
        if wgups_table.get_bucket(package_id).get_address() in addresses:
            del addresses[wgups_table.get_bucket(package_id).get_address()]

    return manifest

def build_route(manifest):
    priority_list = []
    non_priority_list = []

    route = []

    for address, info in manifest.items():
        if info[0] < datetime.time(17, 0):
            priority_list.append(address)
        else:
            non_priority_list.append(address)

    route.extend(dijkstras(priority_list))
    route.extend(dijkstras(non_priority_list))

    route.insert(0, "HUB")
    route.append("HUB")

    distance = get_route_distance(route)

    return route, distance
