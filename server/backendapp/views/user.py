from ..serializers import CreateUserSerializer, UpdateUserSerializer
from ..models import User
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view

class UserList(APIView):
    def get(self, request):
        try:
            users = User.objects.all()
            serializer = CreateUserSerializer(users, many=True)
            return Response({
                'status': 'success',
                'data': serializer.data,
                'error': None,
            }, status=status.HTTP_200_OK)
        except Exception as e:
             return Response({
                'status': 'error',
                'data': None,
                'error': 'Failed to retrieve users'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request):
        try:
            serializer = CreateUserSerializer(data=request.data)
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
                'error': 'Failed to create user'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class UserDetail(APIView):
    def get(self, request, id):
        try:
            user = User.objects.get(pk=id)
            serializer = CreateUserSerializer(user)
            return Response({
                'status': 'success',
                'data': serializer.data,
                'error': None
            }, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({
                'status': 'error',
                'data': None,
                'error': 'User not found'
            }, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
             return Response({
                'status': 'error',
                'data': None,
                'error': 'Failed to retrieve user details'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def put(self, request, id):
        try:
            user = User.objects.get(pk=id)
            serializer = UpdateUserSerializer(user, data=request.data)
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
        except User.DoesNotExist:
            return Response({
                'status': 'error',
                'data': None,
                'error': 'User not found'
            }, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
             return Response({
                'status': 'error',
                'data': None,
                'error': 'Failed to update user details'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request, id):
        try:
            user = User.objects.get(pk=id)
            user.delete()
            return Response({
                'status': 'success',
                'data': None,
                'error': None
            }, status=status.HTTP_204_NO_CONTENT)
        except User.DoesNotExist:
            return Response({
                'status': 'error',
                'data': None,
                'error': 'User not found'
            }, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
             return Response({
                'status': 'error',
                'data': None,
                'error': 'Failed to delete user'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

