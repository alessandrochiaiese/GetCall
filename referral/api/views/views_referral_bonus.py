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
from ..services.referral_bonus_service import ReferralBonusService
from ...models.referral_bonus import ReferralBonus
from ..serializers import ReferralBonusSerializer

# Set up a logger
logger = logging.getLogger(__name__)

class ReferralBonusAPIView(APIView):
    permission_classes = [AllowAny]  # [AllowAny]  or [IsAuthenticated]
    renderer_classes = [JSONRenderer]
    authentication_classes = [OAuth2Authentication]

    def __init__(self, *args, **kwargs):
        self.referral_bonus_service = ReferralBonusService()

    @swagger_auto_schema(
        operation_summary="List all referral_bonus",
        operation_description="Returns a list of all referral_bonus entries.",
        responses={
            200: openapi.Response('Successful Response', ReferralBonusSerializer(many=True)),
            500: 'Internal Server Error'
        },
        tags=['referral_bonus']
    )
    def get(self, request, referral_bonus_id = None):
        try:
            if referral_bonus_id == None:
                referral_bonus = ReferralBonus.objects.all()
                serializer = ReferralBonusSerializer(referral_bonus, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                referral_bonus = self.referral_bonus_service.get_referral_bonus(referral_bonus_id)
                serializer = ReferralBonusSerializer(referral_bonus)
                return Response(serializer.data, status=status.HTTP_200_OK)  
        except ReferralBonus.DoesNotExist as e:
            return Response({'error': str(e)}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.error(f"Error fetching referral_bonus: {str(e)}")
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @swagger_auto_schema(
        operation_summary="Create new referral_bonus",
        operation_description="Creates a new referral_bonus entry.",
        request_body=ReferralBonusSerializer,
        responses={
            201: openapi.Response('Created', ReferralBonusSerializer),
            400: 'Bad Request',
            500: 'Internal Server Error'
        },
        tags=['referral_bonus']
    )
    def post(self, request):
        try:
            serializer = ReferralBonusSerializer(data=request.data)
            if serializer.is_valid():
                referral_bonus = self.referral_bonus_service.create_referral_bonus(serializer.validated_data)
                return Response(ReferralBonusSerializer(referral_bonus).data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f"Error creating referral_bonus: {str(e)}")
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
 
    @swagger_auto_schema(
        operation_summary="Update a referral_bonus entry",
        operation_description="Updates a specific referral_bonus entry by ID.",
        request_body=ReferralBonusSerializer,
        responses={
            200: openapi.Response('Successful Response', ReferralBonusSerializer),
            400: 'Bad Request',
            404: 'Not Found',
            500: 'Internal Server Error'
        },
        tags=['referral_bonus']
    )
    def put(self, request, referral_bonus_id=None):
        try: 
            serializer = ReferralBonusSerializer(data=request.data)
            if serializer.is_valid():
                referral_bonus = self.referral_bonus_service.update_referral_bonus(referral_bonus_id, serializer.validated_data)
                return Response(ReferralBonusSerializer(referral_bonus).data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except ReferralBonus.DoesNotExist as e:
            return Response({'error': str(e)}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.error(f"Error updating referral_bonus: {str(e)}")
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @swagger_auto_schema(
        operation_summary="Delete a referral_bonus entry",
        operation_description="Deletes a specific referral_bonus entry by ID.",
        responses={
            204: 'No Content',
            404: 'Not Found',
            500: 'Internal Server Error'
        },
        tags=['referral_bonus']
    )
    def delete(self, request, referral_bonus_id=None):
        try:
            referral_bonus = self.referral_bonus_service.delete_referral_bonus(referral_bonus_id)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except ReferralBonus.DoesNotExist as e:
            return Response({'error': str(e)}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.error(f"Error deleting referral_bonus: {str(e)}")
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
