from django.test import TestCase
from backendapp.tests.factories import InvoiceFactory

class InvoiceModelTest(TestCase):
    def test_string_representation(self):
        invoice = InvoiceFactory()
        expected_str = invoice.invoice_no
        actual_str = str(invoice)
        self.assertEqual(actual_str, expected_str)
