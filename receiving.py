import csv
import re
from datetime import datetime

from package import Package, Status
from global_variables import *

# This python file is used to read the CSV file of packages and receive/insert them into the Hash Table.
# Time Complexity: O(N)
# Space Complexity: O(N)
def receive_package():
    with open("packages.csv", "r") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            package = Package(row['id'], row['address'], row['city'], row['state'], row['zipcode'], row['delivery_deadline'], row['weight'], row['notes'])
            handle_package(package)
            wgups_table.insert(package)

# Of course, there is some cleaning and sorting to do with each of the packages, that is what this function is for.
# Time Complexity: O(1)
# Space Complexity: O(1)
def handle_package(package):
    update_deadline(package)
    handle_notes(package)
    if package.get_id() in delayed_package_ids:
        package.update_status(Status.LABEL_CREATED, datetime.time(7, 30))
        return
    address_mixer(package)
    package.update_status(Status.AT_HUB, datetime.time(7, 30))
    if package.get_id() in truck_two_packages or package.get_id() in paired_packages:
        return
    if package.get_deadline() < datetime.time(17, 00):
        priority_set.add(package.get_id())
        return
    loading_queue.add(package.get_id())

# This is a simple helper function that updates the deadline from a string to datetime.time so the application can work with it.
# Time Complexity: O(1)
# Space Complexity: O(1)
def update_deadline(package):
    if "EOD" in package.get_deadline():
        package.update_deadline(datetime.time(17, 00))
    else:
        package.update_deadline(datetime.datetime.strptime(package.get_deadline(), "%I:%M %p").time())

# There are special notes on some of the packages that need to be handled, that is where this function comes in.
# Time Complexity: O(N)
# Space Complexity: O(1)
def handle_notes(package):
    note = package.get_notes()
    if "Can only be on truck 2" in note:
        truck_two_packages.add(package.get_id())
        package.update_required_truck(2)
        return
    if "Must be delivered with" in note:
        paired_package = [int(package_id) for package_id in re.findall(r'\d+', note)]
        paired_packages.add(package.get_id())
        for i in paired_package:
            paired_packages.add(i) if i not in paired_packages else None
            if i in loading_queue:
                loading_queue.remove(i)
            if i in priority_set:
                priority_set.remove(i)
        return
    if "Delayed on flight" in note:
        delayed_package_ids.add(package.get_id())
        return
    if "Wrong address listed" in note:
        package.update_address(None, None, None, None)
        delayed_package_ids.add(package.get_id())
        return

# To help minimize the number of miles traveled, a good practice is to not go to one location more than once, so
# this function will take the address from the packages and pair those in a python dictionary so they can be loaded onto
# a truck together
# Time Complexity: O(1)
# Space Complexity: O(N)
def address_mixer(package):
    address = package.get_address()
    if address in addresses:
        if package.get_deadline() < addresses[address][0]:
            addresses[address][0] = package.get_deadline()
        addresses[address][1].append(package.get_id())
    else:
        addresses[address] = [package.get_deadline(), [package.get_id()]]

# This function will handle the delayed packages, and even the one that has the wrong address listed. This will update and
# sort those packages into the correct queues once they arrive at the hub/address is corrected.
# Time Complexity: O(N)
# Space Complexity: O(1)
def delayed_package_handler(time):
    if time >= datetime.time(10, 20):
        wgups_table.get_bucket(9).update_address("410 S State St", "Salt Lake City", "UT", "84111")
        wgups_table.get_bucket(9).update_status(Status.AT_HUB, time)
        loading_queue.add(9)
        address_mixer(wgups_table.get_bucket(9))
        delayed_package_ids.remove(9)
    if time >= datetime.time(9, 5):
        for package_id in delayed_package_ids:
            if package_id == 9:
                continue
            package = wgups_table.get_bucket(package_id)
            package.update_status(Status.AT_HUB, time)
            if package.get_deadline() < datetime.time(17, 00):
                priority_set.add(package_id)
            else:
                loading_queue.add(package_id)
            address_mixer(package)
        delayed_package_ids.clear()
        delayed_package_ids.add(9)