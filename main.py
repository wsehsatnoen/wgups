import threading

from receiving import *
from shipping import *
import time

receive_package()

manifest_one, packages_one = build_manifest(paired_packages.union(truck_two_packages))
ship(manifest_one, packages_one, truck_one, 1, datetime.time(8, 0))

delayed_package_handler(datetime.time(9, 5))
manifest_two, packages_two = build_manifest(priority_set)
ship(manifest_two, packages_two, truck_two, 2, datetime.time(9, 5))

delayed_package_handler(datetime.time(10, 20))
manifest_three, packages_three = build_manifest(loading_queue)
ship(manifest_three, packages_three, truck_three, 1, datetime.time(10, 25))

current_time = datetime.time(7, 30)

print("Welcome!!")
print(f"Current Time: {current_time}")
print("Booting up, please wait...")
while True:
    print("\033[2JHello there! What would you like to do?\n1. View Packages\n2. View Truck Status\n3. Change Time\n4. Exit", end="")
    input_choice = int(input("\nEnter your choice: "))
    match input_choice:
        case 1:
            wgups_table.print_table(current_time)
            input("Press Enter to continue...")
        case 2:
            print(truck_one.update_status(current_time))
            print(truck_two.update_status(current_time))
            print(truck_three.update_status(current_time))
            input("Press Enter to continue...")
        case 3:
            print("How much time would you like to advance the clock by?:\n1. 15 minutes\n2. 30 minutes\n3. 45 minutes\n4. 60 minutes\n ")
            match int(input("Enter your choice: ")):
                case 1:
                    current_time = (datetime.datetime.combine(datetime.date.today(), current_time) + datetime.timedelta(
                        minutes=15)).time()
                case 2:
                    current_time = (datetime.datetime.combine(datetime.date.today(), current_time) + datetime.timedelta(
                        minutes=30)).time()
                case 3:
                    current_time = (datetime.datetime.combine(datetime.date.today(), current_time) + datetime.timedelta(
                        minutes=45)).time()
                case 4:
                    current_time = (datetime.datetime.combine(datetime.date.today(), current_time) + datetime.timedelta(
                        minutes=60)).time()
                case _:
                    print("Invalid choice. Please try again.")
            print(f"Current Time: {current_time}")
        case 4:
            print("Goodbye!")
            exit()
        case _:
            print("Invalid choice. Please try again.")

# for milage, just take the time requested and the difference from the time the truck left to get the current