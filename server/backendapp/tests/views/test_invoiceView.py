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

    def test_invoice_list_GET(self):
        response = self.client.get(reverse('invoice-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()['data']), len(self.initial_invoices))

    def test_invoice_list_POST_success(self):
        data = {
            'customer': self.customer.id,
            'package': self.package.id,
            'price': 20.00
        }
        response = self.client.post(reverse('invoice-list'), data=data, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Invoice.objects.count(), len(self.initial_invoices) + 1)

    def test_invoice_list_POST_error(self):
        invalid_customer_id = 999
        data = {
            'customer': invalid_customer_id,
            'package': self.package.id,
            'price': 20.00
        }
        response = self.client.post(reverse('invoice-list'), data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_invoice_detail_GET_success(self):
        response = self.client.get(self._get_invoice_detail_url(self.initial_invoices[0].id))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_invoice_detail_GET_error(self):
        invalid_invoice_id = 999
        response = self.client.get(self._get_invoice_detail_url(invalid_invoice_id))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.json().get('error'), 'Invoice not found')


    def test_invoice_detail_PUT_success(self):
        updated_price = 40.00
        data = {
            'customer': self.customer.id,
            'package': self.package.id,
            'price': updated_price
        }
        response = self.client.put(self._get_invoice_detail_url(self.initial_invoices[0].id), data=data, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        updated_invoice = Invoice.objects.get(pk=self.initial_invoices[0].id)
        self.assertEqual(updated_invoice.price, updated_price)

    def test_invoice_detail_PUT_errors(self):
        # Test incomplete data (400 Error)
        incomplete_data = {
            'package': self.package.id,
            'price': 20.00
        }
        response = self.client.put(self._get_invoice_detail_url(self.initial_invoices[0].id), data=incomplete_data, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Test invalid invoice ID (404 Error)
        invalid_invoice_id = 999
        response = self.client.put(self._get_invoice_detail_url(invalid_invoice_id), data={}, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_invoice_detail_DELETE_success(self):
        response = self.client.delete(self._get_invoice_detail_url(self.initial_invoices[0].id))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_invoice_detail_DELETE_error(self):
        invalid_invoice_id = 999
        response = self.client.delete(self._get_invoice_detail_url(invalid_invoice_id))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
