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

        self.required_truck = None

        self.status = Status.LABEL_CREATED
        self.delivered_time = "Pending "

        self.activity_tracking = []

    # Will turn it into a string when printed.
    def __str__(self):
        return f"Package ID: {self.id:2} || Status: {self.status:13} || Delivered Time: {self.delivered_time} || Deadline: {self.deadline} || Weight: {self.weight:2} || Address: {self.address}, {self.city} {self.state}, {self.zipcode} || Notes: {self.notes}"

    # Setters
    def update_address(self, address, city, state, zipcode):
        self.address = address
        self.city = city
        self.state = state
        self.zipcode = zipcode

    def update_status(self, status: Status, time):
        self.status = status
        self.add_activity(status, time)
        if status == Status.DELIVERED:
            self.delivered_time = time

    def update_required_truck(self, required_truck):
        self.required_truck = required_truck

    def update_deadline(self, deadline: datetime):
        self.deadline = deadline

    def add_activity(self, status, time):
        self.activity_tracking.append([status, time])

    def print_package(self, time: datetime = None):
        if time is None:
            return self.__str__()
        else:
            current_status = self.status
            delivered_time_at = "Pending "
            for activity_status, activity_time in self.activity_tracking:
                if activity_time <= time:
                    current_status = activity_status
                    if activity_status == Status.DELIVERED:
                        delivered_time_at = activity_time
        return f"Package ID: {self.id:2} || Status: {current_status:13} || Delivered Time: {delivered_time_at} || Deadline: {self.deadline} || Weight: {self.weight:2} || Address: {self.address}, {self.city} {self.state}, {self.zipcode} || Notes: {self.notes}"

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