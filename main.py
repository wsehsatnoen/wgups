from receiving import *
from shipping import *

receive_package()

manifest_one, packages_one = build_manifest(paired_packages.union(truck_two_packages))
ship(manifest_one, packages_one, datetime.time(8, 0))

delayed_package_handler(datetime.time(9, 5))
manifest_two, packages_two = build_manifest(priority_set)
ship(manifest_two, packages_two, datetime.time(9, 5))


delayed_package_handler(datetime.time(10, 20))
manifest_three, packages_three = build_manifest(loading_queue)
ship(manifest_three, packages_three, datetime.time(10, 25))



wgups_table.print_table(datetime.time(9, 59))

# for milage, just take the time requested and the difference from the time the truck left to get the current