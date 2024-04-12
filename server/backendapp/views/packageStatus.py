from ..serializers import PackageStatusSerializer
from ..models import PackageStatus
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view

class PackageStatusList(APIView):
    def get(self, request):
        try:
            package_statuses = PackageStatus.objects.all()
            serializer = PackageStatusSerializer(package_statuses, many=True)
            return Response({
                'status': 'success',
                'data': serializer.data,
                'error': None,
            }, status=status.HTTP_200_OK)
        except Exception as e:
             return Response({
                'status': 'error',
                'data': None,
                'error': 'Failed to retrieve package statuses'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request):
        try:
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
        except Exception as e:
             return Response({
                'status': 'error',
                'data': None,
                'error': 'Failed to create package status'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class PackageStatusDetail(APIView):
    def get(self, request, id):
        try:
            package_status = PackageStatus.objects.get(pk=id)
            serializer = PackageStatusSerializer(package_status)
            return Response({
                'status': 'success',
                'data': serializer.data,
                'error': None
            }, status=status.HTTP_200_OK)
        except PackageStatus.DoesNotExist:
            return Response({
                'status': 'error',
                'data': None,
                'error': 'Package status not found'
            }, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
             return Response({
                'status': 'error',
                'data': None,
                'error': 'Failed to retrieve package status details'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    def put(self, request, id):
        try:
            package_status = PackageStatus.objects.get(pk=id)
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
        except PackageStatus.DoesNotExist:
            return Response({
                'status': 'error',
                'data': None,
                'error': 'Package status not found'
            }, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
             return Response({
                'status': 'error',
                'data': None,
                'error': 'Failed to update package status details'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request, id):
        try:
            package_status = PackageStatus.objects.get(pk=id)
            package_status.delete()
            return Response({
                'status': 'success',
                'data': None,
                'error': None
            }, status=status.HTTP_204_NO_CONTENT)
        except PackageStatus.DoesNotExist:
            return Response({
                'status': 'error',
                'data': None,
                'error': 'Package status not found'
            }, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
             return Response({
                'status': 'error',
                'data': None,
                'error': 'Failed to delete package status'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

