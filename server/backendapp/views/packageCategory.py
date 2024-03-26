from ..serializers import PackageCategorySerializer
from ..models import PackageCategory
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view

class PackageCategoryList(APIView):
    def get(self, request):
        package_categories = PackageCategory.objects.all()
        serializer = PackageCategorySerializer(package_categories, many=True)
        return Response({
            'status': 'success',
            'data': serializer.data,
            'error': None,
        }, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = PackageCategorySerializer(data=request.data)
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

class PackageCategoryDetail(APIView):
    def get(self, request, id):
        try:
            package_category = PackageCategory.objects.get(pk=id)
        except PackageCategory.DoesNotExist:
            return Response({
                'status': 'error',
                'data': None,
                'error': 'Package category not found'
            }, status=status.HTTP_404_NOT_FOUND)

        serializer = PackageCategorySerializer(package_category)
        return Response({
            'status': 'success',
            'data': serializer.data,
            'error': None
        }, status=status.HTTP_200_OK)

    def put(self, request, id):
        try:
            package_category = PackageCategory.objects.get(pk=id)
        except PackageCategory.DoesNotExist:
            return Response({
                'status': 'error',
                'data': None,
                'error': 'Package category not found'
            }, status=status.HTTP_404_NOT_FOUND)

        serializer = PackageCategorySerializer(package_category, data=request.data)
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
            package_category = PackageCategory.objects.get(pk=id)
        except PackageCategory.DoesNotExist:
            return Response({
                'status': 'error',
                'data': None,
                'error': 'Package category not found'
            }, status=status.HTTP_404_NOT_FOUND)

        package_category.delete()
        return Response({
            'status': 'success',
            'data': None,
            'error': None
        }, status=status.HTTP_204_NO_CONTENT)