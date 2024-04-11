from ..serializers import CreateCustomerSerializer, UpdateCustomerSerializer
from ..models import Customer
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view

class CustomerList(APIView):
    def get(self, request):
        try:
            customers = Customer.objects.all()
            serializer = CreateCustomerSerializer(customers, many=True)
            return Response({
                'status': 'success',
                'data': serializer.data,
                'error': None,
            }, status=status.HTTP_200_OK)
        except Exception as e:
             return Response({
                'status': 'error',
                'data': None,
                'error': 'Failed to retrieve customers'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request):
        try:
            serializer = CreateCustomerSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({
                    'status': 'success',
                    'data': serializer.data,
                    'error': None
                }, status=status.HTTP_201_CREATED)
            else:
                return Response({
                    'status': 'error',
                    'data': None,
                    'error': serializer.errors
                }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
             return Response({
                'status': 'error',
                'data': None,
                'error': 'Failed to create customer'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class CustomerDetail(APIView):
    def get(self, request, id):
        try:
            customer = Customer.objects.get(pk=id)
            serializer = CreateCustomerSerializer(customer)
            return Response({
            'status': 'success',
            'data': serializer.data,
            'error': None
        }, status=status.HTTP_200_OK)
        except Customer.DoesNotExist:
            return Response({
                'status': 'error',
                'data': None,
                'error': 'Customer not found'
            }, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({
                'status': 'error',
                'data': None,
                'error': 'Failed to retrieve customer details'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def put(self, request, id):
        try:
            customer = Customer.objects.get(pk=id)
            serializer = UpdateCustomerSerializer(customer, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({
                    'status': 'success',
                    'data': serializer.data,
                    'error': None
                }, status=status.HTTP_200_OK)
            else:
                return Response({
                    'status': 'error',
                    'data': None,
                    'error': serializer.errors
                }, status=status.HTTP_400_BAD_REQUEST)
        except Customer.DoesNotExist:
            return Response({
                'status': 'error',
                'data': None,
                'error': 'Customer not found'
            }, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({
                'status': 'error',
                'data': None,
                'error': 'Failed to update customer details'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request, id):
        try:
            customer = Customer.objects.get(pk=id)
            customer.delete()
            return Response({
                'status': 'success',
                'data': None,
                'error': None
            }, status=status.HTTP_204_NO_CONTENT)
        except Customer.DoesNotExist:
            return Response({
                'status': 'error',
                'data': None,
                'error': 'Customer not found'
            }, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({
                'status': 'error',
                'data': None,
                'error': 'Failed to delete customer'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

