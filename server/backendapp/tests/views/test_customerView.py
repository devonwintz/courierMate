from django.test import TestCase, Client
from backendapp.tests.factories import CustomerFactory, UserFactory
from backendapp.models import Customer
from backendapp.serializers import CustomerSerializer
from django.urls import reverse
from rest_framework import status
from factory.faker import Faker

class CustomerViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = UserFactory()
        self.initial_customers = CustomerFactory.create_batch(5)

    def _get_customer_detail_url(self, customer_id):
        return reverse('customer-detail', kwargs={'id': customer_id})

    def test_customer_list_GET(self):
        response = self.client.get(reverse('customer-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()['data']), len(self.initial_customers))

    def test_customer_list_POST_success(self):
        data = {
            'user': self.user.id,
            'first_name': 'Jane',
            'last_name': 'Doe',
            'telephone': '5921234567',
            'email': 'jdoe@example.com',
            'email_verified': True,
            'notification_opted_in': True
        }
        response = self.client.post(reverse('customer-list'), data=data, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Customer.objects.count(), len(self.initial_customers) + 1)
        new_customer = Customer.objects.last()
        self.assertEqual(new_customer.email, 'jdoe@example.com')

    def test_customer_list_POST_error(self):
        invalid_user_id = 999
        data = {
            'user': invalid_user_id,
            'first_name': 'Jane',
            'last_name': 'Doe',
            'telephone': '5921234567',
            'email': 'jdoe@example.com',
            'email_verified': True,
            'notification_opted_in': True
        }
        response = self.client.post(reverse('customer-list'), data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_customer_detail_GET_success(self):
        response = self.client.get(self._get_customer_detail_url(self.initial_customers[0].id))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_customer_detail_GET_error(self):
        response = self.client.get(self._get_customer_detail_url(9999))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.json().get('error'), 'Customer not found')

    def test_customer_detail_PUT_success(self):
        updated_email = 'jane@example.com'
        data = {
            'user': self.user.id,
            'first_name': 'Jane',
            'last_name': 'Doe',
            'telephone': '5921234567',
            'email': updated_email,
            'email_verified': True,
            'notification_opted_in': True
        }
        response = self.client.put(self._get_customer_detail_url(self.initial_customers[0].id), data=data, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        updated_customer = Customer.objects.get(pk=self.initial_customers[0].id)
        self.assertEqual(updated_customer.email, updated_email)

    def test_customer_detail_PUT_errors(self):
        # Test incomplete data (400 Error)
        incomplete_data = {
            'first_name': 'John',
            'last_name': 'Doe'
        }
        response = self.client.put(self._get_customer_detail_url(self.initial_customers[0].id), data=incomplete_data, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Test invalid customer ID (404 Error)
        response = self.client.put(self._get_customer_detail_url(9999), data={}, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_customer_detail_DELETE_success(self):
        response = self.client.delete(self._get_customer_detail_url(self.initial_customers[0].id))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_customer_detail_DELETE_error(self):
        response = self.client.delete(self._get_customer_detail_url(9999))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

