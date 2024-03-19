from .models import *
from rest_framework import serializers

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['id', 'first_name', 'last_name', 'telephone', 'email', 'email_verified', 'notification_opted_in', 'created', 'created_by', 'updated', 'updated_by']

class PackageSerializer(serializers.ModelSerializer):
    customer = serializers.PrimaryKeyRelatedField(
        queryset = Customer.objects.all(),
        many=False
    )
    category = serializers.PrimaryKeyRelatedField(
        queryset = PackageCategory.objects.all(),
        many=False
    )
    status = serializers.PrimaryKeyRelatedField(
        queryset =  PackageStatus.objects.all(),
        many=False
    )

    class Meta:
        model = Package
        fields = ['id', 'customer', 'tracking_number', 'category', 'date_delivered', 'date_shipped', 'expected_delivery_date', 'status', 'weight', 'length', 'width', 'height', 'created', 'created_by', 'updated', 'updated_by']

class PackageCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = PackageCategory
        fields = ['id', 'name', 'created', 'created_by', 'updated', 'updated_by']

class PackageStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = PackageStatus
        fields = ['id', 'name', 'created', 'created_by', 'updated', 'updated_by']