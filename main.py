from receiving import *
from global_variables import *
from shipping import build_regular_shipment, build_special_case_shipment, build_route

receive_package()

print(wgups_table)

shipments.append(build_special_case_shipment())
shipments.append(build_regular_shipment())

print_shipments()

route_one, route_dis_one = build_route(shipments[0])
print_route(route_one, route_dis_one)

route_two, route_dis_two = build_route(shipments[1])
print_route(route_two, route_dis_two)

delayed_package_handler(datetime.time(9, 5))

shipments.append(build_regular_shipment())

route_three, route_dis_three = build_route(shipments[2])

delayed_package_handler(datetime.time(10, 20))

shipments.append(build_regular_shipment())

route_four, route_dis_four = build_route(shipments[3])

print_route(route_three, route_dis_three)
print_route(route_four, route_dis_four)

print_loading_queue()


