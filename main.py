from receiving import *
from global_variables import *
from shipping import build_shipment, build_special_case_shipment

receive_package()

print(wgups_table)

print_addresses()

print_loading_queue()

print(required_packages_set)

manifest = build_shipment(build_special_case_shipment())

print_manifest(manifest)