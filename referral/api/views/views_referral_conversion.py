import logging
from django.http import JsonResponse
from referral.api.serializers import ReferralConversionSerializer
from referral.models.referral_conversion import ReferralConversion
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework import status
from oauth2_provider.contrib.rest_framework import OAuth2Authentication
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from ..services.referral_conversion_service import ReferralConversionService 

# Set up a logger
logger = logging.getLogger(__name__)

class ReferralConversionAPIView(APIView):
    permission_classes = [AllowAny]  # [AllowAny]  or [IsAuthenticated]
    renderer_classes = [JSONRenderer]
    authentication_classes = [OAuth2Authentication]

    def __init__(self, *args, **kwargs):
        self.referral_conversion_service = ReferralConversionService()

    @swagger_auto_schema(
        operation_summary="List all referral_conversion",
        operation_description="Returns a list of all referral_conversion entries.",
        responses={
            200: openapi.Response('Successful Response', ReferralConversionSerializer(many=True)),
            500: 'Internal Server Error'
        },
        tags=['referral_conversion']
    )
    def get(self, request, referral_conversion_id = None):
        try:
            if referral_conversion_id == None:
                referral_conversion = ReferralConversion.objects.all()
                serializer = ReferralConversionSerializer(referral_conversion, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                referral_conversion = self.referral_conversion_service.get_referral_conversion(referral_conversion_id)
                serializer = ReferralConversionSerializer(referral_conversion)
                return Response(serializer.data, status=status.HTTP_200_OK)  
        except ReferralConversion.DoesNotExist as e:
            return Response({'error': str(e)}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.error(f"Error fetching referral_conversion: {str(e)}")
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @swagger_auto_schema(
        operation_summary="Create new referral_conversion",
        operation_description="Creates a new referral_conversion entry.",
        request_body=ReferralConversionSerializer,
        responses={
            201: openapi.Response('Created', ReferralConversionSerializer),
            400: 'Bad Request',
            500: 'Internal Server Error'
        },
        tags=['referral_conversion']
    )
    def post(self, request):
        try:
            serializer = ReferralConversionSerializer(data=request.data)
            if serializer.is_valid():
                referral_conversion = self.referral_conversion_service.create_referral_conversion(serializer.validated_data)
                return Response(ReferralConversionSerializer(referral_conversion).data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f"Error creating referral_conversion: {str(e)}")
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
 
    @swagger_auto_schema(
        operation_summary="Update a referral_conversion entry",
        operation_description="Updates a specific referral_conversion entry by ID.",
        request_body=ReferralConversionSerializer,
        responses={
            200: openapi.Response('Successful Response', ReferralConversionSerializer),
            400: 'Bad Request',
            404: 'Not Found',
            500: 'Internal Server Error'
        },
        tags=['referral_conversion']
    )
    def put(self, request, referral_conversion_id=None):
        try: 
            serializer = ReferralConversionSerializer(data=request.data)
            if serializer.is_valid():
                referral_conversion = self.referral_conversion_service.update_referral_conversion(referral_conversion_id, serializer.validated_data)
                return Response(ReferralConversionSerializer(referral_conversion).data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except ReferralConversion.DoesNotExist as e:
            return Response({'error': str(e)}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.error(f"Error updating referral_conversion: {str(e)}")
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @swagger_auto_schema(
        operation_summary="Delete a referral_conversion entry",
        operation_description="Deletes a specific referral_conversion entry by ID.",
        responses={
            204: 'No Content',
            404: 'Not Found',
            500: 'Internal Server Error'
        },
        tags=['referral_conversion']
    )
    def delete(self, request, referral_conversion_id=None):
        try:
            referral_conversion = self.referral_conversion_service.delete_referral_conversion(referral_conversion_id)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except ReferralConversion.DoesNotExist as e:
            return Response({'error': str(e)}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.error(f"Error deleting referral_conversion: {str(e)}")
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
