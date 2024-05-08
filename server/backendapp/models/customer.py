from django.db import models
from .user import User

class Customer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=255, null=False)
    last_name = models.CharField(max_length=255, null=False)
    telephone = models.CharField(max_length=10, null=False)
    email = models.EmailField(max_length=255, unique=True, null=True)
    email_verified = models.BooleanField(default=False, null=False)
    notification_opted_in = models.BooleanField(default=False, null=False)
    created = models.DateTimeField(auto_now_add=True, null=False)
    created_by = models.CharField(max_length=255, null=False, default='Admin')
    updated = models.DateTimeField(auto_now=True, null=False)
    updated_by = models.CharField(max_length=255, null=False, default='Admin')

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    class Meta:
        verbose_name_plural = "customers"
        indexes = [
            models.Index(fields=['email']),
        ]