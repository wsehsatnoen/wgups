import copy

from dijkstras import dijkstras, get_route_distance, get_distance
from global_variables import *
import datetime

from package import Status

# Once all of the packages have been received, this is where they will be sorted onto the trucks and the routes are
# officially built.

# Here is the function that will pull from a specified set and build a manifest with those packages.
def build_manifest(packages):
    manifest = {}
    count = 0
    packages_in_manifest = set()

    # This will parse through the set of packages and add them to the manifest.
    # Time Complexity: O(N)
    # Space Complexity: O(N)
    for id in packages:
        package = wgups_table.get_bucket(id)
        same_address = addresses[package.get_address()]

        # To minimize the number of miles traveled, here is where the creation of the address_mixer benifets. Packages
        # that are going to the same address will be loaded together, but keeping in mind the 16 maximum capacity.
        if count + len(same_address[1]) <= 16 and package.get_address() not in manifest:
            # Because python has an extreme use of pointers, unfortunately we need to make a copy of the addresses to add
            # to the manifest.
            manifest[package.get_address()] = copy.deepcopy(same_address)
            count += len(same_address[1])
            packages_in_manifest.update(same_address[1])

    account_for_packages(packages_in_manifest)

    return manifest, packages_in_manifest

# Whenever packages are loaded onto a truck, they will need to be removed from the sets so that they are not
# attempted to be handled again.
# Time Complexity: O(N^2)
# Space Complexity: O(1)
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

# This function will take the manifest that was created and build the route for that shipment. It will take all of the addresses
# on that manifest, sort them into two groups (priority, and non-priority) and first built a route with the priority list, then
# append the route of the non-priority list.
# Time Complexity: O(N^2) (Dijkstra's algorithm is the time determining algorithm, thus the N^2)
# Space Complexity: O(N)
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

# Now that we have a manifest and the routes built, here is where we will ship and update the status of each of the
# packages.
# Time Complexity: O(N^2)
# Space Complexity: O(N)
def ship(manifest, package_ids, truck, driver, time = None):
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
    truck.load(manifest, package_ids, delivery_time_list, distance, driver, time)
    return distance