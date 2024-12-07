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
from affiliate.api.services.affiliate_performance_service import AffiliatePerformanceService
from affiliate.models.affiliate_performance import AffiliatePerformance
from affiliate.api.serializers import AffiliatePerformanceSerializer

# Set up a logger
logger = logging.getLogger(__name__)

class AffiliatePerformanceAPIView(APIView):
    permission_classes = [IsAuthenticated]  # [AllowAny]  or [IsAuthenticated]
    renderer_classes = [JSONRenderer]
    authentication_classes = [OAuth2Authentication]

    def __init__(self, *args, **kwargs):
        self.affiliate_performance_service = AffiliatePerformanceService()

    @swagger_auto_schema(
        operation_summary="List all affiliate_performance",
        operation_description="Returns a list of all affiliate_performance entries.",
        responses={
            200: openapi.Response('Successful Response', AffiliatePerformanceSerializer(many=True)),
            500: 'Internal Server Error'
        },
        tags=['affiliate_performance']
    )
    def get(self, request, affiliate_performance_id = None):
        try:
            if affiliate_performance_id == None:
                affiliate_performance = AffiliatePerformance.objects.all()
                serializer = AffiliatePerformanceSerializer(affiliate_performance, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                affiliate_performance = self.affiliate_performance_service.get_affiliate_performance(affiliate_performance_id)
                serializer = AffiliatePerformanceSerializer(affiliate_performance)
                return Response(serializer.data, status=status.HTTP_200_OK)  
        except AffiliatePerformance.DoesNotExist as e:
            return Response({'error': str(e)}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.error(f"Error fetching affiliate_performance: {str(e)}")
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @swagger_auto_schema(
        operation_summary="Create new affiliate_performance",
        operation_description="Creates a new affiliate_performance entry.",
        request_body=AffiliatePerformanceSerializer,
        responses={
            201: openapi.Response('Created', AffiliatePerformanceSerializer),
            400: 'Bad Request',
            500: 'Internal Server Error'
        },
        tags=['affiliate_performance']
    )
    def post(self, request):
        try:
            serializer = AffiliatePerformanceSerializer(data=request.data)
            if serializer.is_valid():
                affiliate_performance = self.affiliate_performance_service.create_affiliate_performance(serializer.validated_data)
                return Response(AffiliatePerformanceSerializer(affiliate_performance).data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f"Error creating affiliate_performance: {str(e)}")
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
 
    @swagger_auto_schema(
        operation_summary="Update a affiliate_performance entry",
        operation_description="Updates a specific affiliate_performance entry by ID.",
        request_body=AffiliatePerformanceSerializer,
        responses={
            200: openapi.Response('Successful Response', AffiliatePerformanceSerializer),
            400: 'Bad Request',
            404: 'Not Found',
            500: 'Internal Server Error'
        },
        tags=['affiliate_performance']
    )
    def put(self, request, affiliate_performance_id=None):
        try: 
            serializer = AffiliatePerformanceSerializer(data=request.data)
            if serializer.is_valid():
                affiliate_performance = self.affiliate_performance_service.update_affiliate_performance(affiliate_performance_id, serializer.validated_data)
                return Response(AffiliatePerformanceSerializer(affiliate_performance).data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except AffiliatePerformance.DoesNotExist as e:
            return Response({'error': str(e)}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.error(f"Error updating affiliate_performance: {str(e)}")
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @swagger_auto_schema(
        operation_summary="Delete a affiliate_performance entry",
        operation_description="Deletes a specific affiliate_performance entry by ID.",
        responses={
            204: 'No Content',
            404: 'Not Found',
            500: 'Internal Server Error'
        },
        tags=['affiliate_performance']
    )
    def delete(self, request, affiliate_performance_id=None):
        try:
            affiliate_performance = self.affiliate_performance_service.delete_affiliate_performance(affiliate_performance_id)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except AffiliatePerformance.DoesNotExist as e:
            return Response({'error': str(e)}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.error(f"Error deleting affiliate_performance: {str(e)}")
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
