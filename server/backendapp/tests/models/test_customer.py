from django.test import TestCase
from backendapp.models import Customer
from backendapp.tests.factories import CustomerFactory

class CustomerTest(TestCase):
    def test_string_representation(self):
        customer = CustomerFactory()
        expected_str = f"{customer.first_name} {customer.last_name}"
        actual_str = str(customer)
        self.assertEqual(actual_str, expected_str)
