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
    address_mixer(package)
    if any(package.get_id() in x for x in [delayed_package_ids, special_case_packages]):
        return
    loading_queue.append([package.get_id(), package.get_deadline()])

def update_deadline(package):
    if "EOD" in package.deadline:
        package.deadline = datetime.time(17, 00)
    else:
        package.deadline = datetime.datetime.strptime(package.deadline, "%I:%M %p").time()

def handle_notes(package):
    note = package.get_notes()
    if "Can only be on truck 2" in note:
        package.set_required_truck(2)
        special_case_packages.add(package.get_id())
        return
    if "Must be delivered with" in note:
        paired_package = [int(package_id) for package_id in re.findall(r'\d+', note)]
        special_case_packages.add(package.get_id())
        for i in paired_package:
            special_case_packages.add(i)
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

def delayed_package_handler():
    pass