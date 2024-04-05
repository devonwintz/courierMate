from django.test import TestCase, Client
from backendapp.tests.factories import PackageFactory, CustomerFactory, PackageCategoryFactory, PackageStatusFactory
from backendapp.models import Package
from django.urls import reverse
from rest_framework import status

class PackageViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.customer = CustomerFactory()
        self.package_category = PackageCategoryFactory()
        self.package_status = PackageStatusFactory()
        self.initial_packages = PackageFactory.create_batch(5)

    def _get_package_detail_url(self, package_id):
        return reverse('package-detail', kwargs={'id': package_id})

    def test_package_list_GET_status(self):
        response = self.client.get(reverse('package-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_package_list_GET_count(self):
        response = self.client.get(reverse('package-list'))
        self.assertEqual(len(response.json()['data']), len(self.initial_packages))

    def test_package_list_POST_success_status(self):
        data = {
            'customer': self.customer.id,
            'tracking_number': '12345678910',
            'category': self.package_category.id,
            'status': self.package_status.id
        }
        response = self.client.post(reverse('package-list'), data=data, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_package_list_POST_success_count(self):
        data = {
            'customer': self.customer.id,
            'tracking_number': '12345678910',
            'category': self.package_category.id,
            'status': self.package_status.id
        }
        response = self.client.post(reverse('package-list'), data=data, content_type='application/json')
        self.assertEqual(Package.objects.count(), len(self.initial_packages) + 1)

    def test_package_list_POST_success_new_package_value(self):
        data = {
            'customer': self.customer.id,
            'tracking_number': '12345678910',
            'category': self.package_category.id,
            'status': self.package_status.id
        }
        response = self.client.post(reverse('package-list'), data=data, content_type='application/json')
        new_package = Package.objects.last()
        self.assertEqual(new_package.tracking_number, '12345678910')

    def test_package_list_POST_invalid_customer_error(self):
        invalid_customer_id = 9999
        data = {
            'customer': invalid_customer_id,
            'tracking_number': '12345678910',
            'category': self.package_category.id,
            'status': self.package_status.id
        }
        response = self.client.post(reverse('package-list'), data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_package_detail_GET_success_status(self):
        response = self.client.get(self._get_package_detail_url(self.initial_packages[0].id))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_package_detail_GET_error_status(self):
        response = self.client.get(self._get_package_detail_url(9999))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_package_detail_GET_error_message(self):
        response = self.client.get(self._get_package_detail_url(9999))
        self.assertEqual(response.json().get('error'), 'Package not found')

    def test_package_detail_PUT_success_status(self):
        updated_tracking_number = '0123456789'
        data = {
            'customer': self.customer.id,
            'tracking_number': updated_tracking_number,
            'category': self.package_category.id,
            'status': self.package_status.id
        }
        response = self.client.put(self._get_package_detail_url(self.initial_packages[0].id), data=data, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_package_detail_PUT_success_updated_value(self):
        updated_tracking_number = '0123456789'
        data = {
            'customer': self.customer.id,
            'tracking_number': updated_tracking_number,
            'category': self.package_category.id,
            'status': self.package_status.id
        }
        response = self.client.put(self._get_package_detail_url(self.initial_packages[0].id), data=data, content_type='application/json')
        updated_package = Package.objects.get(pk=self.initial_packages[0].id)
        self.assertEqual(updated_package.tracking_number, updated_tracking_number)

    def test_package_detail_PUT_incomplete_data_errors(self):
        # Missing customer field
        incomplete_data = {
            'tracking_number': '0123456789',
            'category': self.package_category.id,
            'status': self.package_status.id
        }
        response = self.client.put(self._get_package_detail_url(self.initial_packages[0].id), data=incomplete_data, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_package_detail_PUT_not_found_errors(self):
        invalid_package_id = 9999
        response = self.client.put(self._get_package_detail_url(invalid_package_id), data={}, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_package_detail_DELETE_success_status(self):
        response = self.client.delete(self._get_package_detail_url(self.initial_packages[0].id))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_package_detail_DELETE_not_found_error(self):
        response = self.client.delete(self._get_package_detail_url(9999))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)