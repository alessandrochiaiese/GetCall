import logging
from django.http import JsonResponse
from django.contrib.auth.models import Group 
from accounts.api.serializers import GroupSerializer
from rest_framework import generics, permissions, serializers
from oauth2_provider.contrib.rest_framework import TokenHasReadWriteScope, TokenHasScope

# Set up a logger
logger = logging.getLogger(__name__)

class GroupList(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated, TokenHasScope]
    required_scopes = ['groups']
    queryset = Group.objects.all()
    serializer_class = GroupSerializer