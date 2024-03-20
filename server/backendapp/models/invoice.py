from django.db import models
from .customer import Customer
from .package import Package

class Invoice(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    package = models.ForeignKey(Package, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=False, default=0.00)
    created = models.DateTimeField(auto_now_add=True, null=False)
    created_by = models.CharField(max_length=255, null=False, default='Admin')
    updated = models.DateTimeField(auto_now=True, null=False)
    updated_by = models.CharField(max_length=255, null=False, default='Admin')

    def __str__(self): 
        return str(self.id)

    class Meta:
        verbose_name_plural = "invoices"