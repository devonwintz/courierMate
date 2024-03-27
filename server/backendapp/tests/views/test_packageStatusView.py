from django.test import TestCase, Client
from backendapp.tests.factories import PackageStatusFactory
from backendapp.models import PackageStatus
from django.urls import reverse
from rest_framework import status

class PackageStatusViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.initial_package_statuses = PackageStatusFactory.create_batch(5)

    def _get_package_status_detail_url(self, package_status_id):
        return reverse('package-status-detail', kwargs={'id': package_status_id})

    def test_package_status_list_GET_status(self):
        response = self.client.get(reverse('package-status-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_package_status_list_GET_count(self):
        response = self.client.get(reverse('package-status-list'))
        self.assertEqual(len(response.json()['data']), len(self.initial_package_statuses))

    def test_package_status_list_POST_success_status(self):
        data = {
            'name': 'Available for pickup'
        }
        response = self.client.post(reverse('package-status-list'), data=data, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_package_status_list_POST_success_count(self):
        data = {
            'name': 'Available for pickup'
        }
        response = self.client.post(reverse('package-status-list'), data=data, content_type='application/json')
        self.assertEqual(PackageStatus.objects.count(), len(self.initial_package_statuses) + 1)

    def test_package_status_list_POST_success_new_package_status_value(self):
        data = {
            'name': 'Available for pickup'
        }
        response = self.client.post(reverse('package-status-list'), data=data, content_type='application/json')
        new_package_status = PackageStatus.objects.last()
        self.assertEqual(new_package_status.name, 'Available for pickup')

    def test_package_status_list_POST_incomplete_data_error(self):
        incomplete_data = {}
        response = self.client.post(reverse('package-status-list'), data=incomplete_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_package_status_detail_GET_success_status(self):
        response = self.client.get(self._get_package_status_detail_url(self.initial_package_statuses[0].id))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_package_status_detail_GET_error_status(self):
        invalid_package_status = 9999
        response = self.client.get(self._get_package_status_detail_url(invalid_package_status))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_package_status_detail_GET_error_message(self):
        invalid_package_status = 9999
        response = self.client.get(self._get_package_status_detail_url(invalid_package_status))
        self.assertEqual(response.json().get('error'), 'Package status not found')

    def test_package_status_detail_PUT_success_status(self):
        updated_name = 'Delivered'
        data = {
            'name': updated_name
        }
        response = self.client.put(self._get_package_status_detail_url(self.initial_package_statuses[0].id), data=data, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_package_status_detail_PUT_success_updated_value(self):
        updated_name = 'Delivered'
        data = {
            'name': updated_name
        }
        response = self.client.put(self._get_package_status_detail_url(self.initial_package_statuses[0].id), data=data, content_type='application/json')
        updated_package_status = PackageStatus.objects.get(pk=self.initial_package_statuses[0].id)
        self.assertEqual(updated_package_status.name, updated_name)

    def test_package_status_detail_PUT_incomplete_data_error(self):
        incomplete_data = {}
        response = self.client.put(self._get_package_status_detail_url(self.initial_package_statuses[0].id), data=incomplete_data, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_package_status_detail_PUT_not_found_error(self):
        invalid_package_status = 9999
        response = self.client.put(self._get_package_status_detail_url(invalid_package_status), data={}, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_package_status_detail_DELETE_success_status(self):
        response = self.client.delete(self._get_package_status_detail_url(self.initial_package_statuses[0].id))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_package_status_detail_DELETE_not_found_error(self):
        response = self.client.delete(self._get_package_status_detail_url(9999))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
