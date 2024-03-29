# Tenny Akihary
# Main for user input and implementing each file

# Imports
import csv
from hash import *
from package import *
from truck import *

# Call and assignment of the user input. Breaking only when an acceptable input is made.
# 0(1)
while True:
    # Prompt user input
    print('Enter a four digit time (in military time) throughout this day\'s delivery process (e.g., HHMM 1300): ')
    desired_time = input("Enter time: ")
    # Try and except for non integer values.
    try:
        # Get integer value.
        desired_time = int(desired_time)
        # If the minute is correct.
        if (desired_time % 100) < 60:
            # If under 2400 break.
            if desired_time < 2400:
                break
        # Prompt error and try user input again.
        print('ERROR: Hour must be from 00 to 23 and minute 00 to 59')
    # Except a value error if anything but digits are entered and send prompt to user.
    except ValueError:
        print('ERROR: Make sure you are using proper formatting and try again.')

# Get the amount of hours after the trucks may leave (800)
minute = desired_time % 100
hours = (desired_time - minute - 800)/100
hours = hours + (minute/60)

# Only two trucks can drive at the same time.
# Therefore, two drivers can drive the same amount of miles from 8:00AM to whatever given time.
total_miles = hours * 18

# Special case, truck 1 will wait until 9:05 before beginning delivery to complete the delayed packages with deadlines.
# Five minutes will be subtracted, and instead of subtracting the military time by 800, it will be 900.
minute = minute - 5
hours = (desired_time - minute - 900)/100
hours = hours + (minute/60)
truck1_miles = hours * 18

# Function for loading the packages into a hashtable.
# Package format in csv: "Package ID",Address,City,State,Zip,"Delivery Deadline","Mass KILO", "Special Notes"
# O(n)
def load_package_data(filename):
    with open(filename) as all_packages:
        package_data = csv.reader(all_packages, delimiter=',')
        # To skip the header.
        next(package_data)
        for PACKAGE in package_data:
            package_id = PACKAGE[0]
            package_address = PACKAGE[1]
            package_city = PACKAGE[2]
            package_state = PACKAGE[3]
            package_zip = PACKAGE[4]
            package_deadline = PACKAGE[5]
            package_mass = PACKAGE[6]
            package_notes = PACKAGE[7]
            # Create package object, set status "AT HUB" and insert into hashtable.
            package_object = Package(package_id, package_address, package_city, package_state, package_zip,
                                     package_deadline, package_mass, package_notes, "AT HUB")
            all_packages_hashtable.add(package_id, package_object)


# Instantiate package hashtable and load package data table.
all_packages_hashtable = MyHashTable()
load_package_data("Resources/Package File.csv")


# Function for loading the distance table into a dictionary.
# Follows
# O(n)
def load_distance_data(filename):
    with open(filename) as all_distances:
        distance_data = csv.reader(all_distances, delimiter=',')
        # Set row index in all distance data to follow 1-27
        row_index = 0
        # Iterate through each line in the file
        for distance in distance_data:
            # Store values using dictionary.
            # Index (row or column) for each location corresponds to each line in the distance table -1.
            all_distance_data[row_index] = [distance[2], distance[3], distance[4], distance[5], distance[6],
                                              distance[7], distance[8], distance[9], distance[10], distance[11],
                                              distance[12], distance[13], distance[14], distance[15], distance[16],
                                              distance[17], distance[18], distance[19], distance[20], distance[21],
                                              distance[22], distance[23], distance[24], distance[25], distance[26],
                                              distance[27], distance[28]]
            row_index += 1
            # Add address data to list of addresses.
            address_data.append(distance[1])


# Define distance dictionary and address variables and load the distance data table.
all_distance_data = {}
address_data = []
load_distance_data('Resources/Distance Table.csv')

