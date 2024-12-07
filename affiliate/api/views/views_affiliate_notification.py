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
from affiliate.api.services.affiliate_notification_service import AffiliateNotificationService
from affiliate.models.affiliate_notification import AffiliateNotification
from affiliate.api.serializers import AffiliateNotificationSerializer

# Set up a logger
logger = logging.getLogger(__name__)

class AffiliateNotificationAPIView(APIView):
    permission_classes = [IsAuthenticated]  # [AllowAny]  or [IsAuthenticated]
    renderer_classes = [JSONRenderer]
    authentication_classes = [OAuth2Authentication]

    def __init__(self, *args, **kwargs):
        self.affiliate_notification_service = AffiliateNotificationService()

    @swagger_auto_schema(
        operation_summary="List all affiliate_notification",
        operation_description="Returns a list of all affiliate_notification entries.",
        responses={
            200: openapi.Response('Successful Response', AffiliateNotificationSerializer(many=True)),
            500: 'Internal Server Error'
        },
        tags=['affiliate_notification']
    )
    def get(self, request, affiliate_notification_id = None):
        try:
            if affiliate_notification_id == None:
                affiliate_notification = AffiliateNotification.objects.all()
                serializer = AffiliateNotificationSerializer(affiliate_notification, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                affiliate_notification = self.affiliate_notification_service.get_affiliate_notification(affiliate_notification_id)
                serializer = AffiliateNotificationSerializer(affiliate_notification)
                return Response(serializer.data, status=status.HTTP_200_OK)  
        except AffiliateNotification.DoesNotExist as e:
            return Response({'error': str(e)}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.error(f"Error fetching affiliate_notification: {str(e)}")
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @swagger_auto_schema(
        operation_summary="Create new affiliate_notification",
        operation_description="Creates a new affiliate_notification entry.",
        request_body=AffiliateNotificationSerializer,
        responses={
            201: openapi.Response('Created', AffiliateNotificationSerializer),
            400: 'Bad Request',
            500: 'Internal Server Error'
        },
        tags=['affiliate_notification']
    )
    def post(self, request):
        try:
            serializer = AffiliateNotificationSerializer(data=request.data)
            if serializer.is_valid():
                affiliate_notification = self.affiliate_notification_service.create_affiliate_notification(serializer.validated_data)
                return Response(AffiliateNotificationSerializer(affiliate_notification).data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f"Error creating affiliate_notification: {str(e)}")
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
 
    @swagger_auto_schema(
        operation_summary="Update a affiliate_notification entry",
        operation_description="Updates a specific affiliate_notification entry by ID.",
        request_body=AffiliateNotificationSerializer,
        responses={
            200: openapi.Response('Successful Response', AffiliateNotificationSerializer),
            400: 'Bad Request',
            404: 'Not Found',
            500: 'Internal Server Error'
        },
        tags=['affiliate_notification']
    )
    def put(self, request, affiliate_notification_id=None):
        try: 
            serializer = AffiliateNotificationSerializer(data=request.data)
            if serializer.is_valid():
                affiliate_notification = self.affiliate_notification_service.update_affiliate_notification(affiliate_notification_id, serializer.validated_data)
                return Response(AffiliateNotificationSerializer(affiliate_notification).data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except AffiliateNotification.DoesNotExist as e:
            return Response({'error': str(e)}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.error(f"Error updating affiliate_notification: {str(e)}")
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @swagger_auto_schema(
        operation_summary="Delete a affiliate_notification entry",
        operation_description="Deletes a specific affiliate_notification entry by ID.",
        responses={
            204: 'No Content',
            404: 'Not Found',
            500: 'Internal Server Error'
        },
        tags=['affiliate_notification']
    )
    def delete(self, request, affiliate_notification_id=None):
        try:
            affiliate_notification = self.affiliate_notification_service.delete_affiliate_notification(affiliate_notification_id)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except AffiliateNotification.DoesNotExist as e:
            return Response({'error': str(e)}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.error(f"Error deleting affiliate_notification: {str(e)}")
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
