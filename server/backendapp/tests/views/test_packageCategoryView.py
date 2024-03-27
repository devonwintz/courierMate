from django.test import TestCase, Client
from backendapp.tests.factories import PackageCategoryFactory
from backendapp.models import PackageCategory
from django.urls import reverse
from rest_framework import status

class PackageCategoryViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.initial_package_categories = PackageCategoryFactory.create_batch(5)

    def _get_package_category_detail_url(self, package_category_id):
        return reverse('package-category-detail', kwargs={'id': package_category_id})

    def test_package_category_list_GET_status(self):
        response = self.client.get(reverse('package-category-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_package_category_list_GET_count(self):
        response = self.client.get(reverse('package-category-list'))
        self.assertEqual(len(response.json()['data']), len(self.initial_package_categories))

    def test_package_category_list_POST_success_status(self):
        data = {
            'name': 'Clothing'
        }
        response = self.client.post(reverse('package-category-list'), data=data, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_package_category_list_POST_success_count(self):
        data = {
            'name': 'Clothing'
        }
        response = self.client.post(reverse('package-category-list'), data=data, content_type='application/json')
        self.assertEqual(PackageCategory.objects.count(), len(self.initial_package_categories) + 1)

    def test_package_category_list_POST_success_new_package_category_value(self):
        data = {
            'name': 'Clothing'
        }
        response = self.client.post(reverse('package-category-list'), data=data, content_type='application/json')
        new_package_category = PackageCategory.objects.last()
        self.assertEqual(new_package_category.name, 'Clothing')

    def test_package_category_list_POST_incomplete_data_error(self):
        incomplete_data = {}
        response = self.client.post(reverse('package-category-list'), data=incomplete_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_package_category_detail_GET_success_status(self):
        response = self.client.get(self._get_package_category_detail_url(self.initial_package_categories[0].id))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_package_category_detail_GET_error_status(self):
        response = self.client.get(self._get_package_category_detail_url(9999))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_package_category_detail_GET_error_message(self):
        response = self.client.get(self._get_package_category_detail_url(9999))
        self.assertEqual(response.json().get('error'), 'Package category not found')

    def test_package_category_detail_PUT_success_status(self):
        updated_name = 'Health/Sports'
        data = {
            'name': updated_name
        }
        response = self.client.put(self._get_package_category_detail_url(self.initial_package_categories[0].id), data=data, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_package_category_detail_PUT_success_updated_value(self):
        updated_name = 'Health/Sports'
        data = {
            'name': updated_name
        }
        response = self.client.put(self._get_package_category_detail_url(self.initial_package_categories[0].id), data=data, content_type='application/json')
        updated_package_category = PackageCategory.objects.get(pk=self.initial_package_categories[0].id)
        self.assertEqual(updated_package_category.name, updated_name)

    def test_package_category_detail_PUT_incomplete_data_error(self):
        incomplete_data = {}
        response = self.client.put(self._get_package_category_detail_url(self.initial_package_categories[0].id), data=incomplete_data, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_package_category_detail_PUT_not_found_error(self):
        response = self.client.put(self._get_package_category_detail_url(9999), data={}, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_package_category_detail_DELETE_success_status(self):
        response = self.client.delete(self._get_package_category_detail_url(self.initial_package_categories[0].id))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_package_category_detail_DELETE_not_found_error(self):
        response = self.client.delete(self._get_package_category_detail_url(9999))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