# Function to return the distance between two addresses.
# O(1)
def distance_between(address1, address2):
    # If the second address index is larger than the first.
    if address_data.index(address1) < address_data.index(address2):
        # Return the distance data for [address 2 index] [address 1 index].
        return float(all_distance_data[address_data.index(address2)][address_data.index(address1)])
    # Return the distance data for [address 1 index] [address 2 index].
    return float(all_distance_data[address_data.index(address1)][address_data.index(address2)])


# Instantiate the trucks.
# Set driver status, time departed, and miles left.
truck1 = Truck('4001 South 700 East')
truck1.driver = True
truck1.miles_left = truck1_miles
truck2 = Truck('4001 South 700 East')
truck2.driver = True
truck2.miles_left = total_miles
truck3 = Truck('4001 South 700 East')


# Manually loading truck 1 with delayed flight and delivery deadline.
truck1.packages = ['6', '25', '26', '28', '31', '32']
# Manually loading truck 2 with delivery deadlines but no delayed flights.
truck2.packages = ['1', '3', '13', '14', '15', '16', '18', '19', '20', '29', '30', '34', '36', '37', '38', '40']
# Truck 3 gets the delayed packages since there are only 2 drivers.
# By the time another driver makes it back with their initial deliveries the delayed packages will arrive.
# Manually loading truck 3.
truck3.packages = ['2', '4', '5', '7', '8', '10', '11', '12', '17', '21', '22', '23', '24', '27', '33', '35']


# Function to find the closest address from the trucks current location.
# Parameters are the address in string and the truck object.
# O(n)
def find_closest_address(truck):
    # Closest address being compared is where the truck currently resides.
    closest_address = truck.location
    shortest_distance = 100.0
    # Iterate through the list of packages.
    for i in range(0, len(truck.packages)):
        # Pull the package at the index from the hashtable.
        pkg = all_packages_hashtable.get(truck.packages[i])
        # Check the distance between is less than the smallest distance.
        if distance_between(truck.location, pkg.get_address()) < shortest_distance:
            # Save address to closest_address.
            closest_address = pkg.get_address()
            # Save the shortest distance.
            shortest_distance = distance_between(truck.location, pkg.get_address())
    return closest_address


# Method to deliver packages.
# Iterates through each package and calls the truck.delivered which is O(n) for each case.
# O(n^2)
def deliver_packages(truck):
    # While loop to run while there are packages or miles left.
    while len(truck.packages) != 0 and truck.miles_left > 0:
        # Call the function to find the closest address and get the distance.
        closest_address = find_closest_address(truck)
        distance = distance_between(closest_address, truck.location)
        # Check if there are any miles left for the given distance.
        if distance < truck.miles_left:
            # Subtract the distance traveled, change truck location, add the mileage, and call the delivered function.
            truck.miles_left -= distance
            truck.location = closest_address
            truck.mileage += distance
            truck.delivered(distance, all_packages_hashtable)
        else:
            # If not enough miles for the distance add the partial distance.
            truck.mileage += truck.miles_left
            truck.miles_left = 0
            break
    # Check for packages still remaining in the truck.
    if len(truck.packages) == 0 and truck.miles_left > 0:
        # Get distance from the current location and back to the hub.
        distance = distance_between(truck.location, '4001 South 700 East')
        # Check if the distance is less than the remaining miles.
        if distance < truck.miles_left:
            # Subtract distance, change location,count in mileage, and add the time difference.
            truck.miles_left -= distance
            truck.location = '4001 South 700 East'
            truck.mileage += distance
            truck.time += (distance / 18)
        else:
            # If not enough miles left to spend, add partial miles to mileage.
            truck.mileage += truck.miles_left
            truck.miles_left = 0


# If statement to check for positive hours, and deliver all the packages with time constraints.
if total_miles > 0:
    truck2.en_route(all_packages_hashtable)
    deliver_packages(truck2)

# Wait until 9:05 and deliver truck 1 if there are positive hours.
if truck1_miles > 0:
    truck1.time = 905.0
    deliver_packages(truck1)

