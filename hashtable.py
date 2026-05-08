from package import Package

# Because each package has a unique id, we can use that as the hash key.
def hash(item: Package):
    return item.get_id()

# This here is a bucket class that will store the package. It is also
# used to initialize two empty buckets for hash table functionality.
class Bucket:

    def __init__(self, item: Package = None):
        self.item = item
        self.key = hash(item) if item is not None else None

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

# These are the two types of empty buckets that will be used.
Bucket.EMPTY_SINCE_START = Bucket()
Bucket.EMPTY_AFTER_REMOVAL = Bucket()

# This is the hash table class that will store the packages.
class Hashtable:

    def __init__(self, initial_size=40):
        self.table = [Bucket.EMPTY_SINCE_START] * initial_size
        self.size = initial_size

    # This is the insert function that will create a new bucket for an item, then insert
    # it into the table quadratically. If the table is full, it will resize the table
    # and then insert the item into the table.
    def insert(self, item: Package):
        bucket_item = Bucket(item)

        for i in range(self.size):
            index = (hash(item) + i + i * i) % self.size
            if self.table[index].is_empty():
                self.table[i] = bucket_item
                return

        # If we get here, the table is full and needs to be resized and then add
        # the item into the table.
        self.resize(bucket_item)

    # Here is where we will be able to grab a requested item from the table!
    # Note, because we are directly hashing the item id, we can use that as the key.
    # Also, because we are using a quadratic probing technique, we will need to
    # check each bucket via quadratic probing until the key is found, or the bucket is
    # empty since start.
    def get(self, item_id):

        for i in range(self.size):
            index = (item_id + i + i * i) % self.size
            if self.table[index].get_id() == item_id:
                return self.table[index].item
            elif self.table[index].is_emtpy_since_start():
                return None
        return None

    # This is the remove function that will remove an item from the table.
    # It will do this by checking each bucket via quadratic probing until the key is found,
    # or the bucket is empty since start. (For our purposes, this will most likely not be used.
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

    # This is the resize function that will resize the table. It will do this by
    # creating a new table with twice the size of the old table, and then inserting
    # the new bucket into the new table.
    def resize(self, new_bucket_item):
        self.size *= 2
        temp_table = [Bucket.EMPTY_SINCE_START] * self.size
        for bucket in self.table:
            if not bucket.is_empty():
                for i in range(self.size):
                    index = (bucket.get_id() + i + i * i) % self.size
                    if self.table[index].is_empty():
                        self.table[i] = bucket
                        return

        for i in range(self.size):
            index = (new_bucket_item.get_id() + i + i * i) % self.size
            if self.table[index].is_empty():
                self.table[i] = new_bucket_item
                return
        self.table = temp_table
