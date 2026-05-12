from enum import Enum
from datetime import datetime

# For type safety, the use of this Enum class prevents problems.
class Status(Enum):
    LABEL_CREATED = "Label Created"
    AT_HUB = "At Hub"
    LOADED = "Loaded"
    EN_ROUTE= "En Route"
    DELIVERED = "Delivered"

    # Will turn it into a string when printed.
    def __str__(self):
        return self.value

# This will be used for ease of functionality with the hash table. Instead of creating
# a new class for the buckets, the packages themselves will be buckets and these will take
# the place of empty buckets.
class PackageBucket:

    def is_empty(self):
        if self is PackageBucket.EMPTY_SINCE_START:
            return True
        return self is PackageBucket.EMPTY_AFTER_REMOVAL

    def is_empty_since_start(self):
        return self is PackageBucket.EMPTY_SINCE_START

    def is_empty_after_removal(self):
        return self is PackageBucket.EMPTY_AFTER_REMOVAL

    def __str__(self):
        if self.is_empty_since_start():
            return "Empty Since Start"
        elif self.is_empty_after_removal():
            return "Empty After Removal"
        else:
            return None

def hash(package: Package):
    return package.id

# This will create a class of each package that will store the information
# about that package.
class Package(PackageBucket):

    def __init__(self, id: int, address, city, state, zipcode, deadline, weight, notes):
        self.id = int(id)
        self.address = address
        self.city = city
        self.state = state
        self.zipcode = zipcode
        self.deadline = deadline
        self.weight = weight
        self.notes = notes

        self.status = Status.LABEL_CREATED
        self.delivered_time = None
        self.required_truck = None

    # Will turn it into a string when printed.
    def __str__(self):
        return f"Package ID: {self.id} || Status: {self.status} Delivered Time: {self.delivered_time if self.delivered_time is not None else "N/A"} || Deadline: {self.deadline} ||Weight: {self.weight} || Address: {self.address}, {self.city} {self.state}, {self.zipcode} || Required Truck: {self.required_truck} Notes: {self.notes}"

    # Setters
    def update_address(self, address, city, state, zipcode):
        self.address = address
        self.city = city
        self.state = state
        self.zipcode = zipcode

    def update_status(self, status: Status, delivered_time: datetime = None):
        self.status = status
        if status == Status.DELIVERED:
            self.delivered_time = delivered_time

    def set_required_truck(self, truck):
        self.required_truck = truck

    def add_required_package(self, package_id: int):
        self.required_package_set.add(package_id)

    # Getters
    def get_id(self):
        return self.id
    def get_address(self):
        return self.address
    def get_city(self):
        return self.city
    def get_state(self):
        return self.state
    def get_zipcode(self):
        return self.zipcode
    def get_deadline(self):
        return self.deadline
    def get_weight(self):
        return self.weight
    def get_notes(self):
        return self.notes
    def get_status(self):
        return self.status
    def get_delivered_time(self):
        return self.delivered_time
    def get_required_truck(self):
        return self.required_truck

PackageBucket.EMPTY_SINCE_START = PackageBucket()
PackageBucket.EMPTY_AFTER_REMOVAL = PackageBucket()