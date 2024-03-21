from django.test import TestCase
from backendapp.tests.factories import PackageStatusFactory

class PackageStatusTest(TestCase):
    def test_string_representation(self):
        package_status = PackageStatusFactory()
        expected_str = str(package_status.name)
        actual_str = str(package_status)
        self.assertEqual(actual_str, expected_str)
