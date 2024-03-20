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

# class PackageCategoryFactory(factory.django.DjangoModelFactory):
#     class Meta:
#         model = PackageCategory

#     name = "test"

# class PackageStatusFactory(factory.django.DjangoModelFactory):
#     class Meta:
#         model = PackageStatus
#     name = "test"

# class PackageFactory(factory.django.DjangoModelFactory):
#     class Meta:
#         model = Package

#     customer = factory.SubFactory(PackageFactory)
#     tracking_number = '123'
#     category = factory.SubFactory(PackageCategoryFactory)
#     date_delivered
#     date_shipped
#     expected_delivery_date
#     status = factory.SubFactory(PackageStatusFactory)
#     weight
#     length
#     width
#     height
