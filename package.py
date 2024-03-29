# Implementation for the package object

# Initialization for the package class
class Package:
    # Constructor
    # Sets all package variables:
    # ID, Address, City, State, Zip Code, Delivery Deadline, Mass KILO, Special Notes, and Status.
    # O(1)
    def __init__(self, package_id, address, city, state, postal, deadline, mass, notes, status):
        self.package_id = package_id
        self.address = address
        self.city = city
        self.state = state
        self.postal = postal
        self.deadline = deadline
        self.mass = mass
        self.notes = notes
        self.status = status

    # Status update class to set package object to delivered.
    # Takes a string parameter for the delivery time.
    # O(1)
    def set_delivered(self, time):
        # Sets status to delivered including the time
        self.status = 'Delivered at ' + time

    # Status update class to set package object to en route.
    # O(1)
    def set_en_route(self):
        self.status = 'En Route'

    # Get address function
    # O(1)
    def get_address(self):
        return self.address

    # Intended for package #9 when the address can finally update at 10:20
    # O(1)
    def set_address(self):
        self.address = '410 S State St'
        self.postal = '84111'

    # Print to the user interface the package data.
    # O(1)
    def print_package(self):
        print('ID:', self.package_id, '  Address:', self.address, '  City:', self.city, '  State:', self.state,
              '  Zip:', self.postal, '  Delivery Deadline:', self.deadline, '  Mass KILO:', self.mass,
              '  Special Notes:', self.notes, '  Delivery Status:', self.status)

