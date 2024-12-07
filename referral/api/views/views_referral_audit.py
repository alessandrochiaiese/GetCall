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
from ..services.referral_audit_service import ReferralAuditService
from ...models.referral_audit import ReferralAudit
from ..serializers import ReferralAuditSerializer

# Set up a logger
logger = logging.getLogger(__name__)

class ReferralAuditAPIView(APIView):
    permission_classes = [AllowAny]  # [AllowAny]  or [IsAuthenticated]
    renderer_classes = [JSONRenderer]
    authentication_classes = [OAuth2Authentication]

    def __init__(self, *args, **kwargs):
        self.referral_audit_service = ReferralAuditService()

    @swagger_auto_schema(
        operation_summary="List all referral_audit",
        operation_description="Returns a list of all referral_audit entries.",
        responses={
            200: openapi.Response('Successful Response', ReferralAuditSerializer(many=True)),
            500: 'Internal Server Error'
        },
        tags=['referral_audit']
    )
    def get(self, request, referral_audit_id = None):
        try:
            if referral_audit_id == None:
                referral_audit = ReferralAudit.objects.all()
                serializer = ReferralAuditSerializer(referral_audit, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                referral_audit = self.referral_audit_service.get_referral_audit(referral_audit_id)
                serializer = ReferralAuditSerializer(referral_audit)
                return Response(serializer.data, status=status.HTTP_200_OK)  
        except ReferralAudit.DoesNotExist as e:
            return Response({'error': str(e)}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.error(f"Error fetching referral_audit: {str(e)}")
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @swagger_auto_schema(
        operation_summary="Create new referral_audit",
        operation_description="Creates a new referral_audit entry.",
        request_body=ReferralAuditSerializer,
        responses={
            201: openapi.Response('Created', ReferralAuditSerializer),
            400: 'Bad Request',
            500: 'Internal Server Error'
        },
        tags=['referral_audit']
    )
    def post(self, request):
        try:
            data = request.data
            data['ip_address'] = request.hostname
            serializer = ReferralAuditSerializer(data=data)
            if serializer.is_valid():
                referral_audit = self.referral_audit_service.create_referral_audit(serializer.validated_data)
                return Response(ReferralAuditSerializer(referral_audit).data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f"Error creating referral_audit: {str(e)}")
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
 
    @swagger_auto_schema(
        operation_summary="Update a referral_audit entry",
        operation_description="Updates a specific referral_audit entry by ID.",
        request_body=ReferralAuditSerializer,
        responses={
            200: openapi.Response('Successful Response', ReferralAuditSerializer),
            400: 'Bad Request',
            404: 'Not Found',
            500: 'Internal Server Error'
        },
        tags=['referral_audit']
    )
    def put(self, request, referral_audit_id=None):
        try: 
            serializer = ReferralAuditSerializer(data=request.data)
            if serializer.is_valid():
                referral_audit = self.referral_audit_service.update_referral_audit(referral_audit_id, serializer.validated_data)
                return Response(ReferralAuditSerializer(referral_audit).data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except ReferralAudit.DoesNotExist as e:
            return Response({'error': str(e)}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.error(f"Error updating referral_audit: {str(e)}")
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @swagger_auto_schema(
        operation_summary="Delete a referral_audit entry",
        operation_description="Deletes a specific referral_audit entry by ID.",
        responses={
            204: 'No Content',
            404: 'Not Found',
            500: 'Internal Server Error'
        },
        tags=['referral_audit']
    )
    def delete(self, request, referral_audit_id=None):
        try:
            referral_audit = self.referral_audit_service.delete_referral_audit(referral_audit_id)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except ReferralAudit.DoesNotExist as e:
            return Response({'error': str(e)}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.error(f"Error deleting referral_audit: {str(e)}")
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
