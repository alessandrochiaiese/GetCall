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
from affiliate.api.services.affiliate_payout_service import AffiliatePayoutService
from affiliate.models.affiliate_payout import AffiliatePayout
from affiliate.api.serializers import AffiliatePayoutSerializer

# Set up a logger
logger = logging.getLogger(__name__)

class AffiliatePayoutAPIView(APIView):
    permission_classes = [IsAuthenticated]  # [AllowAny]  or [IsAuthenticated]
    renderer_classes = [JSONRenderer]
    authentication_classes = [OAuth2Authentication]

    def __init__(self, *args, **kwargs):
        self.affiliate_payout_service = AffiliatePayoutService()

    @swagger_auto_schema(
        operation_summary="List all affiliate_payout",
        operation_description="Returns a list of all affiliate_payout entries.",
        responses={
            200: openapi.Response('Successful Response', AffiliatePayoutSerializer(many=True)),
            500: 'Internal Server Error'
        },
        tags=['affiliate_payout']
    )
    def get(self, request, affiliate_payout_id = None):
        try:
            if affiliate_payout_id == None:
                affiliate_payout = AffiliatePayout.objects.all()
                serializer = AffiliatePayoutSerializer(affiliate_payout, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                affiliate_payout = self.affiliate_payout_service.get_affiliate_payout(affiliate_payout_id)
                serializer = AffiliatePayoutSerializer(affiliate_payout)
                return Response(serializer.data, status=status.HTTP_200_OK)  
        except AffiliatePayout.DoesNotExist as e:
            return Response({'error': str(e)}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.error(f"Error fetching affiliate_payout: {str(e)}")
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @swagger_auto_schema(
        operation_summary="Create new affiliate_payout",
        operation_description="Creates a new affiliate_payout entry.",
        request_body=AffiliatePayoutSerializer,
        responses={
            201: openapi.Response('Created', AffiliatePayoutSerializer),
            400: 'Bad Request',
            500: 'Internal Server Error'
        },
        tags=['affiliate_payout']
    )
    def post(self, request):
        try:
            serializer = AffiliatePayoutSerializer(data=request.data)
            if serializer.is_valid():
                affiliate_payout = self.affiliate_payout_service.create_affiliate_payout(serializer.validated_data)
                return Response(AffiliatePayoutSerializer(affiliate_payout).data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f"Error creating affiliate_payout: {str(e)}")
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
 
    @swagger_auto_schema(
        operation_summary="Update a affiliate_payout entry",
        operation_description="Updates a specific affiliate_payout entry by ID.",
        request_body=AffiliatePayoutSerializer,
        responses={
            200: openapi.Response('Successful Response', AffiliatePayoutSerializer),
            400: 'Bad Request',
            404: 'Not Found',
            500: 'Internal Server Error'
        },
        tags=['affiliate_payout']
    )
    def put(self, request, affiliate_payout_id=None):
        try: 
            serializer = AffiliatePayoutSerializer(data=request.data)
            if serializer.is_valid():
                affiliate_payout = self.affiliate_payout_service.update_affiliate_payout(affiliate_payout_id, serializer.validated_data)
                return Response(AffiliatePayoutSerializer(affiliate_payout).data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except AffiliatePayout.DoesNotExist as e:
            return Response({'error': str(e)}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.error(f"Error updating affiliate_payout: {str(e)}")
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @swagger_auto_schema(
        operation_summary="Delete a affiliate_payout entry",
        operation_description="Deletes a specific affiliate_payout entry by ID.",
        responses={
            204: 'No Content',
            404: 'Not Found',
            500: 'Internal Server Error'
        },
        tags=['affiliate_payout']
    )
    def delete(self, request, affiliate_payout_id=None):
        try:
            affiliate_payout = self.affiliate_payout_service.delete_affiliate_payout(affiliate_payout_id)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except AffiliatePayout.DoesNotExist as e:
            return Response({'error': str(e)}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.error(f"Error deleting affiliate_payout: {str(e)}")
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
