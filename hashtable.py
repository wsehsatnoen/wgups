from package import Package

def hash(item: Package):
    return item.get_id()

# This here is a bucket class that will store the package. It is also
# used to initialize two empty buckets for hash table functionality.
class Bucket:

    def __init__(self, item: Package = None):
        self.item = item
        self.key = item.get_id() if item is not None else None

    def is_empty(self):
        if self is Bucket.EMPTY_SINCE_START:
            return True
        return self is Bucket.EMPTY_AFTER_REMOVAL

    def is_emtpy_since_start(self):
        return self is Bucket.EMPTY_SINCE_START

    def is_empty_after_removal(self):
        return self is Bucket.EMPTY_AFTER_REMOVAL

    def get_id(self):
        return self.key if self.item is not None else None

Bucket.EMPTY_SINCE_START = Bucket()
Bucket.EMPTY_AFTER_REMOVAL = Bucket()

class Hashtable:

    def __init__(self, initial_size=40):
        self.table = [Bucket.EMPTY_SINCE_START] * initial_size
        self.size = initial_size

    def insert(self, item: Package):
        bucket_item = Bucket(item)

        for i in range(self.size):
            index = (hash(item) + i + i * i) % self.size
            if self.table[index].is_empty():
                self.table[i] = bucket_item
                return

        # If we get here, the table is full and needs to be resized.
        self.resize()

    def get(self, key):

        for i in range(self.size):
            index = (hash(key) + i + i * i) % self.size
            if self.table[index].get_id() == key:
                return self.table[index].item
            elif self.table[index].is_emtpy_since_start():
                return None
        return None

    def remove(self, key):

        for i in range(self.size):
            index = (hash(key) + i + i * i) % self.size

            if self.table[index].is_emtpy_since_start():
                return None

            if self.table[index].get_id() == key:
                item_holder = self.table[index].item
                self.table[index] = Bucket.EMPTY_AFTER_REMOVAL
                return item_holder

        return None

    def resize(self):
        self.size *= 1.5
        temp_table = [Bucket.EMPTY_SINCE_START] * self.size
        for bucket in self.table:
            if not bucket.is_empty():
                for i in range(self.size):
                    index = (bucket.get_id() + i + i * i) % self.size
                    if self.table[index].is_empty():
                        self.table[i] = bucket
                        return
        self.table = temp_table
