import logging
from ..serializers import CreateCustomerSerializer, UpdateCustomerSerializer
from ..models import Customer
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view

logger = logging.getLogger("backendapp_request")

class CustomerList(APIView):
    def get(self, request):
        try:
            customers = Customer.objects.all()
            serializer = CreateCustomerSerializer(customers, many=True)
            logger.info("Retrieved all customers successfully")
            return Response({
                'status': 'success',
                'data': serializer.data,
                'error': None,
            }, status=status.HTTP_200_OK)
        except Exception as e:
             logger.exception("Failed to retrieve customers")
             return Response({
                'status': 'error',
                'data': None,
                'error': 'Internal server error: Failed to retrieve customers'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request):
        try:
            serializer = CreateCustomerSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                logger.info("Created new customer successfully")
                return Response({
                    'status': 'success',
                    'data': serializer.data,
                    'error': None
                }, status=status.HTTP_201_CREATED)
            else:
                logger.warning(f"Failed to create customer: {serializer.errors}")
                return Response({
                    'status': 'error',
                    'data': None,
                    'error': serializer.errors
                }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
             logger.exception("Internal server error: Failed to create customer")
             return Response({
                'status': 'error',
                'data': None,
                'error': 'Internal server error: Failed to create customer'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class CustomerDetail(APIView):
    def get(self, request, id):
        try:
            customer = Customer.objects.get(pk=id)
            serializer = CreateCustomerSerializer(customer)
            logger.info("Retrieved customer details successfully")
            return Response({
            'status': 'success',
            'data': serializer.data,
            'error': None
        }, status=status.HTTP_200_OK)
        except Customer.DoesNotExist:
            logger.warning(f"Customer with id '{id}' not found")
            return Response({
                'status': 'error',
                'data': None,
                'error': 'Customer not found'
            }, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.exception("Internal server error: Failed to retrieve customer details")
            return Response({
                'status': 'error',
                'data': None,
                'error': 'Internal server error: Failed to retrieve customer details'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def put(self, request, id):
        try:
            customer = Customer.objects.get(pk=id)
            serializer = UpdateCustomerSerializer(customer, data=request.data)
            if serializer.is_valid():
                serializer.save()
                logger.info("Updated customer details successfully")
                return Response({
                    'status': 'success',
                    'data': serializer.data,
                    'error': None
                }, status=status.HTTP_200_OK)
            else:
                logger.exception(f"Failed to update customer details: {serializer.errors}")
                return Response({
                    'status': 'error',
                    'data': None,
                    'error': serializer.errors
                }, status=status.HTTP_400_BAD_REQUEST)
        except Customer.DoesNotExist:
            logger.warning(f"Customer with id '{id}' not found")
            return Response({
                'status': 'error',
                'data': None,
                'error': 'Customer not found'
            }, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.exception("Internal server error: Failed to update customer details")
            return Response({
                'status': 'error',
                'data': None,
                'error': 'Internal server error: Failed to update customer details'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request, id):
        try:
            customer = Customer.objects.get(pk=id)
            customer.delete()
            logger.info("Deleted customer successfully")
            return Response({
                'status': 'success',
                'data': None,
                'error': None
            }, status=status.HTTP_204_NO_CONTENT)
        except Customer.DoesNotExist:
            logger.warning(f"Customer with id '{id}' not found")
            return Response({
                'status': 'error',
                'data': None,
                'error': 'Customer not found'
            }, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.exception("Internal server error: Failed to delete customer")
            return Response({
                'status': 'error',
                'data': None,
                'error': 'Internal server error: Failed to delete customer'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

