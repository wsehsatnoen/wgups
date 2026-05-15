import copy

from dijkstras import dijkstras, get_route_distance, get_distance
from global_variables import *
import datetime

from package import Status


def build_manifest(packages):
    manifest = {}
    count = 0
    packages_in_manifest = set()

    for id in packages:
        package = wgups_table.get_bucket(id)
        same_address = addresses[package.get_address()]

        if count + len(same_address[1]) <= 16 and package.get_address() not in manifest:
            manifest[package.get_address()] = copy.deepcopy(same_address)
            count += len(same_address[1])
            packages_in_manifest.update(same_address[1])

    account_for_packages(packages_in_manifest)

    return manifest, packages_in_manifest

def account_for_packages(list_of_packages):
    for id in list_of_packages:

        package = wgups_table.get_bucket(id)
        loading_queue.remove(package.get_id()) if package.get_id() in loading_queue else None
        priority_set.remove(package.get_id()) if package.get_id() in priority_set else None
        truck_two_packages.remove(package.get_id()) if package.get_id() in truck_two_packages else None
        paired_packages.remove(package.get_id()) if package.get_id() in paired_packages else None

        for address in addresses:
            if id in addresses[address][1]:
                addresses[address][1].remove(id)

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

def ship(manifest, package_ids, time = None):
    route, distance = build_route(manifest)
    for package in package_ids:
        wgups_table.get_bucket(package).update_status(Status.EN_ROUTE, time)

    current_time = time
    delivery_time_list = []

    i = 0
    for address in route:
        if i > 0:
            segment_distance = get_distance(route[i - 1], address)
            segment_time = (segment_distance / 18) * 60  # Convert hours to minutes
            current_time = (datetime.datetime.combine(datetime.date.today(), current_time) +
                           datetime.timedelta(minutes=segment_time)).time()
            delivery_time_list.append([address, current_time])

            # Update packages at this address to delivered status
            if address in manifest:
                for package_id in manifest[address][1]:
                    wgups_table.get_bucket(package_id).update_status(Status.DELIVERED, current_time)

        i += 1
    print(current_time, distance, delivery_time_list)