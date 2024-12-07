from django.http import Http404
from rest_framework.exceptions import NotFound
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework import status
from oauth2_provider.contrib.rest_framework import OAuth2Authentication
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from affiliate.api.services.affiliate_program_partecipation_service import AffiliateProgramPartecipationService
from affiliate.models.affiliate_program_partecipation import AffiliateProgramPartecipation
from affiliate.api.serializers import AffiliateProgramPartecipationSerializer

# Set up a logger
import logging
logger = logging.getLogger(__name__)

class AffiliateProgramPartecipationAPIView(APIView):
    permission_classes = [AllowAny]  # You can change this to [IsAuthenticated] if needed
    renderer_classes = [JSONRenderer]
    authentication_classes = [OAuth2Authentication]

    def __init__(self, *args, **kwargs):
        self.affiliate_program_partecipation_service = AffiliateProgramPartecipationService()

    @swagger_auto_schema(
        operation_summary="List all affiliate program participations",
        operation_description="Returns a list of all affiliate program participations.",
        responses={200: openapi.Response('Successful Response', AffiliateProgramPartecipationSerializer(many=True))},
        tags=['affiliate_program_partecipation']
    )
    def get(self, request, affiliate_program_partecipation_id=None):
        try:
            if affiliate_program_partecipation_id is None:
                # Fetch all participations
                affiliate_program_partecipations = AffiliateProgramPartecipation.objects.all()
                serializer = AffiliateProgramPartecipationSerializer(affiliate_program_partecipations, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                # Fetch single participation by ID
                affiliate_program_partecipation = self.affiliate_program_partecipation_service.get_affiliate_program_partecipation(affiliate_program_partecipation_id)
                serializer = AffiliateProgramPartecipationSerializer(affiliate_program_partecipation)
                return Response(serializer.data, status=status.HTTP_200_OK)
        except AffiliateProgramPartecipation.DoesNotExist:
            raise Http404("AffiliateProgramParticipation not found")
        except Exception as e:
            logger.error(f"Error fetching affiliate_program_partecipation: {str(e)}")
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @swagger_auto_schema(
        operation_summary="Create new affiliate program participation",
        operation_description="Creates a new affiliate program participation entry.",
        request_body=AffiliateProgramPartecipationSerializer,
        responses={201: openapi.Response('Created', AffiliateProgramPartecipationSerializer)},
        tags=['affiliate_program_partecipation']
    )
    def post(self, request):
        try:
            serializer = AffiliateProgramPartecipationSerializer(data=request.data)
            if serializer.is_valid():
                # Create new participation
                affiliate_program_partecipation = self.affiliate_program_partecipation_service.create_affiliate_program_partecipation(serializer.validated_data)
                return Response(AffiliateProgramPartecipationSerializer(affiliate_program_partecipation).data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f"Error creating affiliate_program_partecipation: {str(e)}")
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @swagger_auto_schema(
        operation_summary="Update a specific affiliate program participation",
        operation_description="Updates a specific affiliate program participation entry by ID.",
        request_body=AffiliateProgramPartecipationSerializer,
        responses={200: openapi.Response('Successful Response', AffiliateProgramPartecipationSerializer)},
        tags=['affiliate_program_partecipation']
    )
    def put(self, request, affiliate_program_partecipation_id=None):
        try:
            # Update existing participation
            serializer = AffiliateProgramPartecipationSerializer(data=request.data)
            if serializer.is_valid():
                affiliate_program_partecipation = self.affiliate_program_partecipation_service.update_affiliate_program_partecipation(affiliate_program_partecipation_id, serializer.validated_data)
                return Response(AffiliateProgramPartecipationSerializer(affiliate_program_partecipation).data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except AffiliateProgramPartecipation.DoesNotExist:
            raise Http404("AffiliateProgramParticipation not found")
        except Exception as e:
            logger.error(f"Error updating affiliate_program_partecipation: {str(e)}")
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @swagger_auto_schema(
        operation_summary="Delete a specific affiliate program participation",
        operation_description="Deletes a specific affiliate program participation entry by ID.",
        responses={204: 'No Content', 404: 'Not Found'},
        tags=['affiliate_program_partecipation']
    )
    def delete(self, request, affiliate_program_partecipation_id=None):
        try:
            # Delete participation
            self.affiliate_program_partecipation_service.delete_affiliate_program_partecipation(affiliate_program_partecipation_id)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except AffiliateProgramPartecipation.DoesNotExist:
            raise Http404("AffiliateProgramParticipation not found")
        except Exception as e:
            logger.error(f"Error deleting affiliate_program_partecipation: {str(e)}")
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
