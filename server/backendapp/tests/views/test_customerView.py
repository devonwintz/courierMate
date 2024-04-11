from django.test import TestCase, Client
from backendapp.tests.factories import CustomerFactory, UserFactory
from backendapp.models import Customer
from django.urls import reverse
from rest_framework import status
from unittest.mock import patch

class CustomerViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = UserFactory()
        self.initial_customers = CustomerFactory.create_batch(5)

    def _get_customer_detail_url(self, customer_id):
        return reverse('customer-detail', kwargs={'id': customer_id})

    def test_customer_list_GET_status(self):
        response = self.client.get(reverse('customer-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_customer_list_GET_count(self):
        response = self.client.get(reverse('customer-list'))
        self.assertEqual(len(response.json()['data']), len(self.initial_customers))

    def test_customer_list_GET_exception_handling(self):
        with patch('backendapp.models.Customer.objects.all') as mock_get_customers:
            mock_get_customers.side_effect = Exception("Test Exception")
            response = self.client.get(reverse('customer-list'))
            self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)
            self.assertEqual(response.data['status'], 'error')
            self.assertEqual(response.data['error'], 'Failed to retrieve customers')

    def test_customer_list_POST_success_status(self):
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

    def test_customer_list_POST_success_count(self):
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
        self.assertEqual(Customer.objects.count(), len(self.initial_customers) + 1)

    def test_customer_list_POST_success_new_customer_value(self):
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
        new_customer = Customer.objects.last()
        self.assertEqual(new_customer.email, 'jdoe@example.com')

    def test_customer_list_POST_bad_request_error(self):
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

    def test_customer_list_POST_duplicate_email_error(self):
        data = {
            'user': self.user.id,
            'first_name': 'Jane',
            'last_name': 'Doe',
            'telephone': '5921234567',
            'email': 'jdoe@example.com',
            'email_verified': True,
            'notification_opted_in': True
        }
        self.client.post(reverse('customer-list'), data=data)
        # Attempt to create another customer with the same email address
        response = self.client.post(reverse('customer-list'), data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        error_message = response.json().get('error', {}).get('email', [])[0]
        self.assertIn("email already exists.", error_message)

    def test_customer_list_POST_exception_handling(self):
        with patch('backendapp.serializers.CreateCustomerSerializer.save') as mock_save:
            mock_save.side_effect = Exception("Test Exception")
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
            self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)
            self.assertEqual(response.data['status'], 'error')
            self.assertEqual(response.data['error'], 'Failed to create customer')

    def test_customer_detail_GET_success_status(self):
        response = self.client.get(self._get_customer_detail_url(self.initial_customers[0].id))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_customer_detail_GET_error_status(self):
        response = self.client.get(self._get_customer_detail_url(9999))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_customer_detail_GET_error_message(self):
        response = self.client.get(self._get_customer_detail_url(9999))
        self.assertEqual(response.json().get('error'), 'Customer not found')

    def test_customer_detail_GET_exception_handling(self):
        with patch('backendapp.models.Customer.objects.get') as mock_get_customer:
            mock_get_customer.side_effect = Exception("Test Exception")
            response = self.client.get(self._get_customer_detail_url(self.initial_customers[0].id))
            self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)
            self.assertEqual(response.data['status'], 'error')
            self.assertEqual(response.data['error'], 'Failed to retrieve customer details')

    def test_customer_detail_PUT_success_status(self):
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

    def test_customer_detail_PUT_success_updated_value(self):
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
        updated_customer = Customer.objects.get(pk=self.initial_customers[0].id)
        self.assertEqual(updated_customer.email, updated_email)

    def test_customer_detail_PUT_not_found_error(self):
        invalid_customer_id = 9999
        response = self.client.put(self._get_customer_detail_url(invalid_customer_id), data={}, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_customer_detail_PUT_bad_request_error(self):
        invalid_updated_email = 'example.com'
        data = {
            'email': invalid_updated_email
        }
        response = self.client.put(self._get_customer_detail_url(self.initial_customers[0].id), data=data, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_customer_detail_PUT_exception_handling(self):
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
        with patch('backendapp.serializers.UpdateCustomerSerializer.save') as mock_save:
            mock_save.side_effect = Exception("Test Exception")
            response = self.client.put(self._get_customer_detail_url(self.initial_customers[0].id), data=data, content_type='application/json')
            self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)
            self.assertEqual(response.data['status'], 'error')
            self.assertEqual(response.data['error'], 'Failed to update customer details')

    def test_customer_detail_DELETE_success_status(self):
        response = self.client.delete(self._get_customer_detail_url(self.initial_customers[0].id))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_customer_detail_DELETE_not_found_error(self):
        response = self.client.delete(self._get_customer_detail_url(9999))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_customer_detail_DELETE_exception_handling(self):
        with patch('backendapp.models.Customer.delete') as mock_delete:
            mock_delete.side_effect = Exception("Test Exception")
            response = self.client.delete(self._get_customer_detail_url(self.initial_customers[0].id))
            self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)
            self.assertEqual(response.data['status'], 'error')
            self.assertEqual(response.data['error'], 'Failed to delete customer')
