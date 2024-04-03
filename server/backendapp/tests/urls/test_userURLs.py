from django.test import TestCase
from django.urls import reverse, resolve
from backendapp import views

class UserURLTest(TestCase):
    def test_user_list_url(self):
        url = reverse('user-list')
        self.assertEqual(url, '/users/')

    def test_user_list_url_resolve_to_correct_view(self):
        url = reverse('user-list')
        resolver_match = resolve(url)
        self.assertEqual(resolver_match.func.view_class, views.UserList)

    def test_user_detail_url(self):
        user_id = 1
        url = reverse('user-detail', args=[user_id])
        self.assertEqual(url, f"/users/{user_id}/")

    def test_user_detail_resolves_to_correct_view(self):
        user_id = 1
        url = reverse('user-detail', args=[user_id])
        resolver_match = resolve(url)
        self.assertEqual(resolver_match.func.view_class, views.UserDetail)
