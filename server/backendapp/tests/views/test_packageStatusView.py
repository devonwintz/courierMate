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

    def test_package_status_list_GET(self):
        response = self.client.get(reverse('package-status-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()['data']), len(self.initial_package_statuses))

    def test_package_status_list_POST_success(self):
        data = {
            'name': 'Available for pickup'
        }
        response = self.client.post(reverse('package-status-list'), data=data, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(PackageStatus.objects.count(), len(self.initial_package_statuses) + 1)
        new_package_status = PackageStatus.objects.last()
        self.assertEqual(new_package_status.name, 'Available for pickup')

    def test_package_status_list_POST_error(self):
        # Test incomplete data (400 Error)
        incomplete_data = {}
        response = self.client.post(reverse('package-status-list'), data=incomplete_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_package_status_detail_GET_success(self):
        response = self.client.get(self._get_package_status_detail_url(self.initial_package_statuses[0].id))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_package_status_detail_GET_error(self):
        response = self.client.get(self._get_package_status_detail_url(9999))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.json().get('error'), 'Package status not found')

    def test_package_status_detail_PUT_success(self):
        updated_name = 'Delivered'
        data = {
            'name': updated_name
        }
        response = self.client.put(self._get_package_status_detail_url(self.initial_package_statuses[0].id), data=data, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        updated_package_status = PackageStatus.objects.get(pk=self.initial_package_statuses[0].id)
        self.assertEqual(updated_package_status.name, updated_name)

    def test_package_status_detail_PUT_errors(self):
        # Test incomplete data (400 Error)
        incomplete_data = {}
        response = self.client.put(self._get_package_status_detail_url(self.initial_package_statuses[0].id), data=incomplete_data, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Test invalid package status ID (404 Error)
        response = self.client.put(self._get_package_status_detail_url(9999), data={}, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_package_status_detail_DELETE_success(self):
        response = self.client.delete(self._get_package_status_detail_url(self.initial_package_statuses[0].id))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_package_status_detail_DELETE_error(self):
        response = self.client.delete(self._get_package_status_detail_url(9999))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
