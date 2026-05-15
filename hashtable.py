from package import Package, PackageBucket, Status, hash

class HashTable:

    def __init__(self, initial_size: int = 40):
        self.table = [PackageBucket.EMPTY_SINCE_START] * initial_size
        self.size = initial_size


    def __str__(self):
        string = f"Table Size: {self.size} \nTable Contents:\n==============================================="
        index = 0
        for bucket in self.table:
            string += f"\nIndex: {index:2} || {bucket}"
            index += 1
        string += "\n==============================================="
        return string

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

    def insert(self, package: Package):
        for i in range(self.size):
            index = (hash(package) + i + i * i) % self.size
            if self.table[index].is_empty():
                self.table[index] = package
                return

        self.resize(package)

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
