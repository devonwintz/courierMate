import logging
from ..serializers import PackageStatusSerializer
from ..models import PackageStatus
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view

logger = logging.getLogger("backendapp_request")

class PackageStatusList(APIView):
    def get(self, request):
        try:
            package_statuses = PackageStatus.objects.all()
            serializer = PackageStatusSerializer(package_statuses, many=True)
            logger.info("Retrieved all package statuses successfully")
            return Response({
                'status': 'success',
                'data': serializer.data,
                'error': None,
            }, status=status.HTTP_200_OK)
        except Exception as e:
             logger.exception("Failed to retrieve package statuses")
             return Response({
                'status': 'error',
                'data': None,
                'error': 'Internal server error: Failed to retrieve package statuses'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request):
        try:
            serializer = PackageStatusSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                logger.info("Created new package status successfully")
                return Response({
                    'status': 'success',
                    'data': serializer.data,
                    'error': None
                }, status=status.HTTP_201_CREATED)
            else:
                logger.warning(f"Failed to create package status: {serializer.errors}")
                return Response({
                    'status': 'error',
                    'data': None,
                    'error': serializer.errors
                }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
             logger.exception("Internal server error: Failed to create package status")
             return Response({
                'status': 'error',
                'data': None,
                'error': 'Internal server error: Failed to create package status'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class PackageStatusDetail(APIView):
    def get(self, request, id):
        try:
            package_status = PackageStatus.objects.get(pk=id)
            serializer = PackageStatusSerializer(package_status)
            logger.info("Retrieved package status details successfully")
            return Response({
                'status': 'success',
                'data': serializer.data,
                'error': None
            }, status=status.HTTP_200_OK)
        except PackageStatus.DoesNotExist:
            logger.warning(f"Package status with id '{id}' not found")
            return Response({
                'status': 'error',
                'data': None,
                'error': 'Package status not found'
            }, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
             logger.exception("Internal server error: Failed to retrieve package status details")
             return Response({
                'status': 'error',
                'data': None,
                'error': 'Internal server error: Failed to retrieve package status details'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    def put(self, request, id):
        try:
            package_status = PackageStatus.objects.get(pk=id)
            serializer = PackageStatusSerializer(package_status, data=request.data)
            if serializer.is_valid():
                serializer.save()
                logger.info("Updated package status details successfully")
                return Response({
                    'status': 'success',
                    'data': serializer.data,
                    'error': None
                }, status=status.HTTP_200_OK)
            else:
                logger.exception(f"Failed to update package status details: {serializer.errors}")
                return Response({
                    'status': 'error',
                    'data': None,
                    'error': serializer.errors
                }, status=status.HTTP_400_BAD_REQUEST)
        except PackageStatus.DoesNotExist:
            logger.warning(f"Package status with id '{id}' not found")
            return Response({
                'status': 'error',
                'data': None,
                'error': 'Package status not found'
            }, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
             logger.exception("Internal server error: Failed to update customer details")
             return Response({
                'status': 'error',
                'data': None,
                'error': 'Internal server error: Failed to update package status details'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request, id):
        try:
            package_status = PackageStatus.objects.get(pk=id)
            package_status.delete()
            logger.info("Deleted package status successfully")
            return Response({
                'status': 'success',
                'data': None,
                'error': None
            }, status=status.HTTP_204_NO_CONTENT)
        except PackageStatus.DoesNotExist:
            logger.warning(f"Package status with id '{id}' not found")
            return Response({
                'status': 'error',
                'data': None,
                'error': 'Package status not found'
            }, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
             logger.exception("Internal server error: Failed to delete package status")
             return Response({
                'status': 'error',
                'data': None,
                'error': 'Internal server error: Failed to delete package status'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

