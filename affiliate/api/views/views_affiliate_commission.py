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
from affiliate.api.services.affiliate_commission_service import AffiliateCommissionService
from affiliate.models.affiliate_commission import AffiliateCommission
from affiliate.api.serializers import AffiliateCommissionSerializer

# Set up a logger
logger = logging.getLogger(__name__)

class AffiliateCommissionAPIView(APIView):
    permission_classes = [IsAuthenticated]  # [AllowAny]  or [IsAuthenticated]
    renderer_classes = [JSONRenderer]
    authentication_classes = [OAuth2Authentication]

    def __init__(self, *args, **kwargs):
        self.affiliate_commission_service = AffiliateCommissionService()

    @swagger_auto_schema(
        operation_summary="List all affiliate_commission",
        operation_description="Returns a list of all affiliate_commission entries.",
        responses={
            200: openapi.Response('Successful Response', AffiliateCommissionSerializer(many=True)),
            500: 'Internal Server Error'
        },
        tags=['affiliate_commission']
    )
    def get(self, request, affiliate_commission_id = None):
        try:
            if affiliate_commission_id == None:
                affiliate_commission = AffiliateCommission.objects.all()
                serializer = AffiliateCommissionSerializer(affiliate_commission, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                affiliate_commission = self.affiliate_commission_service.get_affiliate_commission(affiliate_commission_id)
                serializer = AffiliateCommissionSerializer(affiliate_commission)
                return Response(serializer.data, status=status.HTTP_200_OK)  
        except AffiliateCommission.DoesNotExist as e:
            return Response({'error': str(e)}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.error(f"Error fetching affiliate_commission: {str(e)}")
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @swagger_auto_schema(
        operation_summary="Create new affiliate_commission",
        operation_description="Creates a new affiliate_commission entry.",
        request_body=AffiliateCommissionSerializer,
        responses={
            201: openapi.Response('Created', AffiliateCommissionSerializer),
            400: 'Bad Request',
            500: 'Internal Server Error'
        },
        tags=['affiliate_commission']
    )
    def post(self, request):
        try:
            serializer = AffiliateCommissionSerializer(data=request.data)
            if serializer.is_valid():
                affiliate_commission = self.affiliate_commission_service.create_affiliate_commission(serializer.validated_data)
                return Response(AffiliateCommissionSerializer(affiliate_commission).data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f"Error creating affiliate_commission: {str(e)}")
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
 
    @swagger_auto_schema(
        operation_summary="Update a affiliate_commission entry",
        operation_description="Updates a specific affiliate_commission entry by ID.",
        request_body=AffiliateCommissionSerializer,
        responses={
            200: openapi.Response('Successful Response', AffiliateCommissionSerializer),
            400: 'Bad Request',
            404: 'Not Found',
            500: 'Internal Server Error'
        },
        tags=['affiliate_commission']
    )
    def put(self, request, affiliate_commission_id=None):
        try: 
            serializer = AffiliateCommissionSerializer(data=request.data)
            if serializer.is_valid():
                affiliate_commission = self.affiliate_commission_service.update_affiliate_commission(affiliate_commission_id, serializer.validated_data)
                return Response(AffiliateCommissionSerializer(affiliate_commission).data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except AffiliateCommission.DoesNotExist as e:
            return Response({'error': str(e)}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.error(f"Error updating affiliate_commission: {str(e)}")
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @swagger_auto_schema(
        operation_summary="Delete a affiliate_commission entry",
        operation_description="Deletes a specific affiliate_commission entry by ID.",
        responses={
            204: 'No Content',
            404: 'Not Found',
            500: 'Internal Server Error'
        },
        tags=['affiliate_commission']
    )
    def delete(self, request, affiliate_commission_id=None):
        try:
            affiliate_commission = self.affiliate_commission_service.delete_affiliate_commission(affiliate_commission_id)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except AffiliateCommission.DoesNotExist as e:
            return Response({'error': str(e)}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.error(f"Error deleting affiliate_commission: {str(e)}")
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
