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
from affiliate.api.services.affiliate_setting_service import AffiliateSettingsService
from affiliate.models.affiliate_settings import AffiliateSettings
from affiliate.api.serializers import AffiliateSettingsSerializer

# Set up a logger
logger = logging.getLogger(__name__)

class AffiliateSettingsAPIView(APIView):
    permission_classes = [IsAuthenticated]  # [AllowAny]  or [IsAuthenticated]
    renderer_classes = [JSONRenderer]
    authentication_classes = [OAuth2Authentication]

    def __init__(self, *args, **kwargs):
        self.affiliate_settings_service = AffiliateSettingsService()

    @swagger_auto_schema(
        operation_summary="List all affiliate_settings",
        operation_description="Returns a list of all affiliate_settings entries.",
        responses={
            200: openapi.Response('Successful Response', AffiliateSettingsSerializer(many=True)),
            500: 'Internal Server Error'
        },
        tags=['affiliate_settings']
    )
    def get(self, request, affiliate_settings_id = None):
        try:
            if affiliate_settings_id == None:
                affiliate_settings = AffiliateSettings.objects.all()
                serializer = AffiliateSettingsSerializer(affiliate_settings, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                affiliate_settings = self.affiliate_settings_service.get_affiliate_settings(affiliate_settings_id)
                serializer = AffiliateSettingsSerializer(affiliate_settings)
                return Response(serializer.data, status=status.HTTP_200_OK)  
        except AffiliateSettings.DoesNotExist as e:
            return Response({'error': str(e)}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.error(f"Error fetching affiliate_settings: {str(e)}")
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @swagger_auto_schema(
        operation_summary="Create new affiliate_settings",
        operation_description="Creates a new affiliate_settings entry.",
        request_body=AffiliateSettingsSerializer,
        responses={
            201: openapi.Response('Created', AffiliateSettingsSerializer),
            400: 'Bad Request',
            500: 'Internal Server Error'
        },
        tags=['affiliate_settings']
    )
    def post(self, request):
        try:
            serializer = AffiliateSettingsSerializer(data=request.data)
            if serializer.is_valid():
                affiliate_settings = self.affiliate_settings_service.create_affiliate_settings(serializer.validated_data)
                return Response(AffiliateSettingsSerializer(affiliate_settings).data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f"Error creating affiliate_settings: {str(e)}")
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
 
    @swagger_auto_schema(
        operation_summary="Update a affiliate_settings entry",
        operation_description="Updates a specific affiliate_settings entry by ID.",
        request_body=AffiliateSettingsSerializer,
        responses={
            200: openapi.Response('Successful Response', AffiliateSettingsSerializer),
            400: 'Bad Request',
            404: 'Not Found',
            500: 'Internal Server Error'
        },
        tags=['affiliate_settings']
    )
    def put(self, request, affiliate_settings_id=None):
        try: 
            serializer = AffiliateSettingsSerializer(data=request.data)
            if serializer.is_valid():
                affiliate_settings = self.affiliate_settings_service.update_affiliate_settings(affiliate_settings_id, serializer.validated_data)
                return Response(AffiliateSettingsSerializer(affiliate_settings).data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except AffiliateSettings.DoesNotExist as e:
            return Response({'error': str(e)}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.error(f"Error updating affiliate_settings: {str(e)}")
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @swagger_auto_schema(
        operation_summary="Delete a affiliate_settings entry",
        operation_description="Deletes a specific affiliate_settings entry by ID.",
        responses={
            204: 'No Content',
            404: 'Not Found',
            500: 'Internal Server Error'
        },
        tags=['affiliate_settings']
    )
    def delete(self, request, affiliate_settings_id=None):
        try:
            affiliate_settings = self.affiliate_settings_service.delete_affiliate_settings(affiliate_settings_id)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except AffiliateSettings.DoesNotExist as e:
            return Response({'error': str(e)}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.error(f"Error deleting affiliate_settings: {str(e)}")
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
