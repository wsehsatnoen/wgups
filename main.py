import receiving
from hashtable import Hashtable
from receiving import packages_to_pair

wgups_table = Hashtable()

receiving.receive_packages(wgups_table)

print(wgups_table.get(32))
print(wgups_table.get(12))
print(wgups_table.get(10))
print(wgups_table.get(16))
print(wgups_table.get(20))

