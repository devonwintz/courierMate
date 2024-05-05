import logging
from ..serializers import CreateInvoiceSerializer, UpdateInvoiceSerializer
from ..models import Invoice
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view

logger = logging.getLogger("backendapp_request")

class InvoiceList(APIView):
    def get(self, request):
        try:
            invoices = Invoice.objects.all()
            serializer = CreateInvoiceSerializer(invoices, many=True)
            logger.info("Retrieved all invoices successfully")
            return Response({
                'status': 'success',
                'data': serializer.data,
                'error': None,
            }, status=status.HTTP_200_OK)
        except Exception as e:
             logger.exception("Failed to retrieve invoices")
             return Response({
                'status': 'error',
                'data': None,
                'error': 'Internal server error: Failed to retrieve invoices'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request):
        try:
            serializer = CreateInvoiceSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                logger.info("Created new invoice successfully")
                return Response({
                    'status': 'success',
                    'data': serializer.data,
                    'error': None
                }, status=status.HTTP_201_CREATED)
            else:
                logger.warning(f"Failed to create invoice: {serializer.errors}")
                return Response({
                    'status': 'error',
                    'data': None,
                    'error': serializer.errors
                }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
             logger.exception("Internal server error: Failed to create invoice")
             return Response({
                'status': 'error',
                'data': None,
                'error': 'Internal server error: Failed to create invoice'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class InvoiceDetail(APIView):
    def get(self, request, id):
        try:
            invoice = Invoice.objects.get(pk=id)
            serializer = CreateInvoiceSerializer(invoice)
            logger.info("Retrieved invoice details successfully")
            return Response({
                'status': 'success',
                'data': serializer.data,
                'error': None
            }, status=status.HTTP_200_OK)
        except Invoice.DoesNotExist:
            logger.warning(f"Invoice with id '{id}' not found")
            return Response({
                'status': 'error',
                'data': None,
                'error': 'Invoice not found'
            }, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
             logger.exception("Internal server error: Failed to retrieve invoice details")
             return Response({
                'status': 'error',
                'data': None,
                'error': 'Internal server error: Failed to retrieve invoice details'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def put(self, request, id):
        try:
            invoice = Invoice.objects.get(pk=id)
            serializer = UpdateInvoiceSerializer(invoice, data=request.data)
            if serializer.is_valid():
                serializer.save()
                logger.info("Updated invoice details successfully")
                return Response({
                    'status': 'success',
                    'data': serializer.data,
                    'error': None
                }, status=status.HTTP_200_OK)
            else:
                logger.exception(f"Failed to update invoice details: {serializer.errors}")
                return Response({
                    'status': 'error',
                    'data': None,
                    'error': serializer.errors
                }, status=status.HTTP_400_BAD_REQUEST)
        except Invoice.DoesNotExist:
            logger.warning(f"Invoice with id '{id}' not found")
            return Response({
                'status': 'error',
                'data': None,
                'error': 'Invoice not found'
            }, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
             logger.exception("Internal server error: Failed to update invoice details")
             return Response({
                'status': 'error',
                'data': None,
                'error': 'Internal server error: Failed to update invoice details'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request, id):
        try:
            invoice = Invoice.objects.get(pk=id)
            invoice.delete()
            logger.info("Deleted invoice successfully")
            return Response({
                'status': 'success',
                'data': None,
                'error': None
            }, status=status.HTTP_204_NO_CONTENT)
        except Invoice.DoesNotExist:
            logger.warning(f"Invoice with id '{id}' not found")
            return Response({
                'status': 'error',
                'data': None,
                'error': 'Invoice not found'
            }, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
             logger.exception("Internal server error: Failed to delete invoice")
             return Response({
                'status': 'error',
                'data': None,
                'error': 'Internal server error: Failed to delete invoice'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)