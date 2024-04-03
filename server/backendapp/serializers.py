from .models import *
from rest_framework import serializers

class CustomerSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(
        queryset = User.objects.all(),
        many=False
    )

    class Meta:
        model = Customer
        fields = ['id', 'user', 'first_name', 'last_name', 'telephone', 'email', 'email_verified', 'notification_opted_in', 'created', 'created_by', 'updated', 'updated_by']

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

class InvoiceSerializer(serializers.ModelSerializer):
    customer = serializers.PrimaryKeyRelatedField(
        queryset = Customer.objects.all(),
        many=False
    )
    package = serializers.PrimaryKeyRelatedField(
        queryset = Package.objects.all(),
        many=False
    )
    class Meta:
        model = Invoice
        fields = ['id', 'invoice_no', 'customer', 'package', 'price', 'created', 'created_by', 'updated', 'updated_by']

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'email', 'password', 'is_staff', 'is_superuser', 'is_active', 'created', 'created_by', 'updated', 'updated_by']
        extra_kwargs = {
            'password': {'write_only': True, 'required': True}
        }

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance

    def update(self, instance, validated_data):
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.email = validated_data.get('email', instance.email)

        password = validated_data.get('password')
        if password is not None:
            instance.set_password(password)

        instance.updated_by = validated_data.get('updated_by', instance.updated_by)
        instance.save()
        return instance