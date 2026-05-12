from receiving import *
from global_variables import *
from shipping import *

receive_package()

print(wgups_table)

print_addresses()

shipments.append(build_special_case_shipment_truck())

route_one, route_dis_one = build_route(shipments[0])
print_route(route_one, route_dis_one)

shipments.append(build_express_shipment())
route_two, route_dis_two = build_route(shipments[1])
print_route(route_two, route_dis_two)

shipments.append(build_special_case_shipment_paired())
route_three, route_dis_three = build_route(shipments[2])
print_route(route_three, route_dis_three)

print_shipments()

print(route_dis_one)


