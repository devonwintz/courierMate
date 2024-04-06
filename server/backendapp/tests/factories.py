import random
import factory
from django.contrib.auth.models import User
from backendapp.models import *
from factory.faker import Faker

class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    first_name = Faker("first_name")
    last_name = Faker("last_name")
    email = Faker("email")

class CustomerFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Customer

    user = factory.SubFactory(UserFactory)
    first_name = Faker("first_name")
    last_name = Faker("last_name")
    telephone = Faker('phone_number')
    email = Faker('email')

class PackageCategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = PackageCategory

    name = Faker('random_element', elements=[
        "Electronic/Computer", "Clothing", "Books", "Home Appliances",
        "Toys", "Food", "Health & Beauty", "Furniture", "Sports Equipment",
        "Jewelry", "Office Supplies", "Art & Crafts", "Automotive",
        "Musical Instruments", "Pet Supplies", "Baby Products",
        "Outdoor Gear", "Stationery", "Electrical Supplies",
        "Gardening Supplies", "Kitchenware", "Travel Accessories",
        "Party Supplies", "Fitness Gear", "Tools & Hardware",
        "Gifts & Decor", "School Supplies", "Collectibles"
    ])

class PackageStatusFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = PackageStatus

    name = Faker('random_element', elements=[
        "Shipment Created", "In Transit", "Out for Delivery", "Delivered",
        "Exception", "Returned to Sender", "Pending", "On Hold",
        "Arrived at Sort Facility", "Departed Sort Facility",
        "Customs Processing", "Arrived at Destination", "Sorting Complete",
        "Awaiting Pickup", "Delayed", "Cancelled", "Lost", "Damaged",
        "Refused", "On Route to Pickup", "In Customs", "Out for Shipment",
        "Redirected", "Arrived at Pickup Point", "Ready for Pickup",
        "Picked Up"
    ])

class PackageFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Package

    customer = factory.SubFactory(CustomerFactory)
    tracking_number = Faker('numerify', text='##############')
    category = factory.SubFactory(PackageCategoryFactory)
    date_delivered_ny = Faker('date_this_year')
    date_arrived_gy = Faker('date_this_year')
    date_shipped = Faker('date_this_year')
    expected_delivery_date = Faker('date_between', start_date='today', end_date='+30d')
    status = factory.SubFactory(PackageStatusFactory)
    weight = Faker('random_number', digits=2)
    length = Faker('random_number', digits=2)
    width = Faker('random_number', digits=2)
    height = Faker('random_number', digits=2)

class InvoiceFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Invoice

    customer = factory.SubFactory(CustomerFactory)
    package = factory.SubFactory(PackageFactory)
    price = Faker('random_number', digits=7)
