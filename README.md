# WGUPS Application
*A WMS (Warehouse Management System) created for WGU's C950 Task Two PA.*

When starting this project, the focus was to develop an understanding of different Data Structures
and Algorithms, hence the name of the class. However, my attempt was to take it slightly further.


Because the class is heavily function based, I decided to challenge myself and deviate away from OOP
(Object-Oriented Programming), and practice FP (Functionality Programming). By doing so, I minimized
the number of classes that I used down to only 3 (okay, more if you consider the empty bucket/enum classes).

For the purpose of this assignment, that is besides the point, so here is a quick documentation of where everything
is and how the program flows:

---
### SECTION A
*THE HASH TABLE*

There are two files that build this: packages.py and hashtable.py. The packages.py file is where the buckets are created
and the hashtable.py is what initiates and stores items into a hash table. However, first the items must be hashed (located
in package.py line 40):

    def hash(package: Package):
        return package.id

Because each package has a unique ID, there is no need to hash in any other way than a direct hash. 

Now that we have our hash function, the insertion function is on the hashtable.py file starting at line: 47.

    def insert(self, package: Package):
        for i in range(self.size):
            index = (hash(package) + i + i * i) % self.size
            if self.table[index].is_empty():
                self.table[index] = package
                return
        self.resize(package)

You will note, the insertion algorithm here uses a quadratic probing method that will continuously search for an empty
bucket to place the package in. If none is found, that is where self.resize() is called to resize the hash table.

---
### SECTION B
*THE LOOKUP FUNCTION*

This function is located at line 31 in the hashtable.py file. To look up items, we simply execute the same quadratic function
to find the bucket:

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

However, the difference here is the use of EMPTY_SINCE_START vs. EMPTY_AFTER_REMOVAL.
These were created using a helper class and initializing them with those two attributes.

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

    PackageBucket.EMPTY_SINCE_START = PackageBucket()
    PackageBucket.EMPTY_AFTER_REMOVAL = PackageBucket()

Because we used this, instead of creating a separate list to store which buckets are empty, and to prevent
issues with functionality, we can instead initialize the entire hash table with PackageBucket.EMPTY_SINCE_START object,
and insert PackageBucket.EMPTY_AFTER_REMOVAL whenever something is removed from the table.

    def __init__(self, initial_size: int = 40):
        self.table = [PackageBucket.EMPTY_SINCE_START] * initial_size
        self.size = initial_size

---
### SECTION C
*THE ORIGINAL PROGRAM*

Here is where things were a little complicated. With the challenge as mentioned above, the only other class that was used
was the Truck class. Given my experience as an e-Commerce Warehouse Coordinator on both the shipping and receiving ends,
I used my experience working with our systems to develop one that is similar in aspects.

##### Receiving:

The first thing that needed to happen was receiving each of the packages. That was done simply by using python's CSV reader:

    def receive_package():
        with open("packages.csv", "r") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                package = Package(row['id'], row['address'], row['city'], row['state'], row['zipcode'], row['delivery_deadline'], row['weight'], row['notes'])
                handle_package(package)
                wgups_table.insert(package)

Note that first the package is created in the package class, then handled, then inserted into the wpups_table (an instance of
our Hash Table used for this application). The second portion of handling allows for special notes to be taken care of, 
standardizing data types, and finally sorting the package ID's into specific sets based on specific conditions. This 
follows the same SOP (standard operating procedure) for traditional warehousing via receive, sort, and putaway. 

##### Shipping:

After the packages have been received, sorted, and putaway (inserted into the hash table), now the manifests and routes are 
ready to be built. 