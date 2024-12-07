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
from ..services.referral_settings_service import ReferralSettingsService
from ...models.referral_settings import ReferralSettings
from ..serializers import ReferralSettingsSerializer

# Set up a logger
logger = logging.getLogger(__name__)

class ReferralSettingsAPIView(APIView):
    permission_classes = [AllowAny]  # [AllowAny]  or [IsAuthenticated]
    renderer_classes = [JSONRenderer]
    authentication_classes = [OAuth2Authentication]

    def __init__(self, *args, **kwargs):
        self.referral_setting_service = ReferralSettingsService()

    @swagger_auto_schema(
        operation_summary="List all referral_setting",
        operation_description="Returns a list of all referral_setting entries.",
        responses={
            200: openapi.Response('Successful Response', ReferralSettingsSerializer(many=True)),
            500: 'Internal Server Error'
        },
        tags=['referral_setting']
    )
    def get(self, request, referral_setting_id = None):
        try:
            if referral_setting_id == None:
                referral_setting = ReferralSettings.objects.all()
                serializer = ReferralSettingsSerializer(referral_setting, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                referral_setting = self.referral_setting_service.get_referral_setting(referral_setting_id)
                serializer = ReferralSettingsSerializer(referral_setting)
                return Response(serializer.data, status=status.HTTP_200_OK)  
        except ReferralSettings.DoesNotExist as e:
            return Response({'error': str(e)}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.error(f"Error fetching referral_setting: {str(e)}")
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @swagger_auto_schema(
        operation_summary="Create new referral_setting",
        operation_description="Creates a new referral_setting entry.",
        request_body=ReferralSettingsSerializer,
        responses={
            201: openapi.Response('Created', ReferralSettingsSerializer),
            400: 'Bad Request',
            500: 'Internal Server Error'
        },
        tags=['referral_setting']
    )
    def post(self, request):
        try:
            serializer = ReferralSettingsSerializer(data=request.data)
            if serializer.is_valid():
                referral_setting = self.referral_setting_service.create_referral_setting(serializer.validated_data)
                return Response(ReferralSettingsSerializer(referral_setting).data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f"Error creating referral_setting: {str(e)}")
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
 
    @swagger_auto_schema(
        operation_summary="Update a referral_setting entry",
        operation_description="Updates a specific referral_setting entry by ID.",
        request_body=ReferralSettingsSerializer,
        responses={
            200: openapi.Response('Successful Response', ReferralSettingsSerializer),
            400: 'Bad Request',
            404: 'Not Found',
            500: 'Internal Server Error'
        },
        tags=['referral_setting']
    )
    def put(self, request, referral_setting_id=None):
        try: 
            serializer = ReferralSettingsSerializer(data=request.data)
            if serializer.is_valid():
                referral_setting = self.referral_setting_service.update_referral_setting(referral_setting_id, serializer.validated_data)
                return Response(ReferralSettingsSerializer(referral_setting).data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except ReferralSettings.DoesNotExist as e:
            return Response({'error': str(e)}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.error(f"Error updating referral_setting: {str(e)}")
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @swagger_auto_schema(
        operation_summary="Delete a referral_setting entry",
        operation_description="Deletes a specific referral_setting entry by ID.",
        responses={
            204: 'No Content',
            404: 'Not Found',
            500: 'Internal Server Error'
        },
        tags=['referral_setting']
    )
    def delete(self, request, referral_setting_id=None):
        try:
            referral_setting = self.referral_setting_service.delete_referral_setting(referral_setting_id)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except ReferralSettings.DoesNotExist as e:
            return Response({'error': str(e)}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.error(f"Error deleting referral_setting: {str(e)}")
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
