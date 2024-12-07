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
from ..services.referral_transaction_service import ReferralTransactionService
from ...models.referral_transaction import ReferralTransaction
from ..serializers import ReferralTransactionSerializer

# Set up a logger
logger = logging.getLogger(__name__)

class ReferralTransactionAPIView(APIView):
    permission_classes = [AllowAny]  # [AllowAny]  or [IsAuthenticated]
    renderer_classes = [JSONRenderer]
    authentication_classes = [OAuth2Authentication]

    def __init__(self, *args, **kwargs):
        self.referral_transaction_service = ReferralTransactionService()

    @swagger_auto_schema(
        operation_summary="List all referral_transaction",
        operation_description="Returns a list of all referral_transaction entries.",
        responses={
            200: openapi.Response('Successful Response', ReferralTransactionSerializer(many=True)),
            500: 'Internal Server Error'
        },
        tags=['referral_transaction']
    )
    def get(self, request, referral_transaction_id = None):
        try:
            if referral_transaction_id == None:
                referral_transaction = ReferralTransaction.objects.all()
                serializer = ReferralTransactionSerializer(referral_transaction, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                referral_transaction = self.referral_transaction_service.get_referral_transaction(referral_transaction_id)
                serializer = ReferralTransactionSerializer(referral_transaction)
                return Response(serializer.data, status=status.HTTP_200_OK)  
        except ReferralTransaction.DoesNotExist as e:
            return Response({'error': str(e)}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.error(f"Error fetching referral_transaction: {str(e)}")
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @swagger_auto_schema(
        operation_summary="Create new referral_transaction",
        operation_description="Creates a new referral_transaction entry.",
        request_body=ReferralTransactionSerializer,
        responses={
            201: openapi.Response('Created', ReferralTransactionSerializer),
            400: 'Bad Request',
            500: 'Internal Server Error'
        },
        tags=['referral_transaction']
    )
    def post(self, request):
        try:
            serializer = ReferralTransactionSerializer(data=request.data)
            if serializer.is_valid():
                referral_transaction = self.referral_transaction_service.create_referral_transaction(serializer.validated_data)
                return Response(ReferralTransactionSerializer(referral_transaction).data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f"Error creating referral_transaction: {str(e)}")
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
 
    @swagger_auto_schema(
        operation_summary="Update a referral_transaction entry",
        operation_description="Updates a specific referral_transaction entry by ID.",
        request_body=ReferralTransactionSerializer,
        responses={
            200: openapi.Response('Successful Response', ReferralTransactionSerializer),
            400: 'Bad Request',
            404: 'Not Found',
            500: 'Internal Server Error'
        },
        tags=['referral_transaction']
    )
    def put(self, request, referral_transaction_id=None):
        try: 
            serializer = ReferralTransactionSerializer(data=request.data)
            if serializer.is_valid():
                referral_transaction = self.referral_transaction_service.update_referral_transaction(referral_transaction_id, serializer.validated_data)
                return Response(ReferralTransactionSerializer(referral_transaction).data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except ReferralTransaction.DoesNotExist as e:
            return Response({'error': str(e)}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.error(f"Error updating referral_transaction: {str(e)}")
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @swagger_auto_schema(
        operation_summary="Delete a referral_transaction entry",
        operation_description="Deletes a specific referral_transaction entry by ID.",
        responses={
            204: 'No Content',
            404: 'Not Found',
            500: 'Internal Server Error'
        },
        tags=['referral_transaction']
    )
    def delete(self, request, referral_transaction_id=None):
        try:
            referral_transaction = self.referral_transaction_service.delete_referral_transaction(referral_transaction_id)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except ReferralTransaction.DoesNotExist as e:
            return Response({'error': str(e)}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.error(f"Error deleting referral_transaction: {str(e)}")
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
