from enum import Enum

class Status(Enum):
    CREATED = "created"
    RECEIVED = "received"
    LOADED = "loaded"
    EN_ROUTE = "en_route"
    DELIVERED = "delivered"

class Package:

    def __init__(self, id, delivery_address, delivery_city, delivery_state, delivery_zip, delivery_deadline, package_weight, special_notes,
                 status: Status):
        self.id = int(id)
        self.delivery_address = delivery_address
        self.delivery_city = delivery_city
        self.delivery_state = delivery_state
        self.delivery_zip = delivery_zip
        self.delivery_deadline = delivery_deadline
        self.package_weight = package_weight
        self.special_notes = special_notes
        self.receiving_eta = None
        self.status = status.CREATED
        self.required_truck = None
        self.required_packages_to_pair = set()

    def set_status(self, status: Status):
        self.status = status

    def set_required_truck(self, required_truck):
        self.required_truck = required_truck

    def set_required_packages_to_pair(self, required_package_to_pair):
        for package_id in required_package_to_pair:
            self.required_packages_to_pair.add(package_id)

    def set_delivery_address(self, delivery_address):
        self.delivery_address = delivery_address
    def set_delivery_city(self, delivery_city):
        self.delivery_city = delivery_city
    def set_delivery_state(self, delivery_state):
        self.delivery_state = delivery_state
    def set_delivery_zip(self, delivery_zip):
        self.delivery_zip = delivery_zip
    def set_receiving_eta(self, receiving_eta):
        self.receiving_eta = receiving_eta

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
    def get_receiving_eta(self):
        return self.receiving_eta
    def get_status(self):
        return self.status
    def get_required_truck(self):
        return self.required_truck
    def get_required_packages_to_pair(self):
        return self.required_packages_to_pair

    def __str__(self):
        return f"Package {self.id} is {self.status} \n Delivery Deadline: {self.delivery_deadline} \n Delivery Address: {self.delivery_address} \n Delivery City: {self.delivery_city} \n Delivery Zip: {self.delivery_zip} \n Package Weight: {self.package_weight} \n Package Paired With: {str(self.required_packages_to_pair)}"