from datetime import datetime

from package import Package, PackageBucket, hash

# Here is the Hash Table that will store all the packages:
class HashTable:

    # Time Complexity: O(1)
    # Space Complexity: O(1)
    def __init__(self, initial_size: int = 40):
        self.table = [PackageBucket.EMPTY_SINCE_START] * initial_size
        self.size = initial_size

    # Time Complexity: O(N)
    # Space Complexity: O(N)
    def print_table(self, time: datetime = None):
        string = f"Table Size: {self.size} \nTable Contents:\n==============================================="
        index = 0
        for bucket in self.table:
            string += f"\nIndex: {index:2} || {bucket.print_package(time)}"
            index += 1
        string += "\n==============================================="
        print(string)

    # This function will take an ID and return the package that is stored in the bucket that is found quadratically.
    # The ID is hashed (in our case, it is a direct hash of the id), then the quadratic function is used to find the
    # bucket that the package is stored in, continuing to increase i until a bucket is found that either matches the ID
    # or is empty since start.
    # Time Complexity: O(1)
    # Space Complexity: O(1)
    def get_bucket(self, key):
        for i in range(self.size):
            index = (key + i + i * i) % self.size
            if self.table[index].is_empty_since_start():
                return None
            if self.table[index].is_empty_after_removal():
                continue
            if int(self.table[index].get_id()) == key:
                return self.table[index]
        return None

    # This function will take a package and insert it into the table. If the table is full, it will resize the table
    # and insert the package into the new table. The package ID is hashed (in our case, it is a direct hash of the id),
    # then the quadratic function is used to find an bucket that the package will be stored in.
    # Time Complexity: O(1)
    # Space Complexity: O(1)
    def insert(self, package: Package):
        for i in range(self.size):
            index = (hash(package) + i + i * i) % self.size
            if self.table[index].is_empty():
                self.table[index] = package
                return

        self.resize(package)

    # This function will take an ID and remove the package from the table. The ID is hashed (in our case, it is a direct
    # hash of the id), then the quadratic function is used to find the bucket that the package is stored in. It will then
    # return the package that was removed and set the bucket to empty after removal.
    # Time Complexity: O(1)
    # Space Complexity: O(1)
    def remove(self, key: int):
        for i in range(self.size):
            index = (key + i + i * i) % self.size
            if self.table[index].is_empty_since_start():
                return None
            elif self.table[index].get_id() == key:
                package_holder = self.table[index]
                self.table[index] = PackageBucket.EMPTY_AFTER_REMOVAL
                return package_holder
        return None

    # Time Complexity: O(N)
    # Space Complexity: O(N)
    def resize(self, new_package: Package):
        temptable = [PackageBucket.EMPTY_SINCE_START] * (self.size * 2)
        for bucket in self.table:
            if not bucket.is_empty():
                for i in range(self.size):
                    index = (int(bucket.get_id()) + i + i * i) % self.size
                    if self.table[index].is_empty():
                        self.table[index] = bucket
                        return

        self.table = temptable
        self.size *= 2

        for i in range(self.size):
            index = (new_package.get_id() + i + i * i) % self.size
            if self.table[index].is_empty():
                self.table[index] = new_package
                return
