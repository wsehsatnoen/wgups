from receiving import *
from global_variables import *
from shipping import *
from truck import Truck, Driver

receive_package()

truck_one = Truck(1)
truck_two = Truck(2)
truck_three = Truck(3)

driver_one = Driver(1)
driver_two = Driver(2)

delayed_package_handler(datetime.time(9, 4))

manifest_one = build_manifest(paired_packages.union(truck_two_packages))
route_one, route_one_distance = build_route(manifest_one)
print_manifest(manifest_one)
print_route(route_one, route_one_distance)

print(get_distance(route_one[0], route_one[1]))

print(wgups_table)

print(len(wgups_table.get_bucket(12).get_address()))

# for milage, just take the time requested and the difference from the time the truck left to get the current