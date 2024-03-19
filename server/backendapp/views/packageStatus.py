from ..serializers import PackageStatusSerializer
from ..models import PackageStatus
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view

class PackageStatusList(APIView):
    def get(self, request):
        package_statuses = PackageStatus.objects.all()
        serializer = PackageStatusSerializer(package_statuses, many=True)
        return Response({
            'status': 'success',
            'data': serializer.data,
            'error': None,
        }, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = PackageStatusSerializer(data=request.data)
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

class PackageStatusDetail(APIView):
    def get(self, request, id):
        try:
            package_status = PackageStatus.objects.get(pk=id)
        except PackageStatus.DoesNotExist:
            return Response({
                'status': 'error',
                'data': None,
                'error': 'Package status not found'
            }, status=status.HTTP_404_NOT_FOUND)

        serializer = PackageStatusSerializer(package_status)
        return Response({
            'status': 'success',
            'data': serializer.data,
            'error': None
        }, status=status.HTTP_200_OK)

    def put(self, request, id):
        try:
            package_status = PackageStatus.objects.get(pk=id)
        except PackageStatus.DoesNotExist:
            return Response({
                'status': 'error',
                'data': None,
                'error': 'Package status not found'
            }, status=status.HTTP_404_NOT_FOUND)

        serializer = PackageStatusSerializer(package_status, data=request.data)
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
            package_status = PackageStatus.objects.get(pk=id)
        except Customer.DoesNotExist:
            return Response({
                'status': 'error',
                'data': None,
                'error': 'Package status not found'
            }, status=status.HTTP_404_NOT_FOUND)

        package_status.delete()
        return Response({
            'status': 'success',
            'data': None,
            'error': None
        }, status=status.HTTP_204_NO_CONTENT)