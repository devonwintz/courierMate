import logging

from ..serializers import CreatePackageSerializer, UpdatePackageSerializer
from ..models import Package
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view

logger = logging.getLogger("backendapp_request")

class PackageList(APIView):
    def get(self, request):
        try:
            packages = Package.objects.all()
            serializer = CreatePackageSerializer(packages, many=True)
            logger.info("Retrieved all packages successfully")
            return Response({
                'status': 'success',
                'data': serializer.data,
                'error': None,
            }, status=status.HTTP_200_OK)
        except Exception as e:
             logger.exception("Failed to retrieve packages")
             return Response({
                'status': 'error',
                'data': None,
                'error': 'Internal server error: Failed to retrieve packages'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request):
        try:
            serializer = CreatePackageSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                logger.info("Created new package successfully")
                return Response({
                    'status': 'success',
                    'data': serializer.data,
                    'error': None
                }, status=status.HTTP_201_CREATED)
            else:
                logger.warning(f"Failed to create package: {serializer.errors}")
                return Response({
                    'status': 'error',
                    'data': None,
                    'error': serializer.errors
                }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
             logger.exception("Internal server error: Failed to create package")
             return Response({
                'status': 'error',
                'data': None,
                'error': 'Internal server error: Failed to create package'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class PackageDetail(APIView):
    def get(self, request, id):
        try:
            package = Package.objects.get(pk=id)
            serializer = CreatePackageSerializer(package)
            logger.info("Retrieved package details successfully")
            return Response({
                'status': 'success',
                'data': serializer.data,
                'error': None
            }, status=status.HTTP_200_OK)
        except Package.DoesNotExist:
            logger.warning(f"package with id '{id}' not found")
            return Response({
                'status': 'error',
                'data': None,
                'error': 'Package not found'
            }, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
             logger.exception("Internal server error: Failed to retrieve package details")
             return Response({
                'status': 'error',
                'data': None,
                'error': 'Internal server error: Failed to retrieve package details'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def put(self, request, id):
        try:
            package = Package.objects.get(pk=id)
            serializer = UpdatePackageSerializer(package, data=request.data)
            if serializer.is_valid():
                serializer.save()
                logger.info("Updated package details successfully")
                return Response({
                    'status': 'success',
                    'data': serializer.data,
                    'error': None
                }, status=status.HTTP_200_OK)
            else:
                logger.exception(f"Failed to update package details: {serializer.errors}")
                return Response({
                    'status': 'error',
                    'data': None,
                    'error': serializer.errors
                }, status=status.HTTP_400_BAD_REQUEST)
        except Package.DoesNotExist:
            logger.warning(f"Package with id '{id}' not found")
            return Response({
                'status': 'error',
                'data': None,
                'error': 'Package not found'
            }, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
             logger.exception("Internal server error: Failed to update package details")
             return Response({
                'status': 'error',
                'data': None,
                'error': 'Internal server error: Failed to update package details'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request, id):
        try:
            package = Package.objects.get(pk=id)
            package.delete()
            logger.info("Deleted package successfully")
            return Response({
                'status': 'success',
                'data': None,
                'error': None
            }, status=status.HTTP_204_NO_CONTENT)
        except Package.DoesNotExist:
            logger.warning(f"Package with id '{id}' not found")
            return Response({
                'status': 'error',
                'data': None,
                'error': 'Package not found'
            }, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
             logger.exception("Internal server error: Failed to delete package")
             return Response({
                'status': 'error',
                'data': None,
                'error': 'Internal server error: Failed to delete package'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)