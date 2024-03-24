from django.test import TestCase
from backendapp.tests.factories import PackageCategoryFactory

class PackageCategoryModelTest(TestCase):
    def test_string_representation(self):
        package_category = PackageCategoryFactory()
        expected_str = str(package_category.name)
        actual_str = str(package_category)
        self.assertEqual(actual_str, expected_str)
