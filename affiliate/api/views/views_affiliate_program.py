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
from affiliate.api.services.affiliate_program_service import AffiliateProgramService
from affiliate.models.affiliate_program import AffiliateProgram
from affiliate.api.serializers import AffiliateProgramSerializer

# Set up a logger
logger = logging.getLogger(__name__)

class AffiliateProgramAPIView(APIView):
    permission_classes = [IsAuthenticated]  # [AllowAny]  or [IsAuthenticated]
    renderer_classes = [JSONRenderer]
    authentication_classes = [OAuth2Authentication]

    def __init__(self, *args, **kwargs):
        self.affiliate_program_service = AffiliateProgramService()

    @swagger_auto_schema(
        operation_summary="List all affiliate_program",
        operation_description="Returns a list of all affiliate_program entries.",
        responses={
            200: openapi.Response('Successful Response', AffiliateProgramSerializer(many=True)),
            500: 'Internal Server Error'
        },
        tags=['affiliate_program']
    )
    def get(self, request, affiliate_program_id = None):
        try:
            if affiliate_program_id == None:
                affiliate_program = AffiliateProgram.objects.all()
                serializer = AffiliateProgramSerializer(affiliate_program, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                affiliate_program = self.affiliate_program_service.get_affiliate_program(affiliate_program_id)
                serializer = AffiliateProgramSerializer(affiliate_program)
                return Response(serializer.data, status=status.HTTP_200_OK)  
        except AffiliateProgram.DoesNotExist as e:
            return Response({'error': str(e)}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.error(f"Error fetching affiliate_program: {str(e)}")
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @swagger_auto_schema(
        operation_summary="Create new affiliate_program",
        operation_description="Creates a new affiliate_program entry.",
        request_body=AffiliateProgramSerializer,
        responses={
            201: openapi.Response('Created', AffiliateProgramSerializer),
            400: 'Bad Request',
            500: 'Internal Server Error'
        },
        tags=['affiliate_program']
    )
    def post(self, request):
        try:
            serializer = AffiliateProgramSerializer(data=request.data)
            if serializer.is_valid():
                affiliate_program = self.affiliate_program_service.create_affiliate_program(serializer.validated_data)
                return Response(AffiliateProgramSerializer(affiliate_program).data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f"Error creating affiliate_program: {str(e)}")
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
 
    @swagger_auto_schema(
        operation_summary="Update a affiliate_program entry",
        operation_description="Updates a specific affiliate_program entry by ID.",
        request_body=AffiliateProgramSerializer,
        responses={
            200: openapi.Response('Successful Response', AffiliateProgramSerializer),
            400: 'Bad Request',
            404: 'Not Found',
            500: 'Internal Server Error'
        },
        tags=['affiliate_program']
    )
    def put(self, request, affiliate_program_id=None):
        try: 
            serializer = AffiliateProgramSerializer(data=request.data)
            if serializer.is_valid():
                affiliate_program = self.affiliate_program_service.update_affiliate_program(affiliate_program_id, serializer.validated_data)
                return Response(AffiliateProgramSerializer(affiliate_program).data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except AffiliateProgram.DoesNotExist as e:
            return Response({'error': str(e)}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.error(f"Error updating affiliate_program: {str(e)}")
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @swagger_auto_schema(
        operation_summary="Delete a affiliate_program entry",
        operation_description="Deletes a specific affiliate_program entry by ID.",
        responses={
            204: 'No Content',
            404: 'Not Found',
            500: 'Internal Server Error'
        },
        tags=['affiliate_program']
    )
    def delete(self, request, affiliate_program_id=None):
        try:
            affiliate_program = self.affiliate_program_service.delete_affiliate_program(affiliate_program_id)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except AffiliateProgram.DoesNotExist as e:
            return Response({'error': str(e)}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.error(f"Error deleting affiliate_program: {str(e)}")
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
