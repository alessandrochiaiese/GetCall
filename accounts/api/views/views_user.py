import logging
from django.http import JsonResponse 
from ..services.user_service import UserService
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework import status
from oauth2_provider.contrib.rest_framework import OAuth2Authentication
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics, permissions, serializers
from oauth2_provider.contrib.rest_framework import TokenHasReadWriteScope, TokenHasScope
from drf_yasg import openapi
from accounts.models.user import User
from accounts.api.serializers import UserSerializer

# Set up a logger
logger = logging.getLogger(__name__) 

class UserList(generics.ListCreateAPIView):
    permission_classes = [AllowAny] #, permissions,IsAuthenticated, TokenHasReadWriteScope]
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserDetails(generics.RetrieveAPIView):
    permission_classes = [AllowAny] #, permissions,IsAuthenticated,  TokenHasReadWriteScope]
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserAPIView(APIView):
    permission_classes = [AllowAny]  # [AllowAny]  or [IsAuthenticated]
    renderer_classes = [JSONRenderer]
    authentication_classes = [OAuth2Authentication]

    def __init__(self, *args, **kwargs):
        self.user_service = UserService()

    @swagger_auto_schema(
        operation_summary="List all user",
        operation_description="Returns a list of all user entries.",
        responses={
            200: openapi.Response('Successful Response', UserSerializer(many=True)),
            500: 'Internal Server Error'
        },
        tags=['user']
    )
    def get(self, request, pk=None):
        try:
            if pk == None:
                user = User.objects.all()
                serializer = UserSerializer(user, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                user = self.user_service.get_user(pk)
                serializer = UserSerializer(user)
                return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(f"Error fetching user: {str(e)}")
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @swagger_auto_schema(
        operation_summary="Create new user",
        operation_description="Creates a new user entry.",
        request_body=UserSerializer,
        responses={
            201: openapi.Response('Created', UserSerializer),
            400: 'Bad Request',
            500: 'Internal Server Error'
        },
        tags=['user']
    )
    def post(self, request):
        try:
            serializer = UserSerializer(data=request.data)
            if serializer.is_valid():
                user = self.user_service.create_user(serializer.validated_data)
                return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f"Error creating user: {str(e)}")
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    """@swagger_auto_schema(
        operation_summary="Retrieve a specific user entry",
        operation_description="Retrieves a specific user entry by ID.",
        responses={
            200: openapi.Response('Successful Response', UserSerializer),
            404: 'Not Found',
            500: 'Internal Server Error'
        },
        tags=['user']
    )
    def retrieve(self, request, pk=None):
        try:
            user = self.user_service.get_user(pk)
            serializer = UserSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.error(f"Error retrieving user: {str(e)}")
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)"""

    @swagger_auto_schema(
        operation_summary="Update a user entry",
        operation_description="Updates a specific user entry by ID.",
        request_body=UserSerializer,
        responses={
            200: openapi.Response('Successful Response', UserSerializer),
            400: 'Bad Request',
            404: 'Not Found',
            500: 'Internal Server Error'
        },
        tags=['user']
    )
    def put(self, request, pk=None):
        try:
            user = User.objects.get(pk=pk)
            serializer = UserSerializer(data=request.data)
            if serializer.is_valid():
                user = self.user_service.create_user(serializer.validated_data)
                return Response(UserSerializer(user).data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.error(f"Error updating user: {str(e)}")
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @swagger_auto_schema(
        operation_summary="Delete a user entry",
        operation_description="Deletes a specific user entry by ID.",
        responses={
            204: 'No Content',
            404: 'Not Found',
            500: 'Internal Server Error'
        },
        tags=['user']
    )
    def delete(self, request, pk=None):
        try:
            user = self.user_service.delete_user(pk)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.error(f"Error deleting user: {str(e)}")
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
