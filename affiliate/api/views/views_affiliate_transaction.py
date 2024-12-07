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
from affiliate.api.services.affiliate_transaction_service import AffiliateTransactionService
from affiliate.models.affiliate_transaction import AffiliateTransaction
from affiliate.api.serializers import AffiliateTransactionSerializer

# Set up a logger
logger = logging.getLogger(__name__)

class AffiliateTransactionAPIView(APIView):
    permission_classes = [IsAuthenticated]  # [AllowAny]  or [IsAuthenticated]
    renderer_classes = [JSONRenderer]
    authentication_classes = [OAuth2Authentication]

    def __init__(self, *args, **kwargs):
        self.affiliate_transaction_service = AffiliateTransactionService()

    @swagger_auto_schema(
        operation_summary="List all affiliate_transaction",
        operation_description="Returns a list of all affiliate_transaction entries.",
        responses={
            200: openapi.Response('Successful Response', AffiliateTransactionSerializer(many=True)),
            500: 'Internal Server Error'
        },
        tags=['affiliate_transaction']
    )
    def get(self, request, pk = None):
        try:
            if pk == None:
                affiliate_transaction = AffiliateTransaction.objects.all()
                serializer = AffiliateTransactionSerializer(affiliate_transaction, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                affiliate_transaction = self.affiliate_transaction_service.get_affiliate_transaction(pk)
                serializer = AffiliateTransactionSerializer(affiliate_transaction)
                return Response(serializer.data, status=status.HTTP_200_OK)  
        except AffiliateTransaction.DoesNotExist as e:
            return Response({'error': str(e)}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.error(f"Error fetching affiliate_transaction: {str(e)}")
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @swagger_auto_schema(
        operation_summary="Create new affiliate_transaction",
        operation_description="Creates a new affiliate_transaction entry.",
        request_body=AffiliateTransactionSerializer,
        responses={
            201: openapi.Response('Created', AffiliateTransactionSerializer),
            400: 'Bad Request',
            500: 'Internal Server Error'
        },
        tags=['affiliate_transaction']
    )
    def post(self, request):
        try:
            serializer = AffiliateTransactionSerializer(data=request.data)
            if serializer.is_valid():
                affiliate_transaction = self.affiliate_transaction_service.create_affiliate_transaction(serializer.validated_data)
                return Response(AffiliateTransactionSerializer(affiliate_transaction).data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f"Error creating affiliate_transaction: {str(e)}")
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
 
    @swagger_auto_schema(
        operation_summary="Update a affiliate_transaction entry",
        operation_description="Updates a specific affiliate_transaction entry by ID.",
        request_body=AffiliateTransactionSerializer,
        responses={
            200: openapi.Response('Successful Response', AffiliateTransactionSerializer),
            400: 'Bad Request',
            404: 'Not Found',
            500: 'Internal Server Error'
        },
        tags=['affiliate_transaction']
    )
    def put(self, request, affiliate_transaction_id=None):
        try: 
            serializer = AffiliateTransactionSerializer(data=request.data)
            if serializer.is_valid():
                affiliate_transaction = self.affiliate_transaction_service.update_affiliate_transaction(affiliate_transaction_id, serializer.validated_data)
                return Response(AffiliateTransactionSerializer(affiliate_transaction).data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except AffiliateTransaction.DoesNotExist as e:
            return Response({'error': str(e)}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.error(f"Error updating affiliate_transaction: {str(e)}")
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @swagger_auto_schema(
        operation_summary="Delete a affiliate_transaction entry",
        operation_description="Deletes a specific affiliate_transaction entry by ID.",
        responses={
            204: 'No Content',
            404: 'Not Found',
            500: 'Internal Server Error'
        },
        tags=['affiliate_transaction']
    )
    def delete(self, request, pk=None):
        try:
            affiliate_transaction = self.affiliate_transaction_service.delete_affiliate_transaction(pk)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except AffiliateTransaction.DoesNotExist as e:
            return Response({'error': str(e)}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.error(f"Error deleting affiliate_transaction: {str(e)}")
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
