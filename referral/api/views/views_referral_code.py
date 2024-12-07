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
from ..services.referral_code_service import ReferralCodeService
from ...models.referral_code import ReferralCode
from ..serializers import ReferralCodeSerializer

# Set up a logger
logger = logging.getLogger(__name__)

class ReferralCodeAPIView(APIView):
    permission_classes = [AllowAny]  # [AllowAny]  or [IsAuthenticated]
    renderer_classes = [JSONRenderer]
    authentication_classes = [OAuth2Authentication]

    def __init__(self, *args, **kwargs):
        self.referral_code_service = ReferralCodeService()

    @swagger_auto_schema(
        operation_summary="List all referral_code",
        operation_description="Returns a list of all referral_code entries.",
        responses={
            200: openapi.Response('Successful Response', ReferralCodeSerializer(many=True)),
            500: 'Internal Server Error'
        },
        tags=['referral_code']
    )
    def get(self, request, referral_code_id = None):
        try:
            if referral_code_id == None:
                referral_code = ReferralCode.objects.all()
                serializer = ReferralCodeSerializer(referral_code, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                referral_code = self.referral_code_service.get_referral_code(referral_code_id)
                serializer = ReferralCodeSerializer(referral_code)
                return Response(serializer.data, status=status.HTTP_200_OK)  
        except ReferralCode.DoesNotExist as e:
            return Response({'error': str(e)}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.error(f"Error fetching referral_code: {str(e)}")
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @swagger_auto_schema(
        operation_summary="Create new referral_code",
        operation_description="Creates a new referral_code entry.",
        request_body=ReferralCodeSerializer,
        responses={
            201: openapi.Response('Created', ReferralCodeSerializer),
            400: 'Bad Request',
            500: 'Internal Server Error'
        },
        tags=['referral_code']
    )
    def post(self, request):
        try:
            data=request.data
            data['url'] = request.host
            serializer = ReferralCodeSerializer(data=data)
            if serializer.is_valid():
                referral_code = self.referral_code_service.create_referral_code(serializer.validated_data)
                return Response(ReferralCodeSerializer(referral_code).data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f"Error creating referral_code: {str(e)}")
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
 
    @swagger_auto_schema(
        operation_summary="Update a referral_code entry",
        operation_description="Updates a specific referral_code entry by ID.",
        request_body=ReferralCodeSerializer,
        responses={
            200: openapi.Response('Successful Response', ReferralCodeSerializer),
            400: 'Bad Request',
            404: 'Not Found',
            500: 'Internal Server Error'
        },
        tags=['referral_code']
    )
    def put(self, request, referral_code_id=None):
        try: 
            serializer = ReferralCodeSerializer(data=request.data)
            if serializer.is_valid():
                referral_code = self.referral_code_service.update_referral_code(referral_code_id, serializer.validated_data)
                return Response(ReferralCodeSerializer(referral_code).data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except ReferralCode.DoesNotExist as e:
            return Response({'error': str(e)}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.error(f"Error updating referral_code: {str(e)}")
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @swagger_auto_schema(
        operation_summary="Delete a referral_code entry",
        operation_description="Deletes a specific referral_code entry by ID.",
        responses={
            204: 'No Content',
            404: 'Not Found',
            500: 'Internal Server Error'
        },
        tags=['referral_code']
    )
    def delete(self, request, referral_code_id=None):
        try:
            referral_code = self.referral_code_service.delete_referral_code(referral_code_id)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except ReferralCode.DoesNotExist as e:
            return Response({'error': str(e)}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.error(f"Error deleting referral_code: {str(e)}")
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
