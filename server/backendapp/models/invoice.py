import uuid
from django.db import models
from .customer import Customer
from .package import Package

class Invoice(models.Model):
    invoice_no = models.CharField(max_length=100, unique=True, null=False, editable=False)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    package = models.ForeignKey(Package, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=False)
    created = models.DateTimeField(auto_now_add=True, null=False)
    created_by = models.CharField(max_length=255, null=False, default='Admin')
    updated = models.DateTimeField(auto_now=True, null=False)
    updated_by = models.CharField(max_length=255, null=False, default='Admin')

    def save(self, *args, **kwargs):
        if not self.invoice_no:
            self.invoice_no = self.generate_invoice_no()
        super().save(*args, **kwargs)

    def generate_invoice_no(self):
        return uuid.uuid4().hex[:12].upper()

    def __str__(self):
        return self.invoice_no

    class Meta:
        verbose_name_plural = "invoices"
        indexes = [
            models.Index(fields=['invoice_no']),
        ]