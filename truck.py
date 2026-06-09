from datetime import datetime, date
from enum import Enum

# These classes are used to represent the trucks and their status.

class Status(Enum):
    AT_HUB = "At Hub"
    EN_ROUTE = "En Route"
    RETURNING = "Returning"

    def __str__(self):
        return self.value

# This class represents a truck and stores the relative information on it.
class Truck:
    def __init__(self, id, capacity=16):
        self.id = id
        self.capacity = capacity
        self.status = Status.AT_HUB
        self.miles_driven = 0
        self.departure_time = None
        self.driver_id = None
        self.manifest = {}
        self.packages = []
        self.delivery_time_list = []

    # This function will be called when a truck is assigned to a manifest. It will load the truck with the packages
    # and the delivery time list.
    def load(self, manifest, packages, delivery_time_list, distance, driver_id, departure_time: datetime):
        self.status = Status.EN_ROUTE
        self.delivery_time_list = delivery_time_list
        self.manifest = manifest
        self.packages = packages
        self.departure_time = departure_time
        self.miles_driven += distance
        self.driver_id = driver_id

    # This function is used mainly for front end visibility. It will return a string of the packages assigned to the
    # truck.
    def get_packages(self):
        if not self.packages:
            return "No Packages"
        return " ".join(str(package) for package in self.packages) + " "

    def get_id(self):
        return self.id

    # This function is used mainly for front end visibility. It will take the current time from the simulation and
    # update the status of the truck to match that of the time.
    # Time Complexity: O(N^2)
    # Space Complexity: O(1)
    def update_status(self, time: datetime = None):
        # Convert time to datetime if needed for arithmetic
        time_dt = datetime.combine(date.today(), time)
        departure_dt = datetime.combine(date.today(), self.departure_time)

        # Determine current status and driver
        if time_dt <= departure_dt:
            current_driver = "None"
            assigned_package_indicator = "Assigned: "
        else:
            current_driver = self.driver_id
            assigned_package_indicator = "On Board: "

        # Build route visualization strings
        delivered = ""
        en_route_to = ""
        upcoming = ""

        for i, address in enumerate(self.delivery_time_list):
            location = address[0]

            if time >= self.delivery_time_list[i][1]:
                delivered += f"|| \033[92m{location} \033[0m"
                if location in self.manifest:
                    for package_id in self.manifest[location][1]:
                        if package_id in self.packages:
                            self.packages.remove(package_id)
            elif i > 0 and self.delivery_time_list[i - 1][1] <= time < self.delivery_time_list[i][1]:
                if self.delivery_time_list[i][0] == "HUB":
                    self.status = Status.RETURNING
                en_route_to += f"\033[93m========> \033[91m{location}\033[0m || "
            else:
                upcoming += f"\033[94m{location}\033[0m || "

        # Update final status if all packages delivered
        if not self.packages:
            self.driver_id = None
            current_driver = "None"

        return (f"Truck ID: {self.id} || Current Driver: {current_driver} || "
                f"Route Miles: {self.miles_driven} || Packages {assigned_package_indicator}{self.get_packages()}\n"
                f"{delivered}{en_route_to}{upcoming}")

