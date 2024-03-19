from django.db import models
from .customer import Customer
from .packageCategory import PackageCategory
from .packageStatus import PackageStatus

class Package(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    tracking_number = models.CharField(max_length=255, null=True)
    category=  models.ForeignKey(PackageCategory, on_delete=models.CASCADE)
    date_delivered = models.DateField(null=True)
    date_shipped = models.DateField(null=True)
    expected_delivery_date = models.DateField(null=True)
    status = models.ForeignKey(PackageStatus, on_delete=models.CASCADE)
    weight = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    length = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    width = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    height = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    created = models.DateTimeField(auto_now_add=True, null=False)
    created_by = models.CharField(max_length=255, null=False, default='Admin')
    updated = models.DateTimeField(auto_now=True, null=False)
    updated_by = models.CharField(max_length=255, null=False, default='Admin')

    def __str__(self): 
        return self.tracking_number

    class Meta:
        verbose_name_plural = "packages"