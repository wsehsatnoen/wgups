import csv
import re
import datetime
# from time_machine import TimeMachine, time_machine

from package import Package, Status

delayed_packages = []
packages_to_pair = set()

# This function is where the magic happens. It will receive all the packages from the file and give the proper handling necessary.
# Included on the bottom is the final case for pairing packages that must be delivered with one another for shipping purposes.
def receive_packages(hashtable):
    with open('packages.csv', 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            package = Package(row['id'], row['address'], row['city'], row['state'], row['zipcode'], row['delivery_deadline'], row['weight'], row['notes'], Status.CREATED)
            special_handling(package)
            hashtable.insert(package)
    for package_id in packages_to_pair:
        hashtable.get(package_id).set_required_packages_to_pair(packages_to_pair)

# This function is where we handle the special cases that may arise. It will determine if the package is required for a specific truck,
# packages that must be delivered with one another, if the package is delayed to the facility, and even if the address is wrong.
def special_handling(package: Package):
    note = package.get_special_notes()
    if "Can only be on truck 2" in note:
        package.set_required_truck(2)
    if "Must be delivered with" in note:
        paired_package_ids = [int(package_id) for package_id in re.findall(r'\d+', note)]
        package.set_required_packages_to_pair(paired_package_ids)
        package_pairer(package)
    if "Delayed on flight" in note:
        if package.get_id() in delayed_packages:
            if time_machine.get_simulation_time() == datetime.time(9, 5):
                package.set_status(Status.RECEIVED)
            return
        package.set_status(Status.CREATED)
        package.set_receiving_eta(datetime.time(9, 5))
        delayed_packages.append(package.get_id())
        return
    if "Wrong address listed" in note:
        if package.get_id() in delayed_packages:
            if time_machine.get_simulation_time() > datetime.time(10, 20):
                package.set_delivery_address("410 S. State St.")
                package.set_delivery_city("Salt Lake City")
                package.set_delivery_state("UT")
                package.set_delivery_zip("84111")
                package.set_status(Status.RECEIVED)
                return
        package.set_status(Status.CREATED)
        delayed_packages.append(package.get_id())
        package.set_receiving_eta(datetime.time(10, 20))
        return

    package.set_status(Status.RECEIVED)

# This function is where we pair packages that must be delivered with one another for shipping purposes.
# It will add the package id to the set of packages that must be paired, and then add the package ids of the packages that must be paired.
def package_pairer(package: Package):
    if package.get_required_packages_to_pair():
        packages_to_pair.add(package.get_id())
        for package_id in package.get_required_packages_to_pair():
            packages_to_pair.add(package_id)
