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
from affiliate.api.services.affiliate_audit_service import AffiliateAuditService
from affiliate.models.affiliate_audit import AffiliateAudit
from affiliate.api.serializers import AffiliateAuditSerializer

# Set up a logger
logger = logging.getLogger(__name__)

class AffiliateAuditAPIView(APIView):
    permission_classes = [IsAuthenticated]  # [AllowAny]  or [IsAuthenticated]
    renderer_classes = [JSONRenderer]
    authentication_classes = [OAuth2Authentication]

    def __init__(self, *args, **kwargs):
        self.affiliate_audit_service = AffiliateAuditService()

    @swagger_auto_schema(
        operation_summary="List all affiliate_audit",
        operation_description="Returns a list of all affiliate_audit entries.",
        responses={
            200: openapi.Response('Successful Response', AffiliateAuditSerializer(many=True)),
            500: 'Internal Server Error'
        },
        tags=['affiliate_audit']
    )
    def get(self, request, affiliate_audit_id = None):
        try:
            if affiliate_audit_id == None:
                affiliate_audit = AffiliateAudit.objects.all()
                serializer = AffiliateAuditSerializer(affiliate_audit, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                affiliate_audit = self.affiliate_audit_service.get_affiliate_audit(affiliate_audit_id)
                serializer = AffiliateAuditSerializer(affiliate_audit)
                return Response(serializer.data, status=status.HTTP_200_OK)  
        except AffiliateAudit.DoesNotExist as e:
            return Response({'error': str(e)}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.error(f"Error fetching affiliate_audit: {str(e)}")
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @swagger_auto_schema(
        operation_summary="Create new affiliate_audit",
        operation_description="Creates a new affiliate_audit entry.",
        request_body=AffiliateAuditSerializer,
        responses={
            201: openapi.Response('Created', AffiliateAuditSerializer),
            400: 'Bad Request',
            500: 'Internal Server Error'
        },
        tags=['affiliate_audit']
    )
    def post(self, request):
        try:
            serializer = AffiliateAuditSerializer(data=request.data)
            if serializer.is_valid():
                affiliate_audit = self.affiliate_audit_service.create_affiliate_audit(serializer.validated_data)
                return Response(AffiliateAuditSerializer(affiliate_audit).data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f"Error creating affiliate_audit: {str(e)}")
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
 
    @swagger_auto_schema(
        operation_summary="Update a affiliate_audit entry",
        operation_description="Updates a specific affiliate_audit entry by ID.",
        request_body=AffiliateAuditSerializer,
        responses={
            200: openapi.Response('Successful Response', AffiliateAuditSerializer),
            400: 'Bad Request',
            404: 'Not Found',
            500: 'Internal Server Error'
        },
        tags=['affiliate_audit']
    )
    def put(self, request, affiliate_audit_id=None):
        try: 
            serializer = AffiliateAuditSerializer(data=request.data)
            if serializer.is_valid():
                affiliate_audit = self.affiliate_audit_service.update_affiliate_audit(affiliate_audit_id, serializer.validated_data)
                return Response(AffiliateAuditSerializer(affiliate_audit).data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except AffiliateAudit.DoesNotExist as e:
            return Response({'error': str(e)}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.error(f"Error updating affiliate_audit: {str(e)}")
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @swagger_auto_schema(
        operation_summary="Delete a affiliate_audit entry",
        operation_description="Deletes a specific affiliate_audit entry by ID.",
        responses={
            204: 'No Content',
            404: 'Not Found',
            500: 'Internal Server Error'
        },
        tags=['affiliate_audit']
    )
    def delete(self, request, affiliate_audit_id=None):
        try:
            affiliate_audit = self.affiliate_audit_service.delete_affiliate_audit(affiliate_audit_id)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except AffiliateAudit.DoesNotExist as e:
            return Response({'error': str(e)}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.error(f"Error deleting affiliate_audit: {str(e)}")
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
