from package import Package

def hash(item: Package):
    return item.get_id()

# This here is a bucket class that will store the package. It is also
# used to initialize two empty buckets for hash table functionality.
class Bucket:

    def __init__(self, item: Package = None):
        self.item = item
        self.key = item.get_id()

    def is_empty(self):
        if self is Bucket.EMPTY_SINCE_START:
            return True
        return self is Bucket.EMPTY_AFTER_REMOVAL

    def is_emtpy_since_start(self):
        return self is Bucket.EMPTY_SINCE_START

    def is_empty_after_removal(self):
        return self is Bucket.EMPTY_AFTER_REMOVAL

    def get_id(self):
        return self.key

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
        pass

    def remove(self, key):
        pass

    def resize(self):
        pass