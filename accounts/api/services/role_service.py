import datetime
import logging
from typing import List
from django.http import JsonResponse
from accounts.models import *
from accounts.api.serializers import RoleSerializer 

# Set up a logger
logger = logging.getLogger(__name__)

class RoleService():
    def __init__(self) -> None:
        pass
    
    def get_roles(self) ->  List[Role]:
        try:
            roles = Role.objects.all() 
            return roles
        except Role.DoesNotExist:
            logger.warning(f"Role not found")
            raise ValueError("Role not found")
     
    def get_role(self, pk) -> Role:
        try:
            role = Role.objects.get(id=pk)
            return role
        except Role.DoesNotExist:
            logger.warning(f"Role not found: {pk}")
            raise ValueError("Role not found")
     
    def create_role(self, data) -> Role:
        try:
            role = Role(**data)
            role.save()
            logger.info(f"Role created: {role}")
            return role
        except Exception as e:
            logger.error(f"Error creating role: {e}")
            raise e
 
    def update_role(self, pk, data) -> Role:
        try:
            role = self.get_role(pk)
            for key, value in data.items():
                setattr(role, key, value)
            role.save()
            logger.info(f"Role updated: {role}")
            return role
        except Role.DoesNotExist:
            logger.warning(f"Role not found: {pk}")
            raise ValueError("Role not found")
        except Exception as e:
            logger.error(f"Error updating role: {e}")
            raise e
    
    def delete_role(self, pk) -> None:
        try:
            role = self.get_role(pk)
            role.delete()
            logger.info(f"Role deleted: {role}")
        except Role.DoesNotExist:
            logger.warning(f"Role not found: {pk}")
            raise ValueError("Role not found")
        except Exception as e:
            logger.error(f"Error deleting role: {e}")
            raise e
        