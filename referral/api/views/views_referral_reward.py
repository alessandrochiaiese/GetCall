# referral_system/views.py

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from referral.models import ReferralReward, Referral, ReferralReward
from referral.api.serializers import ReferralRewardSerializer, ReferralSerializer, ReferralRewardSerializer
from referral.api.services.referral_service import ReferralService

class ReferralRewardView(APIView):
    permission_classes = [permissions.IsAuthenticated]
# referral_system/views.py

import logging
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework import status
from oauth2_provider.contrib.rest_framework import OAuth2Authentication
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from ...models import ReferralReward
from ..serializers import ReferralRewardSerializer
from ..services.referral_service import ReferralService

# Set up a logger
logger = logging.getLogger(__name__)

class ReferralRewardAPIView(APIView):
    permission_classes = [AllowAny]  # [AllowAny]  or [IsAuthenticated]
    renderer_classes = [JSONRenderer]
    authentication_classes = [OAuth2Authentication]

    def __init__(self, *args, **kwargs):
        self.referral_reward_service = ReferralReward()

    @swagger_auto_schema(
        operation_summary="List all referral_reward",
        operation_description="Returns a list of all referral_reward entries.",
        responses={
            200: openapi.Response('Successful Response', ReferralRewardSerializer(many=True)),
            500: 'Internal Server Error'
        },
        tags=['referral_reward']
    )
    def get(self, request, referral_reward_id = None):
        try:
            if referral_reward_id == None:
                referral_reward = ReferralReward.objects.all()
                serializer = ReferralRewardSerializer(referral_reward, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                referral_reward = self.referral_reward_service.get_referral_reward(referral_reward_id)
                serializer = ReferralRewardSerializer(referral_reward)
                return Response(serializer.data, status=status.HTTP_200_OK)  
        except ReferralReward.DoesNotExist as e:
            return Response({'error': str(e)}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.error(f"Error fetching referral_reward: {str(e)}")
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @swagger_auto_schema(
        operation_summary="Create new referral_reward",
        operation_description="Creates a new referral_reward entry.",
        request_body=ReferralRewardSerializer,
        responses={
            201: openapi.Response('Created', ReferralRewardSerializer),
            400: 'Bad Request',
            500: 'Internal Server Error'
        },
        tags=['referral_reward']
    )
    def post(self, request):
        try:
            serializer = ReferralRewardSerializer(data=request.data)
            if serializer.is_valid():
                referral_reward = self.referral_reward_service.create_referral_reward(serializer.validated_data)
                return Response(ReferralRewardSerializer(referral_reward).data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f"Error creating referral_reward: {str(e)}")
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
 
    @swagger_auto_schema(
        operation_summary="Update a referral_reward entry",
        operation_description="Updates a specific referral_reward entry by ID.",
        request_body=ReferralRewardSerializer,
        responses={
            200: openapi.Response('Successful Response', ReferralRewardSerializer),
            400: 'Bad Request',
            404: 'Not Found',
            500: 'Internal Server Error'
        },
        tags=['referral_reward']
    )
    def put(self, request, referral_reward_id=None):
        try: 
            serializer = ReferralRewardSerializer(data=request.data)
            if serializer.is_valid():
                referral_reward = self.referral_reward_service.update_referral_reward(referral_reward_id, serializer.validated_data)
                return Response(ReferralRewardSerializer(referral_reward).data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except ReferralReward.DoesNotExist as e:
            return Response({'error': str(e)}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.error(f"Error updating referral_reward: {str(e)}")
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @swagger_auto_schema(
        operation_summary="Delete a referral_reward entry",
        operation_description="Deletes a specific referral_reward entry by ID.",
        responses={
            204: 'No Content',
            404: 'Not Found',
            500: 'Internal Server Error'
        },
        tags=['referral_reward']
    )
    def delete(self, request, referral_reward_id=None):
        try:
            referral_reward = self.referral_reward_service.delete_referral_reward(referral_reward_id)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except ReferralReward.DoesNotExist as e:
            return Response({'error': str(e)}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.error(f"Error deleting referral_reward: {str(e)}")
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
