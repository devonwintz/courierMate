from django.test import TestCase
from django.urls import reverse, resolve
from backendapp import views

class CustomerURLTest(TestCase):
    def test_customer_list_url(self):
        url = reverse('customer-list')
        self.assertEqual(url, '/customers/')

    def test_customer_list_url_resolve_to_correct_view(self):
        url = reverse('customer-list')
        resolver_match = resolve(url)
        self.assertEqual(resolver_match.func.view_class, views.CustomerList)

    def test_customer_detail_url(self):
        customer_id = 1
        url = reverse('customer-detail', args=[customer_id])
        self.assertEqual(url, f"/customers/{customer_id}/")

    def test_customer_detail_resolves_to_correct_view(self):
        customer_id = 1
        url = reverse('customer-detail', args=[customer_id])
        resolver_match = resolve(url)
        self.assertEqual(resolver_match.func.view_class, views.CustomerDetail)
