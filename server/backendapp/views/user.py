from ..serializers import UserSerializer
from ..models import User
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view

class UserList(APIView):
    def get(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response({
            'status': 'success',
            'data': serializer.data,
            'error': None,
        }, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = UserSerializer(data=request.data)
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

class UserDetail(APIView):
    def get(self, request, id):
        try:
            user = User.objects.get(pk=id)
        except User.DoesNotExist:
            return Response({
                'status': 'error',
                'data': None,
                'error': 'User not found'
            }, status=status.HTTP_404_NOT_FOUND)

        serializer = UserSerializer(user)
        return Response({
            'status': 'success',
            'data': serializer.data,
            'error': None
        }, status=status.HTTP_200_OK)

    def put(self, request, id):
        try:
            user = User.objects.get(pk=id)
        except User.DoesNotExist:
            return Response({
                'status': 'error',
                'data': None,
                'error': 'User not found'
            }, status=status.HTTP_404_NOT_FOUND)

        serializer = UserSerializer(user, data=request.data)
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
            user = User.objects.get(pk=id)
        except User.DoesNotExist:
            return Response({
                'status': 'error',
                'data': None,
                'error': 'User not found'
            }, status=status.HTTP_404_NOT_FOUND)

        user.delete()
        return Response({
            'status': 'success',
            'data': None,
            'error': None
        }, status=status.HTTP_204_NO_CONTENT)