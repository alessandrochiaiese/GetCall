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
from affiliate.api.services.affiliate_reward_service import AffiliateRewardService
from affiliate.models.affiliate_reward import AffiliateReward
from affiliate.api.serializers import AffiliateRewardSerializer

# Set up a logger
logger = logging.getLogger(__name__)

class AffiliateRewardAPIView(APIView):
    permission_classes = [IsAuthenticated]  # [AllowAny]  or [IsAuthenticated]
    renderer_classes = [JSONRenderer]
    authentication_classes = [OAuth2Authentication]

    def __init__(self, *args, **kwargs):
        self.affiliate_reward_service = AffiliateRewardService()

    @swagger_auto_schema(
        operation_summary="List all affiliate_reward",
        operation_description="Returns a list of all affiliate_reward entries.",
        responses={
            200: openapi.Response('Successful Response', AffiliateRewardSerializer(many=True)),
            500: 'Internal Server Error'
        },
        tags=['affiliate_reward']
    )
    def get(self, request, affiliate_reward_id = None):
        try:
            if affiliate_reward_id == None:
                affiliate_reward = AffiliateReward.objects.all()
                serializer = AffiliateRewardSerializer(affiliate_reward, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                affiliate_reward = self.affiliate_reward_service.get_affiliate_reward(affiliate_reward_id)
                serializer = AffiliateRewardSerializer(affiliate_reward)
                return Response(serializer.data, status=status.HTTP_200_OK)  
        except AffiliateReward.DoesNotExist as e:
            return Response({'error': str(e)}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.error(f"Error fetching affiliate_reward: {str(e)}")
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @swagger_auto_schema(
        operation_summary="Create new affiliate_reward",
        operation_description="Creates a new affiliate_reward entry.",
        request_body=AffiliateRewardSerializer,
        responses={
            201: openapi.Response('Created', AffiliateRewardSerializer),
            400: 'Bad Request',
            500: 'Internal Server Error'
        },
        tags=['affiliate_reward']
    )
    def post(self, request):
        try:
            serializer = AffiliateRewardSerializer(data=request.data)
            if serializer.is_valid():
                affiliate_reward = self.affiliate_reward_service.create_affiliate_reward(serializer.validated_data)
                return Response(AffiliateRewardSerializer(affiliate_reward).data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f"Error creating affiliate_reward: {str(e)}")
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
 
    @swagger_auto_schema(
        operation_summary="Update a affiliate_reward entry",
        operation_description="Updates a specific affiliate_reward entry by ID.",
        request_body=AffiliateRewardSerializer,
        responses={
            200: openapi.Response('Successful Response', AffiliateRewardSerializer),
            400: 'Bad Request',
            404: 'Not Found',
            500: 'Internal Server Error'
        },
        tags=['affiliate_reward']
    )
    def put(self, request, affiliate_reward_id=None):
        try: 
            serializer = AffiliateRewardSerializer(data=request.data)
            if serializer.is_valid():
                affiliate_reward = self.affiliate_reward_service.update_affiliate_reward(affiliate_reward_id, serializer.validated_data)
                return Response(AffiliateRewardSerializer(affiliate_reward).data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except AffiliateReward.DoesNotExist as e:
            return Response({'error': str(e)}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.error(f"Error updating affiliate_reward: {str(e)}")
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @swagger_auto_schema(
        operation_summary="Delete a affiliate_reward entry",
        operation_description="Deletes a specific affiliate_reward entry by ID.",
        responses={
            204: 'No Content',
            404: 'Not Found',
            500: 'Internal Server Error'
        },
        tags=['affiliate_reward']
    )
    def delete(self, request, affiliate_reward_id=None):
        try:
            affiliate_reward = self.affiliate_reward_service.delete_affiliate_reward(affiliate_reward_id)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except AffiliateReward.DoesNotExist as e:
            return Response({'error': str(e)}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.error(f"Error deleting affiliate_reward: {str(e)}")
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
