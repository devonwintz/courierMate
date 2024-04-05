from ..serializers import CreatePackageSerializer, UpdatePackageSerializer
from ..models import Package
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view

class PackageList(APIView):
    def get(self, request):
        packages = Package.objects.all()
        serializer = CreatePackageSerializer(packages, many=True)
        return Response({
            'status': 'success',
            'data': serializer.data,
            'error': None,
        }, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = CreatePackageSerializer(data=request.data)
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

class PackageDetail(APIView):
    def get(self, request, id):
        try:
            package = Package.objects.get(pk=id)
        except Package.DoesNotExist:
            return Response({
                'status': 'error',
                'data': None,
                'error': 'Package not found'
            }, status=status.HTTP_404_NOT_FOUND)

        serializer = CreatePackageSerializer(package)
        return Response({
            'status': 'success',
            'data': serializer.data,
            'error': None
        }, status=status.HTTP_200_OK)

    def put(self, request, id):
        try:
            package = Package.objects.get(pk=id)
        except Package.DoesNotExist:
            return Response({
                'status': 'error',
                'data': None,
                'error': 'Package not found'
            }, status=status.HTTP_404_NOT_FOUND)

        serializer = UpdatePackageSerializer(package, data=request.data)
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
            package = Package.objects.get(pk=id)
        except Package.DoesNotExist:
            return Response({
                'status': 'error',
                'data': None,
                'error': 'Package not found'
            }, status=status.HTTP_404_NOT_FOUND)

        package.delete()
        return Response({
            'status': 'success',
            'data': None,
            'error': None
        }, status=status.HTTP_204_NO_CONTENT)