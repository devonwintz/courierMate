from django.test import TestCase
from backendapp.tests.factories import PackageFactory

class PackageTest(TestCase):
    def test_string_representation(self):
        package = PackageFactory()
        expected_str = str(package.tracking_number)
        actual_str = str(package)
        self.assertEqual(actual_str, expected_str)
