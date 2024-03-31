from django.test import TestCase
from django.urls import reverse, resolve
from backendapp import views

class InvoiceURLTest(TestCase):
    def test_invoice_list_url(self):
        url = reverse('invoice-list')
        self.assertEqual(url, '/invoices/')

    def test_invoice_list_url_resolve_to_correct_view(self):
        url = reverse('invoice-list')
        resolver_match = resolve(url)
        self.assertEqual(resolver_match.func.view_class, views.InvoiceList)

    def test_invoice_detail_url(self):
        invoice_id = 1
        url = reverse('invoice-detail', args=[invoice_id])
        self.assertEqual(url, f"/invoices/{invoice_id}/")

    def test_invoice_detail_resolves_to_correct_view(self):
        invoice_id = 1
        url = reverse('invoice-detail', args=[invoice_id])
        resolver_match = resolve(url)
        self.assertEqual(resolver_match.func.view_class, views.InvoiceDetail)
