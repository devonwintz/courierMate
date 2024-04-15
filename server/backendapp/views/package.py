from ..serializers import CreatePackageSerializer, UpdatePackageSerializer
from ..models import Package
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view

class PackageList(APIView):
    def get(self, request):
        try:
            packages = Package.objects.all()
            serializer = CreatePackageSerializer(packages, many=True)
            return Response({
                'status': 'success',
                'data': serializer.data,
                'error': None,
            }, status=status.HTTP_200_OK)
        except Exception as e:
             return Response({
                'status': 'error',
                'data': None,
                'error': 'Failed to retrieve packages'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request):
        try:
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
        except Exception as e:
             return Response({
                'status': 'error',
                'data': None,
                'error': 'Failed to create package'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class PackageDetail(APIView):
    def get(self, request, id):
        try:
            package = Package.objects.get(pk=id)
            serializer = CreatePackageSerializer(package)
            return Response({
                'status': 'success',
                'data': serializer.data,
                'error': None
            }, status=status.HTTP_200_OK)
        except Package.DoesNotExist:
            return Response({
                'status': 'error',
                'data': None,
                'error': 'Package not found'
            }, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
             return Response({
                'status': 'error',
                'data': None,
                'error': 'Failed to retrieve package details'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def put(self, request, id):
        try:
            package = Package.objects.get(pk=id)
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
        except Package.DoesNotExist:
            return Response({
                'status': 'error',
                'data': None,
                'error': 'Package not found'
            }, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
             return Response({
                'status': 'error',
                'data': None,
                'error': 'Failed to update package details'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request, id):
        try:
            package = Package.objects.get(pk=id)
            package.delete()
            return Response({
                'status': 'success',
                'data': None,
                'error': None
            }, status=status.HTTP_204_NO_CONTENT)
        except Package.DoesNotExist:
            return Response({
                'status': 'error',
                'data': None,
                'error': 'Package not found'
            }, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
             return Response({
                'status': 'error',
                'data': None,
                'error': 'Failed to delete package'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)