from ..serializers import CreateInvoiceSerializer, UpdateInvoiceSerializer
from ..models import Invoice
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view

class InvoiceList(APIView):
    def get(self, request):
        invoices = Invoice.objects.all()
        serializer = CreateInvoiceSerializer(invoices, many=True)
        return Response({
            'status': 'success',
            'data': serializer.data,
            'error': None,
        }, status=status.HTTP_200_OK)

    def post(self, request):
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

class InvoiceDetail(APIView):
    def get(self, request, id):
        try:
            invoice = Invoice.objects.get(pk=id)
        except Invoice.DoesNotExist:
            return Response({
                'status': 'error',
                'data': None,
                'error': 'Invoice not found'
            }, status=status.HTTP_404_NOT_FOUND)

        serializer = CreateInvoiceSerializer(invoice)
        return Response({
            'status': 'success',
            'data': serializer.data,
            'error': None
        }, status=status.HTTP_200_OK)

    def put(self, request, id):
        try:
            invoice = Invoice.objects.get(pk=id)
        except Invoice.DoesNotExist:
            return Response({
                'status': 'error',
                'data': None,
                'error': 'Invoice not found'
            }, status=status.HTTP_404_NOT_FOUND)

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

    def delete(self, request, id):
        try:
            invoice = Invoice.objects.get(pk=id)
        except Invoice.DoesNotExist:
            return Response({
                'status': 'error',
                'data': None,
                'error': 'Invoice not found'
            }, status=status.HTTP_404_NOT_FOUND)

        invoice.delete()
        return Response({
            'status': 'success',
            'data': None,
            'error': None
        }, status=status.HTTP_204_NO_CONTENT)