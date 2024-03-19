from ..serializers import CustomerSerializer
from ..models import Customer
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view

class CustomerList(APIView):
    def get(self, request):
        customers = Customer.objects.all()
        serializer = CustomerSerializer(customers, many=True)
        return Response({
            'status': 'success',
            'data': serializer.data,
            'error': None,
        }, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = CustomerSerializer(data=request.data)
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

class CustomerDetail(APIView):
    def get(self, request, id):
        try:
            customer = Customer.objects.get(pk=id)
        except Customer.DoesNotExist:
            return Response({
                'status': 'error',
                'data': None,
                'error': 'Customer not found'
            }, status=status.HTTP_404_NOT_FOUND)

        serializer = CustomerSerializer(customer)
        return Response({
            'status': 'success',
            'data': serializer.data,
            'error': None
        }, status=status.HTTP_200_OK)

    def put(self, request, id):
        try:
            customer = Customer.objects.get(pk=id)
        except Customer.DoesNotExist:
            return Response({
                'status': 'error',
                'data': None,
                'error': 'Customer not found'
            }, status=status.HTTP_404_NOT_FOUND)

        serializer = CustomerSerializer(customer, data=request.data)
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

    def delete(self, request, id):
        try:
            customer = Customer.objects.get(pk=id)
        except Customer.DoesNotExist:
            return Response({
                'status': 'error',
                'data': None,
                'error': 'Customer not found'
            }, status=status.HTTP_404_NOT_FOUND)

        customer.delete()
        return Response({
            'status': 'success',
            'data': None,
            'error': None
        }, status=status.HTTP_204_NO_CONTENT)