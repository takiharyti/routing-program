# Hash implementation to hold items in a hashtable.
# References: Joe James https://www.youtube.com/watch?v=9HFbhPscPU0 and C950 - Webinar-1 - Let's Go Hashing

# Initialization of the MyHashTable class.
class MyHashTable:

    # Constructor
    # Sets the number of "columns" to 40.
    # Empties all the cells.
    # O(1)
    def __init__(self):
        # Set the size to 10.
        self.size = 40
        # Empties the cells.
        self.table = [None] * self.size

    # Add an item to the hashtable.
    # Updates the value if it already exists.
    # Key and the item as parameters to store.
    # Returns true once it has been added.
    # O(1)
    def add(self, key, item):
        # Variables to hold which cell and the key item
        cell = hash(key) % self.size
        key_item = [key, item]
        # If the cell is empty then add the key item.
        if self.table[cell] is None:
            self.table[cell] = list([key_item])
            return True
        # If the cell is not empty.
        else:
            # Check each item in the cell for the key. Update item if key is present.
            for item in self.table[cell]:
                if item[0] == key:
                    item[1] = item
                    return True
            # If no key is found in the cell, append the key item to the cell.
            self.table[cell].append(key_item)
            return True

    # Getter from the hashtable.
    # Key parameter to search within the hashmap.
    # Returns the item at the key.
    # O(1)
    def get(self, key):
        # Variable to hold which cell.
        cell = hash(key) % self.size
        # If the cell is not empty.
        if self.table[cell] is not None:
            # Check for the key in the cell. Return the item if found.
            for item in self.table[cell]:
                if item[0] == key:
                    return item[1]
        # If there is no item given the key return None.
        return None

    # Remove from the hashtable
    # Key parameter to search within the hashtable.
    # Returns true if deleted or false if not removed.
    # O(1)
    def remove(self, key):
        # Variable to hold which cell.
        cell = hash(key) % self.size

        # If the cell is not empty.
        if self.table[cell] is not None:
            # Pop the key item out of the cell if it is found.
            for index in range(0, len(self.table[cell])):
                if self.table[cell][index][0] == key:
                    self.table[cell].pop(index)
                    return True
        # Returns false if nothing deleted.
        return False
