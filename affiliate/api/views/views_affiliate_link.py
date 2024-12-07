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
from affiliate.api.services.affiliate_link_service import AffiliateLinkService
from affiliate.models.affiliate_link import AffiliateLink
from affiliate.api.serializers import AffiliateLinkSerializer

# Set up a logger
logger = logging.getLogger(__name__)

class AffiliateLinkAPIView(APIView):
    permission_classes = [IsAuthenticated]  # [AllowAny]  or [IsAuthenticated]
    renderer_classes = [JSONRenderer]
    authentication_classes = [OAuth2Authentication]

    def __init__(self, *args, **kwargs):
        self.affiliate_link_service = AffiliateLinkService()

    @swagger_auto_schema(
        operation_summary="List all affiliate_link",
        operation_description="Returns a list of all affiliate_link entries.",
        responses={
            200: openapi.Response('Successful Response', AffiliateLinkSerializer(many=True)),
            500: 'Internal Server Error'
        },
        tags=['affiliate_link']
    )
    def get(self, request, affiliate_link_id = None):
        try:
            if affiliate_link_id == None:
                affiliate_link = AffiliateLink.objects.all()
                serializer = AffiliateLinkSerializer(affiliate_link, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                affiliate_link = self.affiliate_link_service.get_affiliate_link(affiliate_link_id)
                serializer = AffiliateLinkSerializer(affiliate_link)
                return Response(serializer.data, status=status.HTTP_200_OK)  
        except AffiliateLink.DoesNotExist as e:
            return Response({'error': str(e)}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.error(f"Error fetching affiliate_link: {str(e)}")
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @swagger_auto_schema(
        operation_summary="Create new affiliate_link",
        operation_description="Creates a new affiliate_link entry.",
        request_body=AffiliateLinkSerializer,
        responses={
            201: openapi.Response('Created', AffiliateLinkSerializer),
            400: 'Bad Request',
            500: 'Internal Server Error'
        },
        tags=['affiliate_link']
    )
    def post(self, request):
        try:
            serializer = AffiliateLinkSerializer(data=request.data)
            if serializer.is_valid():
                affiliate_link = self.affiliate_link_service.create_affiliate_link(serializer.validated_data)
                return Response(AffiliateLinkSerializer(affiliate_link).data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f"Error creating affiliate_link: {str(e)}")
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
 
    @swagger_auto_schema(
        operation_summary="Update a affiliate_link entry",
        operation_description="Updates a specific affiliate_link entry by ID.",
        request_body=AffiliateLinkSerializer,
        responses={
            200: openapi.Response('Successful Response', AffiliateLinkSerializer),
            400: 'Bad Request',
            404: 'Not Found',
            500: 'Internal Server Error'
        },
        tags=['affiliate_link']
    )
    def put(self, request, affiliate_link_id=None):
        try: 
            serializer = AffiliateLinkSerializer(data=request.data)
            if serializer.is_valid():
                affiliate_link = self.affiliate_link_service.update_affiliate_link(affiliate_link_id, serializer.validated_data)
                return Response(AffiliateLinkSerializer(affiliate_link).data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except AffiliateLink.DoesNotExist as e:
            return Response({'error': str(e)}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.error(f"Error updating affiliate_link: {str(e)}")
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @swagger_auto_schema(
        operation_summary="Delete a affiliate_link entry",
        operation_description="Deletes a specific affiliate_link entry by ID.",
        responses={
            204: 'No Content',
            404: 'Not Found',
            500: 'Internal Server Error'
        },
        tags=['affiliate_link']
    )
    def delete(self, request, affiliate_link_id=None):
        try:
            affiliate_link = self.affiliate_link_service.delete_affiliate_link(affiliate_link_id)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except AffiliateLink.DoesNotExist as e:
            return Response({'error': str(e)}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.error(f"Error deleting affiliate_link: {str(e)}")
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
