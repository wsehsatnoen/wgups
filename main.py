from receiving import *
from global_variables import *
from shipping import *

receive_package()

print(loading_queue)
print(priority_set)
print(delayed_package_ids)
print(truck_two_packages)
print(paired_packages)

print_addresses()

shipments.append(build_manifest(paired_packages))

delayed_package_handler(datetime.time(9,5))

shipments.append(build_manifest(priority_set))

delayed_package_handler(datetime.time(10,20))

shipments.append(build_manifest(truck_two_packages))
shipments.append(build_manifest(loading_queue))
shipments.append(build_manifest(loading_queue))

print_shipments()

for shipment in shipments:
    route, distance = build_route(shipment)
    miles_driven += distance
    print_route(route, distance)

print(f"Miles Driven: {miles_driven}")

print(loading_queue)
print(priority_set)
print(delayed_package_ids)
print(truck_two_packages)
print(paired_packages)