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
from dashboard.api.services.profile_service import ProfileService
from dashboard.models.profile import Profile
from dashboard.api.serializers import ProfileSerializer

# Set up a logger
logger = logging.getLogger(__name__)

class ProfileAPIView(APIView):
    permission_classes = [AllowAny]  # [AllowAny]  or [IsAuthenticated]
    renderer_classes = [JSONRenderer]
    authentication_classes = [OAuth2Authentication]

    def __init__(self, *args, **kwargs):
        self.profile_service = ProfileService()

    @swagger_auto_schema(
        operation_summary="List all profile",
        operation_description="Returns a list of all profile entries.",
        responses={
            200: openapi.Response('Successful Response', ProfileSerializer(many=True)),
            500: 'Internal Server Error'
        },
        tags=['profile']
    )
    def get(self, request, pk = None):
        try:
            if pk == None:
                profile = Profile.objects.all()
                serializer = ProfileSerializer(profile, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                profile = self.profile_service.get_profile(pk)
                serializer = ProfileSerializer(profile)
                return Response(serializer.data, status=status.HTTP_200_OK)  
        except Profile.DoesNotExist as e:
            return Response({'error': str(e)}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.error(f"Error fetching profile: {str(e)}")
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @swagger_auto_schema(
        operation_summary="Create new profile",
        operation_description="Creates a new profile entry.",
        request_body=ProfileSerializer,
        responses={
            201: openapi.Response('Created', ProfileSerializer),
            400: 'Bad Request',
            500: 'Internal Server Error'
        },
        tags=['profile']
    )
    def post(self, request):
        try:
            serializer = ProfileSerializer(data=request.data)
            if serializer.is_valid():
                profile = self.profile_service.create_profile(serializer.validated_data)
                return Response(ProfileSerializer(profile).data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f"Error creating profile: {str(e)}")
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
 
    @swagger_auto_schema(
        operation_summary="Update a profile entry",
        operation_description="Updates a specific profile entry by ID.",
        request_body=ProfileSerializer,
        responses={
            200: openapi.Response('Successful Response', ProfileSerializer),
            400: 'Bad Request',
            404: 'Not Found',
            500: 'Internal Server Error'
        },
        tags=['profile']
    )
    def put(self, request, profile_id=None):
        try: 
            profile = Profile.objects.get(id=profile_id)
            serializer = ProfileSerializer(instance=profile, data=request.data, partial=True)

            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Profile.DoesNotExist:
            # Profilo non trovato
            error_message = f"Profile with id {profile_id} does not exist."
            logger.error(error_message)
            return Response({'error': error_message}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            # Qualsiasi altro errore generico
            logger.error(f"Error updating profile: {str(e)}")
            return Response({'error': 'An unexpected error occurred.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @swagger_auto_schema(
        operation_summary="Delete a profile entry",
        operation_description="Deletes a specific profile entry by ID.",
        responses={
            204: 'No Content',
            404: 'Not Found',
            500: 'Internal Server Error'
        },
        tags=['profile']
    )
    def delete(self, request, pk=None):
        try:
            profile = self.profile_service.delete_profile(pk)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Profile.DoesNotExist as e:
            return Response({'error': str(e)}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.error(f"Error deleting profile: {str(e)}")
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
