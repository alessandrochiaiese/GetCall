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
from affiliate.api.services.affiliate_campaign_service import AffiliateCampaignService
from affiliate.models.affiliate_campaign import AffiliateCampaign
from affiliate.api.serializers import AffiliateCampaignSerializer

# Set up a logger
logger = logging.getLogger(__name__)

class AffiliateCampaignAPIView(APIView):
    permission_classes = [IsAuthenticated]  # [AllowAny]  or [IsAuthenticated]
    renderer_classes = [JSONRenderer]
    authentication_classes = [OAuth2Authentication]

    def __init__(self, *args, **kwargs):
        self.affiliate_campaign_service = AffiliateCampaignService()

    @swagger_auto_schema(
        operation_summary="List all affiliate_campaign",
        operation_description="Returns a list of all affiliate_campaign entries.",
        responses={
            200: openapi.Response('Successful Response', AffiliateCampaignSerializer(many=True)),
            500: 'Internal Server Error'
        },
        tags=['affiliate_campaign']
    )
    def get(self, request, affiliate_campaign_id = None):
        try:
            if affiliate_campaign_id == None:
                affiliate_campaign = AffiliateCampaign.objects.all()
                serializer = AffiliateCampaignSerializer(affiliate_campaign, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                affiliate_campaign = self.affiliate_campaign_service.get_affiliate_campaign(affiliate_campaign_id)
                serializer = AffiliateCampaignSerializer(affiliate_campaign)
                return Response(serializer.data, status=status.HTTP_200_OK)  
        except AffiliateCampaign.DoesNotExist as e:
            return Response({'error': str(e)}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.error(f"Error fetching affiliate_campaign: {str(e)}")
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @swagger_auto_schema(
        operation_summary="Create new affiliate_campaign",
        operation_description="Creates a new affiliate_campaign entry.",
        request_body=AffiliateCampaignSerializer,
        responses={
            201: openapi.Response('Created', AffiliateCampaignSerializer),
            400: 'Bad Request',
            500: 'Internal Server Error'
        },
        tags=['affiliate_campaign']
    )
    def post(self, request):
        try:
            serializer = AffiliateCampaignSerializer(data=request.data)
            if serializer.is_valid():
                affiliate_campaign = self.affiliate_campaign_service.create_affiliate_campaign(serializer.validated_data)
                return Response(AffiliateCampaignSerializer(affiliate_campaign).data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f"Error creating affiliate_campaign: {str(e)}")
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
 
    @swagger_auto_schema(
        operation_summary="Update a affiliate_campaign entry",
        operation_description="Updates a specific affiliate_campaign entry by ID.",
        request_body=AffiliateCampaignSerializer,
        responses={
            200: openapi.Response('Successful Response', AffiliateCampaignSerializer),
            400: 'Bad Request',
            404: 'Not Found',
            500: 'Internal Server Error'
        },
        tags=['affiliate_campaign']
    )
    def put(self, request, affiliate_campaign_id=None):
        try: 
            serializer = AffiliateCampaignSerializer(data=request.data)
            if serializer.is_valid():
                affiliate_campaign = self.affiliate_campaign_service.update_affiliate_campaign(affiliate_campaign_id, serializer.validated_data)
                return Response(AffiliateCampaignSerializer(affiliate_campaign).data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except AffiliateCampaign.DoesNotExist as e:
            return Response({'error': str(e)}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.error(f"Error updating affiliate_campaign: {str(e)}")
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @swagger_auto_schema(
        operation_summary="Delete a affiliate_campaign entry",
        operation_description="Deletes a specific affiliate_campaign entry by ID.",
        responses={
            204: 'No Content',
            404: 'Not Found',
            500: 'Internal Server Error'
        },
        tags=['affiliate_campaign']
    )
    def delete(self, request, affiliate_campaign_id=None):
        try:
            affiliate_campaign = self.affiliate_campaign_service.delete_affiliate_campaign(affiliate_campaign_id)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except AffiliateCampaign.DoesNotExist as e:
            return Response({'error': str(e)}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.error(f"Error deleting affiliate_campaign: {str(e)}")
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