# Check for remaining miles.
if truck1.miles_left > 0 or truck2.miles_left > 0:
    # Check for the most remaining miles.
    if truck1.miles_left > truck2.miles_left:
        # Toggle boolean for driver switching from truck 1 to truck 3.
        truck1.driver = False
        truck3.driver = True
        # Transfer allotted miles and the time.
        truck3.miles_left = truck1.miles_left
        truck3.time = truck1.time
        # Load trucks that have no delivery deadline and the package whose address updates at 1020.
        truck2.packages = ['9', '39']
        # Truck has to "wait" until 1020 to deliver these packages.
        if truck2.time < 1020.0:
            # Subtracting miles according to how long its waited.
            time_difference = 1020 - truck2.time
            truck2.time = 1020.0
            minute = time_difference % 100
            hours = (time_difference - minute)/100
            if minute > 60:
                minute = minute - 40
                hours += 1
            hours = hours + (minute / 60)
            truck2.miles_left = truck2.miles_left - (hours * 18)
        # Get package 9.
        pkg = all_packages_hashtable.get('9')
        # Update the package address.
        pkg.set_address()
        if truck2.miles_left > 0:
            deliver_packages(truck2)
    else:
        # Toggle boolean for driver switching from truck 2 to truck 3.
        truck2.driver = False
        truck3.driver = True
        # Transfer allotted miles and the time.
        truck3.miles_left = truck2.miles_left
        truck3.time = truck2.time
        # Load trucks that have no delivery deadline and the package whose address updates at 1020.
        truck1.packages = ['9', '39']
        # Truck has to "wait" until 1020 to deliver these packages.
        if truck1.time < 1020.0:
            # Subtracting miles according to how long its waited.
            time_difference = 1020 - truck1.time
            truck1.time = 1020.0
            minute = time_difference % 100
            hours = (time_difference - minute) / 100
            if minute > 60:
                minute = minute - 40
                hours += 1
            hours = hours + (minute / 60)
            truck1.miles_left = truck1.miles_left - (hours * 18)
        # Get package 9.
        pkg = all_packages_hashtable.get('9')
        # Update the package address.
        pkg.set_address()
        if truck1.miles_left > 0:
            deliver_packages(truck1)

# Check for driver before delivery
if truck3.driver:
    truck3.en_route(all_packages_hashtable)
    deliver_packages(truck3)

# Calculate the final mileage of all trucks.
final_mileage = truck3.mileage + truck2.mileage + truck1.mileage

# Ending prompt to ask for specific data.
# O(n^2)
while True:
    # Prompt user the menu for selections and user input.
    print('Menu')
    print('1: View All Package Data')
    print('2: View Specific Package')
    desired_data = input("Enter selection: ")
    # Try to catch value errors for non integer inputs
    try:
        desired_data = int(desired_data)
        # If statements to check only the two options, prompting an error if neither.
        if desired_data == 1:
            # Run and print all package data at specific time.
            for cell in range(0, all_packages_hashtable.size):
                if all_packages_hashtable.table[cell] is not None:
                    for package in all_packages_hashtable.table[cell]:
                        pkg = all_packages_hashtable.get(package[0])
                        pkg.print_package()
            print('Total mileage: ', final_mileage)
            break
        if desired_data == 2:
            # Prompt user input for specific package to be displayed at the specific time.
            desired_package = input("Enter Package ID: ")
            desired_package = int(desired_package)
            # If ID is among all the existing packages.
            if 1 <= desired_package <= 40:
                # Run and print all specific package data at specific time.
                pkg = all_packages_hashtable.get(str(desired_package))
                pkg.print_package()
                print('Total mileage: ', final_mileage)
                break
        print('ERROR: Incorrect option or Package ID. Try again.')

    # Except a value error if anything but digits are entered and send error prompt to user.
    except ValueError:
        print('ERROR: Input was not of the proper format (an integer). Try again.')
