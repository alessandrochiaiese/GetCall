 
from django.contrib.auth.models import User, Group
from rest_framework import serializers
from accounts.models import Role, User as CustomUser

# first we define the serializers
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', "first_name", "last_name")

class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ("name", )

                          
class RoleSerializer(serializers.ModelSerializer):

    class Meta:
        model = Role
        fields = '__all__' 
        #fields = ('id', 'name')

class CustomUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = '__all__' 
        #fields = ('id', 'email', 'phone', 'first_name', 'last_name', 'password', 'roles', 'date_created', 'date_modified')