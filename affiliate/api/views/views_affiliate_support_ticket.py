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
from affiliate.api.services.affiliate_support_ticket_service import AffiliateSupportTicketService
from affiliate.models.affiliate_support_ticket import AffiliateSupportTicket
from affiliate.api.serializers import AffiliateSupportTicketSerializer

# Set up a logger
logger = logging.getLogger(__name__)

class AffiliateSupportTicketAPIView(APIView):
    permission_classes = [IsAuthenticated]  # [AllowAny]  or [IsAuthenticated]
    renderer_classes = [JSONRenderer]
    authentication_classes = [OAuth2Authentication]

    def __init__(self, *args, **kwargs):
        self.affiliate_support_ticket_service = AffiliateSupportTicketService()

    @swagger_auto_schema(
        operation_summary="List all affiliate_support_ticket",
        operation_description="Returns a list of all affiliate_support_ticket entries.",
        responses={
            200: openapi.Response('Successful Response', AffiliateSupportTicketSerializer(many=True)),
            500: 'Internal Server Error'
        },
        tags=['affiliate_support_ticket']
    )
    def get(self, request, affiliate_support_ticket_id = None):
        try:
            if affiliate_support_ticket_id == None:
                affiliate_support_ticket = AffiliateSupportTicket.objects.all()
                serializer = AffiliateSupportTicketSerializer(affiliate_support_ticket, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                affiliate_support_ticket = self.affiliate_support_ticket_service.get_affiliate_support_ticket(affiliate_support_ticket_id)
                serializer = AffiliateSupportTicketSerializer(affiliate_support_ticket)
                return Response(serializer.data, status=status.HTTP_200_OK)  
        except AffiliateSupportTicket.DoesNotExist as e:
            return Response({'error': str(e)}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.error(f"Error fetching affiliate_support_ticket: {str(e)}")
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @swagger_auto_schema(
        operation_summary="Create new affiliate_support_ticket",
        operation_description="Creates a new affiliate_support_ticket entry.",
        request_body=AffiliateSupportTicketSerializer,
        responses={
            201: openapi.Response('Created', AffiliateSupportTicketSerializer),
            400: 'Bad Request',
            500: 'Internal Server Error'
        },
        tags=['affiliate_support_ticket']
    )
    def post(self, request):
        try:
            serializer = AffiliateSupportTicketSerializer(data=request.data)
            if serializer.is_valid():
                affiliate_support_ticket = self.affiliate_support_ticket_service.create_affiliate_support_ticket(serializer.validated_data)
                return Response(AffiliateSupportTicketSerializer(affiliate_support_ticket).data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f"Error creating affiliate_support_ticket: {str(e)}")
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
 
    @swagger_auto_schema(
        operation_summary="Update a affiliate_support_ticket entry",
        operation_description="Updates a specific affiliate_support_ticket entry by ID.",
        request_body=AffiliateSupportTicketSerializer,
        responses={
            200: openapi.Response('Successful Response', AffiliateSupportTicketSerializer),
            400: 'Bad Request',
            404: 'Not Found',
            500: 'Internal Server Error'
        },
        tags=['affiliate_support_ticket']
    )
    def put(self, request, affiliate_support_ticket_id=None):
        try: 
            serializer = AffiliateSupportTicketSerializer(data=request.data)
            if serializer.is_valid():
                affiliate_support_ticket = self.affiliate_support_ticket_service.update_affiliate_support_ticket(affiliate_support_ticket_id, serializer.validated_data)
                return Response(AffiliateSupportTicketSerializer(affiliate_support_ticket).data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except AffiliateSupportTicket.DoesNotExist as e:
            return Response({'error': str(e)}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.error(f"Error updating affiliate_support_ticket: {str(e)}")
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @swagger_auto_schema(
        operation_summary="Delete a affiliate_support_ticket entry",
        operation_description="Deletes a specific affiliate_support_ticket entry by ID.",
        responses={
            204: 'No Content',
            404: 'Not Found',
            500: 'Internal Server Error'
        },
        tags=['affiliate_support_ticket']
    )
    def delete(self, request, affiliate_support_ticket_id=None):
        try:
            affiliate_support_ticket = self.affiliate_support_ticket_service.delete_affiliate_support_ticket(affiliate_support_ticket_id)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except AffiliateSupportTicket.DoesNotExist as e:
            return Response({'error': str(e)}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.error(f"Error deleting affiliate_support_ticket: {str(e)}")
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
