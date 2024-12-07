# referral_system/views.py

import logging
from referral.api.services.referral_program_service import ReferralProgramService
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework import status
from oauth2_provider.contrib.rest_framework import OAuth2Authentication
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from ...models import ReferralProgram
from ..serializers import ReferralProgramSerializer
from ..services.referral_service import ReferralService

# Set up a logger
logger = logging.getLogger(__name__)

class ReferralProgramAPIView(APIView):
    permission_classes = [AllowAny]  # [AllowAny]  or [IsAuthenticated]
    renderer_classes = [JSONRenderer]
    authentication_classes = [OAuth2Authentication]

    def __init__(self, *args, **kwargs):
        self.referral_program_service = ReferralProgramService()

    @swagger_auto_schema(
        operation_summary="List all referral_program",
        operation_description="Returns a list of all referral_program entries.",
        responses={
            200: openapi.Response('Successful Response', ReferralProgramSerializer(many=True)),
            500: 'Internal Server Error'
        },
        tags=['referral_program']
    )
    def get(self, request, referral_program_id = None):
        try:
            if referral_program_id == None:
                referral_program = ReferralProgram.objects.all()
                serializer = ReferralProgramSerializer(referral_program, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                referral_program = self.referral_program_service.get_referral_program(referral_program_id)
                serializer = ReferralProgramSerializer(referral_program)
                return Response(serializer.data, status=status.HTTP_200_OK)  
        except ReferralProgram.DoesNotExist as e:
            return Response({'error': str(e)}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.error(f"Error fetching referral_program: {str(e)}")
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @swagger_auto_schema(
        operation_summary="Create new referral_program",
        operation_description="Creates a new referral_program entry.",
        request_body=ReferralProgramSerializer,
        responses={
            201: openapi.Response('Created', ReferralProgramSerializer),
            400: 'Bad Request',
            500: 'Internal Server Error'
        },
        tags=['referral_program']
    )
    def post(self, request):
        try:
            serializer = ReferralProgramSerializer(data=request.data)
            if serializer.is_valid():
                referral_program = self.referral_program_service.create_referral_program(serializer.validated_data)
                return Response(ReferralProgramSerializer(referral_program).data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f"Error creating referral_program: {str(e)}")
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
 
    @swagger_auto_schema(
        operation_summary="Update a referral_program entry",
        operation_description="Updates a specific referral_program entry by ID.",
        request_body=ReferralProgramSerializer,
        responses={
            200: openapi.Response('Successful Response', ReferralProgramSerializer),
            400: 'Bad Request',
            404: 'Not Found',
            500: 'Internal Server Error'
        },
        tags=['referral_program']
    )
    def put(self, request, referral_program_id=None):
        try: 
            serializer = ReferralProgramSerializer(data=request.data)
            if serializer.is_valid():
                referral_program = self.referral_program_service.update_referral_program(referral_program_id, serializer.validated_data)
                return Response(ReferralProgramSerializer(referral_program).data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except ReferralProgram.DoesNotExist as e:
            return Response({'error': str(e)}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.error(f"Error updating referral_program: {str(e)}")
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @swagger_auto_schema(
        operation_summary="Delete a referral_program entry",
        operation_description="Deletes a specific referral_program entry by ID.",
        responses={
            204: 'No Content',
            404: 'Not Found',
            500: 'Internal Server Error'
        },
        tags=['referral_program']
    )
    def delete(self, request, referral_program_id=None):
        try:
            referral_program = self.referral_program_service.delete_referral_program(referral_program_id)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except ReferralProgram.DoesNotExist as e:
            return Response({'error': str(e)}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.error(f"Error deleting referral_program: {str(e)}")
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
