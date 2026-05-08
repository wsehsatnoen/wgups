from enum import Enum

class Status(Enum):
    created = "created"
    received = "received"
    loaded = "loaded"
    en_route = "en_route"
    delivered = "delivered"

class Package:

    def __init__(self, id, delivery_address, delivery_city, delivery_state, delivery_zip, delivery_deadline, package_weight, special_notes,
                 status: Status):
        self.id = id
        self.delivery_address = delivery_address
        self.delivery_city = delivery_city
        self.delivery_state = delivery_state
        self.delivery_zip = delivery_zip
        self.delivery_deadline = delivery_deadline
        self.package_weight = package_weight
        self.special_notes = special_notes
        self.status = status
        self.required_truck = None
        self.required_packages_to_pair = []

    def set_status(self, status: Status):
        self.status = status

    def set_required_truck(self, required_truck):
        self.required_truck = required_truck

    def set_required_packages_to_pair(self, required_package_to_pair):
        self.required_packages_to_pair.append(required_package_to_pair)

    def get_id(self):
        return self.id
    def get_delivery_address(self):
        return self.delivery_address
    def get_delivery_city(self):
        return self.delivery_city
    def get_delivery_state(self):
        return self.delivery_state
    def get_delivery_zip(self):
        return self.delivery_zip
    def get_delivery_deadline(self):
        return self.delivery_deadline
    def get_package_weight(self):
        return self.package_weight
    def get_special_notes(self):
        return self.special_notes
    def get_status(self):
        return self.status
    def get_required_truck(self):
        return self.required_truck
    def get_required_packages_to_pair(self):
        return self.required_packages_to_pair
