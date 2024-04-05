from django.test import TestCase, Client
from backendapp.tests.factories import InvoiceFactory, CustomerFactory, PackageFactory
from backendapp.models import Invoice
from django.urls import reverse
from rest_framework import status

class InvoiceViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.customer = CustomerFactory()
        self.package = PackageFactory()
        self.initial_invoices = InvoiceFactory.create_batch(5)

    def _get_invoice_detail_url(self, invoice_id):
        return reverse('invoice-detail', kwargs={'id': invoice_id})

    def test_invoice_list_GET_status(self):
        response = self.client.get(reverse('invoice-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_invoice_list_GET_count(self):
        response = self.client.get(reverse('invoice-list'))
        self.assertEqual(len(response.json()['data']), len(self.initial_invoices))

    def test_invoice_list_POST_success_status(self):
        data = {
            'customer': self.customer.id,
            'package': self.package.id,
            'price': 20.00
        }
        response = self.client.post(reverse('invoice-list'), data=data, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_invoice_list_POST_success_count(self):
        data = {
            'customer': self.customer.id,
            'package': self.package.id,
            'price': 20.00
        }
        response = self.client.post(reverse('invoice-list'), data=data, content_type='application/json')
        self.assertEqual(Invoice.objects.count(), len(self.initial_invoices) + 1)

    def test_invoice_list_POST_error_status(self):
        invalid_customer_id = 999
        data = {
            'customer': invalid_customer_id,
            'package': self.package.id,
            'price': 20.00
        }
        response = self.client.post(reverse('invoice-list'), data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_invoice_detail_GET_success_status(self):
        response = self.client.get(self._get_invoice_detail_url(self.initial_invoices[0].id))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_invoice_detail_GET_invalid_invoice_error_status(self):
        invalid_invoice_id = 999
        response = self.client.get(self._get_invoice_detail_url(invalid_invoice_id))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_invoice_detail_GET_invalid_invoice_error_message(self):
        invalid_invoice_id = 999
        response = self.client.get(self._get_invoice_detail_url(invalid_invoice_id))
        self.assertEqual(response.json().get('error'), 'Invoice not found')

    def test_invoice_detail_PUT_success_status(self):
        updated_price = 40.00
        data = {
            'customer': self.customer.id,
            'package': self.package.id,
            'price': updated_price
        }
        response = self.client.put(self._get_invoice_detail_url(self.initial_invoices[0].id), data=data, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_invoice_detail_PUT_success_updated_value(self):
        updated_price = 40.00
        data = {
            'customer': self.customer.id,
            'package': self.package.id,
            'price': updated_price
        }
        response = self.client.put(self._get_invoice_detail_url(self.initial_invoices[0].id), data=data, content_type='application/json')
        updated_invoice = Invoice.objects.get(pk=self.initial_invoices[0].id)
        self.assertEqual(updated_invoice.price, updated_price)

    def test_invoice_detail_PUT_not_found_error(self):
        invalid_invoice_id = 999
        response = self.client.put(self._get_invoice_detail_url(invalid_invoice_id), data={}, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_invoice_detail_DELETE_success_status(self):
        response = self.client.delete(self._get_invoice_detail_url(self.initial_invoices[0].id))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_invoice_detail_DELETE_not_found_error(self):
        invalid_invoice_id = 999
        response = self.client.delete(self._get_invoice_detail_url(invalid_invoice_id))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
