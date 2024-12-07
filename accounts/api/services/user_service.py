import datetime
import logging
from typing import List
from django.http import JsonResponse
from accounts.models.user import User
from accounts.api.serializers import UserSerializer 

# Set up a logger
logger = logging.getLogger(__name__)

class UserService():
    def __init__(self) -> None:
        pass

    def get_users(self) ->  List[User]:
        try:
            users = User.objects.all() 
            return users
        except User.DoesNotExist:
            logger.warning(f"User not found")
            raise ValueError("User not found")
     
    def get_user(self, pk) -> User:
        try:
            user = User.objects.get(id=pk)
            return user
        except User.DoesNotExist:
            logger.warning(f"User not found: {pk}")
            raise ValueError("User not found")
     
    def create_user(self, data) -> User:
        try:
            user = User(
                email=data.email,
                phone=data.phone,
                first_name=data.first_name,
                last_name=data.last_name,
                password=data.password)
            user.save()

            roles = User.objects.filter(id__in=data['roles'])
            user.roles.set(roles)
            
            logger.info(f"User created: {user}")
            return user
        except Exception as e:
            logger.error(f"Error creating user: {e}")
            raise e
 
    def update_user(self, pk, data) -> User:
        try:
            user = self.get_user(pk)
            for key, value in data.items():
                setattr(user, key, value)
            user.save()
            logger.info(f"User updated: {user}")
            return user
        except Exception as e:
            logger.error(f"Error updating user: {e}")
            raise e
    
    def delete_user(self, pk) -> None:
        try:
            user = self.get_user(pk)
            user.delete()
            logger.info(f"User deleted: {user}")
        except Exception as e:
            logger.error(f"Error deleting user: {e}")
            raise e