from receiving import *
from global_variables import *
from shipping import build_regular_shipment, build_special_case_shipment

receive_package()

print(wgups_table)

shipments.append(build_special_case_shipment())
shipments.append(build_regular_shipment())

print_shipments()