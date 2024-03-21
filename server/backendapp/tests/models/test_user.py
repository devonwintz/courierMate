from django.test import TestCase
from backendapp.models import User
from backendapp.tests.factories import UserFactory

class UserTest(TestCase):
    def test_string_representation(self):
        user = UserFactory()
        expected_str = user.email
        actual_str = str(user)
        self.assertEqual(actual_str, expected_str)

    def test_create_user(self):
        user = User.objects.create_user(first_name='John', last_name='Doe', email='john@example.com', password='test123')
        self.assertEqual(user.email, 'john@example.com')
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
        self.assertFalse(user.is_active)
        self.assertTrue(user.check_password('test123'))

    def test_create_superuser(self):
        superuser = User.objects.create_superuser(first_name='Admin', last_name='User', email='admin@example.com', password='admin123')
        self.assertEqual(superuser.email, 'admin@example.com')
        self.assertTrue(superuser.is_staff)
        self.assertTrue(superuser.is_superuser)
        self.assertTrue(superuser.is_active)
        self.assertTrue(superuser.check_password('admin123'))
