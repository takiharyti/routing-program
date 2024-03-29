# Implementation for the truck object

# Initialization for the truck class
class Truck:
    # Constructor
    # Sets all truck object variables.
    # Sets a list for packages in the truck.
    # O(1)
    def __init__(self, location):
        self.mileage = 0
        self.location = location
        self.size = 16
        self.packages = []
        self.driver = False
        self.miles_left = 0.0
        self.time = 800.0

    # Changes all the packages on the truck to en route.
    # O(n)
    def en_route(self, all_package_hashtable):
        # Iterates through each package in the truck.
        for package in range(0, len(self.packages)):
            # Pulls the package, sets package status to en route
            package = all_package_hashtable.get(self.packages[package])
            package.set_en_route()

    # Uses the distance to find the time that has passed and the delivery time.
    # Parameters of distance and the hashtable.
    # O(n)
    def delivered(self, distance, all_package_hashtable):
        # The decimal amount of time that had passed since the last delivery.
        time_passed_decimal = distance / 18
        # Converting decimal to hours and minutes.
        time_passed_hour = int(time_passed_decimal) * 100
        time_passed_minutes = int((time_passed_decimal % 1) * 60)
        # Adding the time passed to the "current" time.
        self.time += time_passed_hour + time_passed_minutes
        # Adding an hour if minutes are over 60.
        if self.time % 100 >= 60:
            self.time += 40
        # Simplifying the time and breaking it up into hours and minutes for setting delivery time.
        raw_time = int(self.time)
        minute = int(raw_time % 100)
        hour = int((raw_time-minute) / 100)
        # Looping through each package in the truck's list.
        for item in self.packages:
            # Pulls each package and compares current location with packages.
            package = all_package_hashtable.get(item)
            # Checking for a matching address at the truck's current location.
            if package.get_address() == self.location:
                # Updating the status to delivered, including a time, and removing the package from the list.
                package.set_delivered(str(hour)+':'+str(minute).zfill(2))
                self.packages.remove(item)

