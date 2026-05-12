from receiving import *
from global_variables import *
from shipping import *

receive_package()

print(wgups_table)

print_addresses()

shipments.append(build_special_case_shipment_truck())
shipments.append(build_special_case_shipment_paired())

delayed_package_handler(datetime.time(9, 5))

shipments.append(build_express_shipment())

delayed_package_handler(datetime.time(10, 20))

shipments.append(build_regular_shipment())

print_shipments()
print_loading_queue()

for shipment in shipments:
    route, route_distance = build_route(shipment)
    print_route(route, route_distance)
    print("----------------")
    miles_driven += route_distance

print(f"Miles Driven: {miles_driven} miles")


