# referral_system/views.py

import logging
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework import status
from oauth2_provider.contrib.rest_framework import OAuth2Authentication
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from ...models import ReferralProgramPartecipation
from ..serializers import ReferralProgramPartecipationSerializer
from ..services.referral_service import ReferralService

# Set up a logger
logger = logging.getLogger(__name__)

class ReferralProgramPartecipationAPIView(APIView):
    permission_classes = [IsAuthenticated]  # [AllowAny]  or [IsAuthenticated]
    renderer_classes = [JSONRenderer]
    authentication_classes = [OAuth2Authentication]

    def __init__(self, *args, **kwargs):
        self.referral_program_partecipation_service = ReferralProgramPartecipation()

    @swagger_auto_schema(
        operation_summary="List all referral_program_partecipation",
        operation_description="Returns a list of all referral_program_partecipation entries.",
        responses={
            200: openapi.Response('Successful Response', ReferralProgramPartecipationSerializer(many=True)),
            500: 'Internal Server Error'
        },
        tags=['referral_program_partecipation']
    )
    def get(self, request, referral_program_partecipation_id = None):
        try:
            if referral_program_partecipation_id == None:
                referral_program_partecipation = ReferralProgramPartecipation.objects.all()
                serializer = ReferralProgramPartecipationSerializer(referral_program_partecipation, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                referral_program_partecipation = self.referral_program_partecipation_service.get_referral_program_partecipation(referral_program_partecipation_id)
                serializer = ReferralProgramPartecipationSerializer(referral_program_partecipation)
                return Response(serializer.data, status=status.HTTP_200_OK)  
        except ReferralProgramPartecipation.DoesNotExist as e:
            return Response({'error': str(e)}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.error(f"Error fetching referral_program_partecipation: {str(e)}")
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @swagger_auto_schema(
        operation_summary="Create new referral_program_partecipation",
        operation_description="Creates a new referral_program_partecipation entry.",
        request_body=ReferralProgramPartecipationSerializer,
        responses={
            201: openapi.Response('Created', ReferralProgramPartecipationSerializer),
            400: 'Bad Request',
            500: 'Internal Server Error'
        },
        tags=['referral_program_partecipation']
    )
    def post(self, request):
        try:
            serializer = ReferralProgramPartecipationSerializer(data=request.data)
            if serializer.is_valid():
                referral_program_partecipation = self.referral_program_partecipation_service.create_referral_program_partecipation(serializer.validated_data)
                return Response(ReferralProgramPartecipationSerializer(referral_program_partecipation).data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f"Error creating referral_program_partecipation: {str(e)}")
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
 
    @swagger_auto_schema(
        operation_summary="Update a referral_program_partecipation entry",
        operation_description="Updates a specific referral_program_partecipation entry by ID.",
        request_body=ReferralProgramPartecipationSerializer,
        responses={
            200: openapi.Response('Successful Response', ReferralProgramPartecipationSerializer),
            400: 'Bad Request',
            404: 'Not Found',
            500: 'Internal Server Error'
        },
        tags=['referral_program_partecipation']
    )
    def put(self, request, referral_program_partecipation_id=None):
        try: 
            serializer = ReferralProgramPartecipationSerializer(data=request.data)
            if serializer.is_valid():
                referral_program_partecipation = self.referral_program_partecipation_service.update_referral_program_partecipation(referral_program_partecipation_id, serializer.validated_data)
                return Response(ReferralProgramPartecipationSerializer(referral_program_partecipation).data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except ReferralProgramPartecipation.DoesNotExist as e:
            return Response({'error': str(e)}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.error(f"Error updating referral_program_partecipation: {str(e)}")
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @swagger_auto_schema(
        operation_summary="Delete a referral_program_partecipation entry",
        operation_description="Deletes a specific referral_program_partecipation entry by ID.",
        responses={
            204: 'No Content',
            404: 'Not Found',
            500: 'Internal Server Error'
        },
        tags=['referral_program_partecipation']
    )
    def delete(self, request, referral_program_partecipation_id=None):
        try:
            referral_program_partecipation = self.referral_program_partecipation_service.delete_referral_program_partecipation(referral_program_partecipation_id)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except ReferralProgramPartecipation.DoesNotExist as e:
            return Response({'error': str(e)}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.error(f"Error deleting referral_program_partecipation: {str(e)}")
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
