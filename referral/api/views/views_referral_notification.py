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
from ...models import ReferralNotification
from ..serializers import ReferralNotificationSerializer
from ..services.referral_service import ReferralService

# Set up a logger
logger = logging.getLogger(__name__)

class ReferralNotificationAPIView(APIView):
    permission_classes = [AllowAny]  # [AllowAny]  or [IsAuthenticated]
    renderer_classes = [JSONRenderer]
    authentication_classes = [OAuth2Authentication]

    def __init__(self, *args, **kwargs):
        self.referral_notification_service = ReferralNotification()

    @swagger_auto_schema(
        operation_summary="List all referral_notification",
        operation_description="Returns a list of all referral_notification entries.",
        responses={
            200: openapi.Response('Successful Response', ReferralNotificationSerializer(many=True)),
            500: 'Internal Server Error'
        },
        tags=['referral_notification']
    )
    def get(self, request, referral_notification_id = None):
        try:
            if referral_notification_id == None:
                referral_notification = ReferralNotification.objects.all()
                serializer = ReferralNotificationSerializer(referral_notification, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                referral_notification = self.referral_notification_service.get_referral_notification(referral_notification_id)
                serializer = ReferralNotificationSerializer(referral_notification)
                return Response(serializer.data, status=status.HTTP_200_OK)  
        except ReferralNotification.DoesNotExist as e:
            return Response({'error': str(e)}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.error(f"Error fetching referral_notification: {str(e)}")
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @swagger_auto_schema(
        operation_summary="Create new referral_notification",
        operation_description="Creates a new referral_notification entry.",
        request_body=ReferralNotificationSerializer,
        responses={
            201: openapi.Response('Created', ReferralNotificationSerializer),
            400: 'Bad Request',
            500: 'Internal Server Error'
        },
        tags=['referral_notification']
    )
    def post(self, request):
        try:
            serializer = ReferralNotificationSerializer(data=request.data)
            if serializer.is_valid():
                referral_notification = self.referral_notification_service.create_referral_notification(serializer.validated_data)
                return Response(ReferralNotificationSerializer(referral_notification).data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f"Error creating referral_notification: {str(e)}")
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
 
    @swagger_auto_schema(
        operation_summary="Update a referral_notification entry",
        operation_description="Updates a specific referral_notification entry by ID.",
        request_body=ReferralNotificationSerializer,
        responses={
            200: openapi.Response('Successful Response', ReferralNotificationSerializer),
            400: 'Bad Request',
            404: 'Not Found',
            500: 'Internal Server Error'
        },
        tags=['referral_notification']
    )
    def put(self, request, referral_notification_id=None):
        try: 
            serializer = ReferralNotificationSerializer(data=request.data)
            if serializer.is_valid():
                referral_notification = self.referral_notification_service.update_referral_notification(referral_notification_id, serializer.validated_data)
                return Response(ReferralNotificationSerializer(referral_notification).data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except ReferralNotification.DoesNotExist as e:
            return Response({'error': str(e)}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.error(f"Error updating referral_notification: {str(e)}")
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @swagger_auto_schema(
        operation_summary="Delete a referral_notification entry",
        operation_description="Deletes a specific referral_notification entry by ID.",
        responses={
            204: 'No Content',
            404: 'Not Found',
            500: 'Internal Server Error'
        },
        tags=['referral_notification']
    )
    def delete(self, request, referral_notification_id=None):
        try:
            referral_notification = self.referral_notification_service.delete_referral_notification(referral_notification_id)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except ReferralNotification.DoesNotExist as e:
            return Response({'error': str(e)}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.error(f"Error deleting referral_notification: {str(e)}")
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
