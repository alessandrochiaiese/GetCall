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
from affiliate.api.services.affiliate_tier_service import AffiliateTierService
from affiliate.models.affiliate_tier import AffiliateTier
from affiliate.api.serializers import AffiliateTierSerializer

# Set up a logger
logger = logging.getLogger(__name__)

class AffiliateTierAPIView(APIView):
    permission_classes = [IsAuthenticated]  # [AllowAny]  or [IsAuthenticated]
    renderer_classes = [JSONRenderer]
    authentication_classes = [OAuth2Authentication]

    def __init__(self, *args, **kwargs):
        self.affiliate_tier_service = AffiliateTierService()

    @swagger_auto_schema(
        operation_summary="List all affiliate_tier",
        operation_description="Returns a list of all affiliate_tier entries.",
        responses={
            200: openapi.Response('Successful Response', AffiliateTierSerializer(many=True)),
            500: 'Internal Server Error'
        },
        tags=['affiliate_tier']
    )
    def get(self, request, affiliate_tier_id = None):
        try:
            if affiliate_tier_id == None:
                affiliate_tier = AffiliateTier.objects.all()
                serializer = AffiliateTierSerializer(affiliate_tier, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                affiliate_tier = self.affiliate_tier_service.get_affiliate_tier(affiliate_tier_id)
                serializer = AffiliateTierSerializer(affiliate_tier)
                return Response(serializer.data, status=status.HTTP_200_OK)  
        except AffiliateTier.DoesNotExist as e:
            return Response({'error': str(e)}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.error(f"Error fetching affiliate_tier: {str(e)}")
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @swagger_auto_schema(
        operation_summary="Create new affiliate_tier",
        operation_description="Creates a new affiliate_tier entry.",
        request_body=AffiliateTierSerializer,
        responses={
            201: openapi.Response('Created', AffiliateTierSerializer),
            400: 'Bad Request',
            500: 'Internal Server Error'
        },
        tags=['affiliate_tier']
    )
    def post(self, request):
        try:
            serializer = AffiliateTierSerializer(data=request.data)
            if serializer.is_valid():
                affiliate_tier = self.affiliate_tier_service.create_affiliate_tier(serializer.validated_data)
                return Response(AffiliateTierSerializer(affiliate_tier).data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f"Error creating affiliate_tier: {str(e)}")
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
 
    @swagger_auto_schema(
        operation_summary="Update a affiliate_tier entry",
        operation_description="Updates a specific affiliate_tier entry by ID.",
        request_body=AffiliateTierSerializer,
        responses={
            200: openapi.Response('Successful Response', AffiliateTierSerializer),
            400: 'Bad Request',
            404: 'Not Found',
            500: 'Internal Server Error'
        },
        tags=['affiliate_tier']
    )
    def put(self, request, affiliate_tier_id=None):
        try: 
            serializer = AffiliateTierSerializer(data=request.data)
            if serializer.is_valid():
                affiliate_tier = self.affiliate_tier_service.update_affiliate_tier(affiliate_tier_id, serializer.validated_data)
                return Response(AffiliateTierSerializer(affiliate_tier).data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except AffiliateTier.DoesNotExist as e:
            return Response({'error': str(e)}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.error(f"Error updating affiliate_tier: {str(e)}")
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @swagger_auto_schema(
        operation_summary="Delete a affiliate_tier entry",
        operation_description="Deletes a specific affiliate_tier entry by ID.",
        responses={
            204: 'No Content',
            404: 'Not Found',
            500: 'Internal Server Error'
        },
        tags=['affiliate_tier']
    )
    def delete(self, request, affiliate_tier_id=None):
        try:
            affiliate_tier = self.affiliate_tier_service.delete_affiliate_tier(affiliate_tier_id)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except AffiliateTier.DoesNotExist as e:
            return Response({'error': str(e)}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.error(f"Error deleting affiliate_tier: {str(e)}")
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
