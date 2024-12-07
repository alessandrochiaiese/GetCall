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
from ..services.referral_stats_service import ReferralStatsService
from ...models.referral_stats import ReferralStats
from ..serializers import ReferralStatsSerializer

# Set up a logger
logger = logging.getLogger(__name__)

class ReferralStatsAPIView(APIView):
    permission_classes = [AllowAny]  # [AllowAny]  or [IsAuthenticated]
    renderer_classes = [JSONRenderer]
    authentication_classes = [OAuth2Authentication]

    def __init__(self, *args, **kwargs):
        self.referral_stat_service = ReferralStatsService()

    @swagger_auto_schema(
        operation_summary="List all referral_stat",
        operation_description="Returns a list of all referral_stat entries.",
        responses={
            200: openapi.Response('Successful Response', ReferralStatsSerializer(many=True)),
            500: 'Internal Server Error'
        },
        tags=['referral_stat']
    )
    def get(self, request, referral_stat_id = None):
        try:
            if referral_stat_id == None:
                referral_stat = ReferralStats.objects.all()
                serializer = ReferralStatsSerializer(referral_stat, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                referral_stat = self.referral_stat_service.get_referral_stat(referral_stat_id)
                serializer = ReferralStatsSerializer(referral_stat)
                return Response(serializer.data, status=status.HTTP_200_OK)  
        except ReferralStats.DoesNotExist as e:
            return Response({'error': str(e)}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.error(f"Error fetching referral_stat: {str(e)}")
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @swagger_auto_schema(
        operation_summary="Create new referral_stat",
        operation_description="Creates a new referral_stat entry.",
        request_body=ReferralStatsSerializer,
        responses={
            201: openapi.Response('Created', ReferralStatsSerializer),
            400: 'Bad Request',
            500: 'Internal Server Error'
        },
        tags=['referral_stat']
    )
    def post(self, request):
        try:
            serializer = ReferralStatsSerializer(data=request.data)
            if serializer.is_valid():
                referral_stat = self.referral_stat_service.create_referral_stat(serializer.validated_data)
                return Response(ReferralStatsSerializer(referral_stat).data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f"Error creating referral_stat: {str(e)}")
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
 
    @swagger_auto_schema(
        operation_summary="Update a referral_stat entry",
        operation_description="Updates a specific referral_stat entry by ID.",
        request_body=ReferralStatsSerializer,
        responses={
            200: openapi.Response('Successful Response', ReferralStatsSerializer),
            400: 'Bad Request',
            404: 'Not Found',
            500: 'Internal Server Error'
        },
        tags=['referral_stat']
    )
    def put(self, request, referral_stat_id=None):
        try: 
            serializer = ReferralStatsSerializer(data=request.data)
            if serializer.is_valid():
                referral_stat = self.referral_stat_service.update_referral_stat(referral_stat_id, serializer.validated_data)
                return Response(ReferralStatsSerializer(referral_stat).data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except ReferralStats.DoesNotExist as e:
            return Response({'error': str(e)}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.error(f"Error updating referral_stat: {str(e)}")
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @swagger_auto_schema(
        operation_summary="Delete a referral_stat entry",
        operation_description="Deletes a specific referral_stat entry by ID.",
        responses={
            204: 'No Content',
            404: 'Not Found',
            500: 'Internal Server Error'
        },
        tags=['referral_stat']
    )
    def delete(self, request, referral_stat_id=None):
        try:
            referral_stat = self.referral_stat_service.delete_referral_stat(referral_stat_id)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except ReferralStats.DoesNotExist as e:
            return Response({'error': str(e)}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.error(f"Error deleting referral_stat: {str(e)}")
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
