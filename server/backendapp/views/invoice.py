from ..serializers import CreateInvoiceSerializer, UpdateInvoiceSerializer
from ..models import Invoice
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view

class InvoiceList(APIView):
    def get(self, request):
        try:
            invoices = Invoice.objects.all()
            serializer = CreateInvoiceSerializer(invoices, many=True)
            return Response({
                'status': 'success',
                'data': serializer.data,
                'error': None,
            }, status=status.HTTP_200_OK)
        except Exception as e:
             return Response({
                'status': 'error',
                'data': None,
                'error': 'Failed to retrieve invoices'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request):
        try:
            serializer = CreateInvoiceSerializer(data=request.data)
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
                'error': 'Failed to create invoice'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class InvoiceDetail(APIView):
    def get(self, request, id):
        try:
            invoice = Invoice.objects.get(pk=id)
            serializer = CreateInvoiceSerializer(invoice)
            return Response({
                'status': 'success',
                'data': serializer.data,
                'error': None
            }, status=status.HTTP_200_OK)
        except Invoice.DoesNotExist:
            return Response({
                'status': 'error',
                'data': None,
                'error': 'Invoice not found'
            }, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
             return Response({
                'status': 'error',
                'data': None,
                'error': 'Failed to retrieve invoice details'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def put(self, request, id):
        try:
            invoice = Invoice.objects.get(pk=id)
            serializer = UpdateInvoiceSerializer(invoice, data=request.data)
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
        except Invoice.DoesNotExist:
            return Response({
                'status': 'error',
                'data': None,
                'error': 'Invoice not found'
            }, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
             return Response({
                'status': 'error',
                'data': None,
                'error': 'Failed to update invoice details'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request, id):
        try:
            invoice = Invoice.objects.get(pk=id)
            invoice.delete()
            return Response({
                'status': 'success',
                'data': None,
                'error': None
            }, status=status.HTTP_204_NO_CONTENT)
        except Invoice.DoesNotExist:
            return Response({
                'status': 'error',
                'data': None,
                'error': 'Invoice not found'
            }, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
             return Response({
                'status': 'error',
                'data': None,
                'error': 'Failed to delete invoice'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)