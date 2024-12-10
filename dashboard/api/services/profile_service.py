import datetime
import logging
from typing import List
from django.http import JsonResponse
from accounts.models.user import User
from dashboard.models.profile import Profile
from dashboard.api.serializers import ProfileSerializer 

# Set up a logger
logger = logging.getLogger(__name__)

class ProfileService():
    def __init__(self) -> None:
        pass

    def get_profiles(self) ->  List[Profile]:
        try:
            profiles = Profile.objects.all() 
            return profiles
        except Profile.DoesNotExist:
            logger.warning(f"Profile not found")
            raise ValueError("Profile not found")
     
    def get_profile(self, pk) -> Profile:
        try:
            profile = Profile.objects.get(id=pk)
            return profile
        except Profile.DoesNotExist:
            logger.warning(f"Profile not found: {pk}")
            raise ValueError("Profile not found")
     
    def create_profile(self, data) -> Profile:
        try:
            user = User.objects.get(username=data.get('username'))
            profile = Profile.objects.create(
                user=user,
                bio=data.get('bio'),
                avatar=data.get('avatar')
            )
            profile.save()
 
            logger.info(f"Profile created: {profile}")
            return profile
        except Exception as e:
            logger.error(f"Error creating profile: {e}")
            raise e
 
    def update_profile(self, profile_id, data) -> Profile:
        try:
            # Recupera il profilo esistente
            profile = Profile.objects.get(id=profile_id)

            # Aggiorna i campi
            for field, value in data.items():
                setattr(profile, field, value)

            # Salva il profilo aggiornato
            profile.save()
            return profile

        except Profile.DoesNotExist:
            # Gestisci l'errore se il profilo non esiste
            raise Profile.DoesNotExist(f"Profile with id {profile_id} does not exist.")

        except Exception as e:
            # Logga e rilancia qualsiasi altro errore
            logger.error(f"Error updating profile: {e}")
            raise e
    
    def delete_profile(self, pk) -> None:
        try:
            profile = self.get_profile(pk)
            profile.delete()
            logger.info(f"Profile deleted: {profile}")
        except Exception as e:
            logger.error(f"Error deleting profile: {e}")
            raise e