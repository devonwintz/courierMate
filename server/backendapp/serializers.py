from .models import *
from rest_framework import serializers

class CreateCustomerSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(
        queryset = User.objects.all(),
        many=False
    )

    class Meta:
        model = Customer
        fields = ['id', 'user', 'first_name', 'last_name', 'telephone', 'email', 'email_verified', 'notification_opted_in', 'created', 'created_by', 'updated', 'updated_by']

        extra_kwargs = {
            'user': {'required': True},
            'first_name': {'required': True},
            'last_name': {'required': True},
            'telephone': {'required': True},
        }

class UpdateCustomerSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(
        many=False,
        read_only=True,
    )

    class Meta:
        model = Customer
        fields = ['id', 'user', 'first_name', 'last_name', 'telephone', 'email', 'email_verified', 'notification_opted_in', 'created', 'created_by', 'updated', 'updated_by']

        extra_kwargs = {
            'user': {'required': False},
            'first_name': {'required': False},
            'last_name': {'required': False},
            'telephone': {'required': False},
        }

class CreatePackageSerializer(serializers.ModelSerializer):
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
        fields = ['id', 'customer', 'tracking_number', 'category', 'date_delivered_ny', 'date_arrived_gy', 'date_shipped', 'expected_delivery_date', 'status', 'weight', 'length', 'width', 'height', 'created', 'created_by', 'updated', 'updated_by']

        extra_kwargs = {
            'customer': {'required': True},
            'tracking_number': {'required': True},
            'category': {'required': True},
            'status': {'required': True},
            'date_delivered_ny': {'required': True},
            'date_arrived_gy': {'required': False},
            'date_shipped': {'required': False},
            'expected_delivery_date': {'required': False},
            'weight': {'required': False},
            'length': {'required': False},
            'width': {'required': False},
            'height': {'required': False},
        }

class UpdatePackageSerializer(serializers.ModelSerializer):
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
        fields = ['id', 'customer', 'tracking_number', 'category', 'date_delivered_ny', 'date_arrived_gy', 'date_shipped', 'expected_delivery_date', 'status', 'weight', 'length', 'width', 'height', 'created', 'created_by', 'updated', 'updated_by']

        extra_kwargs = {
            'customer': {'required': False},
            'tracking_number': {'required': False},
            'category': {'required': False},
            'status': {'required': False},
            'date_delivered_ny': {'required': False},
            'date_arrived_gy': {'required': False},
            'date_shipped': {'required': False},
            'expected_delivery_date': {'required': False},
            'weight': {'required': False},
            'length': {'required': False},
            'width': {'required': False},
            'height': {'required': False},
        }

class PackageCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = PackageCategory
        fields = ['id', 'name', 'created', 'created_by', 'updated', 'updated_by']

class PackageStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = PackageStatus
        fields = ['id', 'name', 'created', 'created_by', 'updated', 'updated_by']

class CreateInvoiceSerializer(serializers.ModelSerializer):
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

        extra_kwargs = {
            'customer': {'required': True},
            'package': {'required': True},
            'price': {'required': True},
        }

class UpdateInvoiceSerializer(serializers.ModelSerializer):
    customer = serializers.PrimaryKeyRelatedField(
        many=False,
        read_only=True,
    )
    package = serializers.PrimaryKeyRelatedField(
        many=False,
        read_only=True,
    )
    class Meta:
        model = Invoice
        fields = ['id', 'invoice_no', 'customer', 'package', 'price', 'created', 'created_by', 'updated', 'updated_by']

        extra_kwargs = {
        'customer': {'required': False},
        'package': {'required': False},
        'price': {'required': False},
    }

class CreateUserSerializer(serializers.ModelSerializer):
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

class UpdateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'email', 'password', 'is_staff', 'is_superuser', 'is_active', 'created', 'created_by', 'updated', 'updated_by']
        extra_kwargs = {
            'first_name': {'required': False},
            'last_name': {'required': False},
            'email': {'required': False},
            'password': {'write_only': True, 'required': False}
        }

    def update(self, instance, validated_data):
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.email = validated_data.get('email', instance.email)
        instance.is_staff = validated_data.get('is_staff', instance.is_staff)
        instance.is_superuser = validated_data.get('is_superuser', instance.is_superuser)
        instance.is_active = validated_data.get('is_active', instance.is_active)
        instance.updated_by = validated_data.get('updated_by', instance.updated_by)

        password = validated_data.get('password')
        if password is not None:
            instance.set_password(password)

        instance.updated_by = validated_data.get('updated_by', instance.updated_by)
        instance.save()
        return instance