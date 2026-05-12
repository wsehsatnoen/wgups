import math
from random import random

from global_variables import *


def build_special_case_shipment():
    manifest = {}
    remove_from_lists = []
    for package_id in special_case_packages:
        package = wgups_table.get_bucket(package_id)
        same_address_packages = addresses[package.get_address()]
        if package.get_address() not in manifest:
            manifest[package.get_address()] = [package.get_deadline(), same_address_packages]
        remove_from_lists.extend(same_address_packages)

    for package_id in remove_from_lists:
        special_case_packages.remove(package_id) if package_id in special_case_packages else None
        loading_queue.remove(package_id) if package_id in loading_queue else None
        if wgups_table.get_bucket(package_id).get_address() in addresses:
            del addresses[wgups_table.get_bucket(package_id).get_address()]

    return manifest


def build_regular_shipment():
    manifest = {}
    remove_from_lists = []
    current_capacity = 0
    
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
    address_order = []
    for address, info in manifest.get_items():
        pass
    return address_order
