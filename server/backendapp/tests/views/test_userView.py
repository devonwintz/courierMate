from django.test import TestCase, Client
from backendapp.tests.factories import UserFactory
from backendapp.models import User
from django.urls import reverse
from rest_framework import status

class UserViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.initial_users_count = 2  # Initial users created below
        self.user = User.objects.create_user(
            first_name='John',
            last_name='Doe',
            email='john@example.com',
            password='password123'
        )
        self.superuser = User.objects.create_superuser(
            first_name='Admin',
            last_name='User',
            email='admin@example.com',
            password='adminpassword'
        )

    def _get_user_detail_url(self, user_id):
        return reverse('user-detail', kwargs={'id': user_id})

    def test_user_list_GET_status(self):
        response = self.client.get(reverse('user-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_list_GET_count(self):
        response = self.client.get(reverse('user-list'))
        self.assertEqual(len(response.json()['data']), self.initial_users_count)

    def test_user_list_POST_success_status(self):
        data = {
            'first_name': 'James',
            'last_name': 'Smith',
            'email': 'james@example.com',
            'password': 'password123'
        }
        response = self.client.post(reverse('user-list'), data=data, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_user_list_POST_success_count(self):
        data = {
            'first_name': 'James',
            'last_name': 'Smith',
            'email': 'james@example.com',
            'password': 'password123'
        }
        response = self.client.post(reverse('user-list'), data=data, content_type='application/json')
        self.assertEqual(User.objects.count(), self.initial_users_count + 1)

    def test_user_list_POST_success_new_user_value(self):
        data = {
            'first_name': 'Mark',
            'last_name': 'Wayne',
            'email': 'mwayne@example.com',
            'password': 'drowssap321'
        }
        response = self.client.post(reverse('user-list'), data=data, content_type='application/json')
        new_user = User.objects.last()
        self.assertEqual(new_user.email, 'mwayne@example.com')

    def test_user_list_POST_duplicate_email_error(self):
        data = {
            'first_name': 'Mark',
            'last_name': 'Wayne',
            'email': 'mwayne@example.com',
            'password': 'drowssap321'
        }
        self.client.post(reverse('user-list'), data=data)
        # Attempt to create another user with the same email address (username)
        response = self.client.post(reverse('user-list'), data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        error_message = response.json().get('error', {}).get('email', [])[0]
        self.assertIn("email already exists.", error_message)

    def test_user_detail_GET_success_status(self):
        response = self.client.get(self._get_user_detail_url(self.user.id))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_detail_GET_error_status(self):
        user_id = 9999
        response = self.client.get(self._get_user_detail_url(user_id))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_user_detail_GET_error_message(self):
        user_id = 9999
        response = self.client.get(self._get_user_detail_url(user_id))
        self.assertEqual(response.json().get('error'), 'User not found')

    def test_user_detail_PUT_success_status(self):
        updated_email = 'johndoe@example.com'
        data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'email': updated_email,
        }
        response = self.client.put(self._get_user_detail_url(self.user.id), data=data, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_detail_PUT_success_updated_value(self):
        updated_email = 'johndoe@example.com'
        data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'email': updated_email,
        }
        response = self.client.put(self._get_user_detail_url(self.user.id), data=data, content_type='application/json')
        updated_user = User.objects.get(pk=self.user.id)
        self.assertEqual(updated_user.email, updated_email)

    def test_user_detail_PUT_incomplete_data_error(self):
        incomplete_data = {
        }
        response = self.client.put(self._get_user_detail_url(self.user.id), data=incomplete_data, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_detail_PUT_not_found_error(self):
        invalid_user_id = 9999
        response = self.client.put(self._get_user_detail_url(invalid_user_id), data={}, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_user_detail_DELETE_success_status(self):
        response = self.client.delete(self._get_user_detail_url(self.user.id))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_user_detail_DELETE_not_found_error(self):
        invalid_user_id = 9999
        response = self.client.delete(self._get_user_detail_url(invalid_user_id))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

