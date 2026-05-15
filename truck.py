from enum import Enum

from global_variables import print_manifest


class truckStatus(Enum):
    IDLE = "IDLE"
    ON_ROUTE = "ON ROUTE"
    RETURNING = "RETURNING"

class Truck:

    def __init__(self, id: int, capacity: int = 16):
        self.id = id
        self.capacity = capacity
        self.truckStatus = truckStatus.IDLE
        self.driver = None
        self.current_location = "HUB"
        self.milage = 0
        self.manifest = None


    def __str__(self):
        return f"Truck ID: {self.id} || Status: {self.truckStatus}\n Manifest: {print_manifest(self.manifest) if self.manifest is not None else "None"}"

    def load_manifest(self, manifest):
        self.manifest = manifest

    def set_status(self, status: truckStatus):
        self.truckStatus = status

    def ship(self):
        if self.manifest is not None and self.driver is not None:
            self.truckStatus = truckStatus.ON_ROUTE
        else:
            print("Truck is not ready to ship.")

class Driver:

    def __init__(self, id: int):
        self.id = id
        self.Status = truckStatus.IDLE
        self.truck = None

    def __str__(self):
        return f"Driver ID: {self.id} || Status: {self.Status}"

    def set_status(self, status: truckStatus):
        self.Status = status

    def assign_truck(self, truck: Truck):
        self.truck = truck


