import csv
import datetime
import re
from package import Package, Status
from global_variables import *

def receive_package():
    with open("packages.csv", "r") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            package = Package(row['id'], row['address'], row['city'], row['state'], row['zipcode'], row['delivery_deadline'], row['weight'], row['notes'])
            wgups_table.insert(package)
            handle_package(package)
    sort_loading_queue()

def handle_package(package):
    update_deadline(package)
    handle_notes(package)
    if package.get_id() in delayed_package_ids:
        return
    address_mixer(package)
    if package.get_id() in special_case_packages:
        return
    loading_queue.append(package.get_id())

def update_deadline(package):
    if "EOD" in package.deadline:
        package.deadline = datetime.time(17, 00)
    else:
        package.deadline = datetime.datetime.strptime(package.deadline, "%I:%M %p").time()

def handle_notes(package):
    note = package.get_notes()
    if "Can only be on truck 2" in note:
        special_case_packages.append(package.get_id())
        return
    if "Must be delivered with" in note:
        paired_package = [int(package_id) for package_id in re.findall(r'\d+', note)]
        special_case_packages.append(package.get_id())
        for i in paired_package:
            special_case_packages.append(i)
        return
    if "Delayed on flight" in note:
        package.update_status(Status.LABEL_CREATED)
        delayed_package_ids.add(package.get_id())
        return
    if "Wrong address listed" in note:
        package.update_status(Status.LABEL_CREATED)
        package.update_address(None, None, None, None)
        delayed_package_ids.add(package.get_id())
        return

def address_mixer(package):
    address = package.get_address()
    if address in addresses:
        addresses[address].append(package.get_id())
    else:
        addresses[address] = [package.get_id()]

def delayed_package_handler(time):
    if time == datetime.time(10, 20):
        wgups_table.get_bucket(9).update_address("410 S State St", "Salt Lake City", "UT", "84111")
        wgups_table.get_bucket(9).update_status(Status.AT_HUB)
        loading_queue.append(9)
        address_mixer(wgups_table.get_bucket(9))
    if time == datetime.time(9, 5):
        for package_id in delayed_package_ids:
            if package_id == 9:
                continue
            package = wgups_table.get_bucket(package_id)
            package.update_status(Status.AT_HUB)
            loading_queue.append(package_id)
            address_mixer(package)
    sort_loading_queue()
