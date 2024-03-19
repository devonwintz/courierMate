from django.db import models

class PackageCategory(models.Model):
    name =  models.CharField(max_length=255, null=False)
    created = models.DateTimeField(auto_now_add=True, null=False)
    created_by = models.CharField(max_length=255, null=False, default='Admin')
    updated = models.DateTimeField(auto_now=True, null=False)
    updated_by = models.CharField(max_length=255, null=False, default='Admin')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "package categories"