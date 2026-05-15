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
            handle_package(package)
            wgups_table.insert(package)

def handle_package(package):
    update_deadline(package)
    handle_notes(package)
    if package.get_id() in delayed_package_ids:
        package.update_status(Status.LABEL_CREATED)
        return
    address_mixer(package)
    package.update_status(Status.AT_HUB)
    if package.get_id() in truck_two_packages or package.get_id() in paired_packages:
        return
    if package.get_deadline() < datetime.time(17, 00):
        priority_set.add(package.get_id())
        return
    loading_queue.add(package.get_id())

def update_deadline(package):
    if "EOD" in package.get_deadline():
        package.update_deadline(datetime.time(17, 00))
    else:
        package.update_deadline(datetime.datetime.strptime(package.get_deadline(), "%I:%M %p").time())

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

def address_mixer(package):
    address = package.get_address()
    if address in addresses:
        if package.get_deadline() < addresses[address][0]:
            addresses[address][0] = package.get_deadline()
        addresses[address][1].append(package.get_id())
    else:
        addresses[address] = [package.get_deadline(), [package.get_id()]]

def delayed_package_handler(time):
    if time >= datetime.time(10, 20):
        wgups_table.get_bucket(9).update_address("410 S State St", "Salt Lake City", "UT", "84111")
        wgups_table.get_bucket(9).update_status(Status.AT_HUB)
        loading_queue.add(9)
        address_mixer(wgups_table.get_bucket(9))
        delayed_package_ids.remove(9)
    if time >= datetime.time(9, 5):
        for package_id in delayed_package_ids:
            if package_id == 9:
                continue
            package = wgups_table.get_bucket(package_id)
            package.update_status(Status.AT_HUB)
            if package.get_deadline() < datetime.time(17, 00):
                priority_set.add(package_id)
            else:
                loading_queue.add(package_id)
            address_mixer(package)
        delayed_package_ids.clear()
        delayed_package_ids.add(9)