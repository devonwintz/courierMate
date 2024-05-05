import logging
from ..serializers import PackageCategorySerializer
from ..models import PackageCategory
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view

logger = logging.getLogger("backendapp_request")

class PackageCategoryList(APIView):
    def get(self, request):
        try:
            package_categories = PackageCategory.objects.all()
            serializer = PackageCategorySerializer(package_categories, many=True)
            logger.info("Retrieved all package categories successfully")
            return Response({
                'status': 'success',
                'data': serializer.data,
                'error': None,
            }, status=status.HTTP_200_OK)
        except Exception as e:
             logger.exception("Failed to retrieve package categories")
             return Response({
                'status': 'error',
                'data': None,
                'error': 'Internal server error: Failed to retrieve package categories'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request):
        try:
            serializer = PackageCategorySerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                logger.info("Created new package category successfully")
                return Response({
                    'status': 'success',
                    'data': serializer.data,
                    'error': None
                }, status=status.HTTP_201_CREATED)
            else:
                logger.warning(f"Failed to create package category: {serializer.errors}")
                return Response({
                    'status': 'error',
                    'data': None,
                    'error': serializer.errors
                }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
             logger.exception("Internal server error: Failed to create package category")
             return Response({
                'status': 'error',
                'data': None,
                'error': 'Internal server error: Failed to create package category'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class PackageCategoryDetail(APIView):
    def get(self, request, id):
        try:
            package_category = PackageCategory.objects.get(pk=id)
            serializer = PackageCategorySerializer(package_category)
            logger.info("Retrieved package category details successfully")
            return Response({
                'status': 'success',
                'data': serializer.data,
                'error': None
            }, status=status.HTTP_200_OK)
        except PackageCategory.DoesNotExist:
            logger.warning(f"Package category with id '{id}' not found")
            return Response({
                'status': 'error',
                'data': None,
                'error': 'Package category not found'
            }, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
             logger.exception("Internal server error: Failed to retrieve package category details")
             return Response({
                'status': 'error',
                'data': None,
                'error': 'Internal server error: Failed to retrieve package category details'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def put(self, request, id):
        try:
            package_category = PackageCategory.objects.get(pk=id)
            serializer = PackageCategorySerializer(package_category, data=request.data)
            if serializer.is_valid():
                serializer.save()
                logger.info("Updated package category details successfully")
                return Response({
                    'status': 'success',
                    'data': serializer.data,
                    'error': None
                }, status=status.HTTP_200_OK)
            else:
                logger.exception(f"Failed to update package category details: {serializer.errors}")
                return Response({
                    'status': 'error',
                    'data': None,
                    'error': serializer.errors
                }, status=status.HTTP_400_BAD_REQUEST)
        except PackageCategory.DoesNotExist:
            logger.warning(f"Package category with id '{id}' not found")
            return Response({
                'status': 'error',
                'data': None,
                'error': 'Package category not found'
            }, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
             logger.exception("Internal server error: Failed to update package category details")
             return Response({
                'status': 'error',
                'data': None,
                'error': 'Internal server error: Failed to update package category details'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request, id):
        try:
            package_category = PackageCategory.objects.get(pk=id)
            package_category.delete()
            logger.info("Deleted package category successfully")
            return Response({
                'status': 'success',
                'data': None,
                'error': None
            }, status=status.HTTP_204_NO_CONTENT)
        except PackageCategory.DoesNotExist:
            logger.warning(f"Package category with id '{id}' not found")
            return Response({
                'status': 'error',
                'data': None,
                'error': 'Package category not found'
            }, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
             logger.exception("Internal server error: Failed to delete package category")
             return Response({
                'status': 'error',
                'data': None,
                'error': 'Internal server error: Failed to delete package category'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)