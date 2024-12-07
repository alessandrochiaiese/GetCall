import logging
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework import status
from oauth2_provider.contrib.rest_framework import OAuth2Authentication
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework import generics, permissions, serializers
from oauth2_provider.contrib.rest_framework import TokenHasReadWriteScope, TokenHasScope
from ..services.role_service import RoleService
from accounts.models import Role
from accounts.api.serializers import RoleSerializer

# Set up a logger
logger = logging.getLogger(__name__)

class GroupList(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated, TokenHasScope]
    required_scopes = ['roles']
    queryset = Role.objects.all()
    serializer_class = RoleSerializer

class RoleAPIView(APIView):
    permission_classes = [IsAuthenticated]  # [AllowAny]  or [IsAuthenticated]
    renderer_classes = [JSONRenderer]
    authentication_classes = [OAuth2Authentication]

    def __init__(self, *args, **kwargs):
        self.role_service = RoleService()

    @swagger_auto_schema(
        operation_summary="List all role",
        operation_description="Returns a list of all role entries.",
        responses={
            200: openapi.Response('Successful Response', RoleSerializer(many=True)),
            500: 'Internal Server Error'
        },
        tags=['role']
    )
    def get(self, request, pk = None):
        try:
            if pk == None:
                role = Role.objects.all()
                serializer = RoleSerializer(role, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                role = self.role_service.get_role(pk)
                serializer = RoleSerializer(role)
                return Response(serializer.data, status=status.HTTP_200_OK)  
        except Role.DoesNotExist as e:
            return Response({'error': str(e)}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.error(f"Error fetching role: {str(e)}")
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @swagger_auto_schema(
        operation_summary="Create new role",
        operation_description="Creates a new role entry.",
        request_body=RoleSerializer,
        responses={
            201: openapi.Response('Created', RoleSerializer),
            400: 'Bad Request',
            500: 'Internal Server Error'
        },
        tags=['role']
    )
    def post(self, request):
        try:
            serializer = RoleSerializer(data=request.data)
            if serializer.is_valid():
                role = self.role_service.create_role(serializer.validated_data)
                return Response(RoleSerializer(role).data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f"Error creating role: {str(e)}")
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    """@swagger_auto_schema(
        operation_summary="Retrieve a specific role entry",
        operation_description="Retrieves a specific role entry by ID.",
        responses={
            200: openapi.Response('Successful Response', RoleSerializer),
            404: 'Not Found',
            500: 'Internal Server Error'
        },
        tags=['role']
    )
    def retrieve(self, request, pk=None):
        try:
            role = self.role_service.get_role(pk=pk) 
            return Response(RoleSerializer(role).data, status=status.HTTP_200_OK)
        except Role.DoesNotExist as e:
            return Response({'error': str(e)}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.error(f"Error retrieving role: {str(e)}")
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)"""

    @swagger_auto_schema(
        operation_summary="Update a role entry",
        operation_description="Updates a specific role entry by ID.",
        request_body=RoleSerializer,
        responses={
            200: openapi.Response('Successful Response', RoleSerializer),
            400: 'Bad Request',
            404: 'Not Found',
            500: 'Internal Server Error'
        },
        tags=['role']
    )
    def put(self, request, role_id=None):
        try: 
            serializer = RoleSerializer(data=request.data)
            if serializer.is_valid():
                role = self.role_service.update_role(role_id, serializer.validated_data)
                return Response(RoleSerializer(role).data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Role.DoesNotExist as e:
            return Response({'error': str(e)}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.error(f"Error updating role: {str(e)}")
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @swagger_auto_schema(
        operation_summary="Delete a role entry",
        operation_description="Deletes a specific role entry by ID.",
        responses={
            204: 'No Content',
            404: 'Not Found',
            500: 'Internal Server Error'
        },
        tags=['role']
    )
    def delete(self, request, pk=None):
        try:
            role = self.role_service.delete_role(pk)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Role.DoesNotExist as e:
            return Response({'error': str(e)}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.error(f"Error deleting role: {str(e)}")
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
