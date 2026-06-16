# Student ID: #########
# Student Name: Shane Darilek

from receiving import *
from shipping import *

receive_package()

# Here is where all the functions that were created come together to build the routes.

manifest_two, packages_two = build_manifest(priority_set.union(truck_two_packages))
total_miles += ship(manifest_two, packages_two, truck_two, 2, datetime.time(8, 0))

delayed_package_handler(datetime.time(9, 5))
manifest_one, packages_one = build_manifest(paired_packages.union(priority_set))
total_miles += ship(manifest_one, packages_one, truck_one, 1, datetime.time(9, 5))

delayed_package_handler(datetime.time(10, 20))
manifest_three, packages_three = build_manifest(priority_set.union(loading_queue))
total_miles += ship(manifest_three, packages_three, truck_three, 1, datetime.time(10, 40))

current_time = datetime.time(7, 30)

# Here is where the simulation. It allows the user to view the packages, truck status, and change the time.
print("Welcome!!")
print(f"Current Time: {current_time}")
print("Booting up, please wait...")
while True:
    print("\033[2JHello there! What would you like to do?\n1. View Dashboard \n2. Change Time\n3. Get Package Status \n4. Exit", end="")
    input_choice = input("\nEnter your choice: ")
    if input_choice == "1":
        print(f"Current Time: {current_time}")
        print("Total Miles that will be traveled: ", total_miles, " miles")
        wgups_table.print_table(current_time)
        print(truck_one.update_status(current_time))
        print(truck_two.update_status(current_time))
        print(truck_three.update_status(current_time))
    elif input_choice == '2':
        print("How much time would you like to advance the clock by?:\n1. 15 minutes\n2. 30 minutes\n3. 45 minutes\n4. 60 minutes\n ")
        try:
            time_choice = int(input("Enter your choice: "))
        except ValueError:
            print("Invalid choice. Please try again.")
            continue
        match time_choice:
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
    elif input_choice == '3':
        try:
            package_id = int(input("Enter Package ID: "))
        except ValueError:
            print("Invalid choice. Please try again.")
            continue
        try:
            req_time = input("Enter requested time: ")
            requested_time = datetime.time.strptime(req_time, "%H:%M")
        except ValueError:
            print("Invalid choice. Please try again.")
            continue
        package = wgups_table.get_bucket(package_id)
        if package is None:
            print(f"Package ID {package_id} not found.")
            continue
        print(f"Getting Package ID: {package.id} at time: {req_time}")
        print(package.print_package(requested_time))
        print("--------------------------")
    elif input_choice == "4":
        print("The day has ended, here are the results:")
        print(f"Total Miles Driven: {total_miles}")
        print("Packages Delivered = 40")
        print("Goodbye!")
        exit()
    else:
        print("Invalid choice. Please try again.")
