# referral_system/services.py

import logging

from django.db.models.manager import BaseManager
from referral.models import ReferralProgramPartecipation
from django.contrib.auth import get_user_model

from referral.models.referral_code import ReferralCode
from referral.models.referral_program import ReferralProgram

User = get_user_model()

# Set up a logger
logger = logging.getLogger(__name__)


class ReferralProgramPartecipationPartecipationService():
    def __init__(self) -> None:
        pass
    
    def get_referral_program_partecipations(self) -> BaseManager[ReferralProgramPartecipation]:
        try:
            referral_program_partecipations = ReferralProgramPartecipation.objects.all() 
            return referral_program_partecipations
        except ReferralProgramPartecipation.DoesNotExist:
            logger.warning(f"ReferralProgramPartecipation not found")
            raise ValueError("ReferralProgramPartecipation not found")
     
    def get_referral_program_partecipation(self, pk) -> ReferralProgramPartecipation:
        try:
            referral_program_partecipation = ReferralProgramPartecipation.objects.get(id=pk)
            return referral_program_partecipation
        except ReferralProgramPartecipation.DoesNotExist:
            logger.warning(f"ReferralProgramPartecipation not found: {pk}")
            raise ValueError("ReferralProgramPartecipation not found")
     
    def create_referral_program_partecipation(self, data) -> ReferralProgramPartecipation:
        try:
            referral_program_partecipation = ReferralProgramPartecipation( 
                date_joined = data.get('date_joined'),
                reward_earned = data.get('reward_earned'),
                status = data.get('status'))
            referral_program_partecipation.save()
            programs = ReferralProgram.objects.filter(id__in=data['programs'])
            referral_program_partecipation.programs.set(programs)

            referral_codes = ReferralCode.objects.filter(id__in=data['referral_codes'])
            referral_program_partecipation.referral_codes.set(referral_codes)

            logger.info(f"ReferralProgramPartecipation created: {referral_program_partecipation}")
            return referral_program_partecipation
        except Exception as e:
            logger.error(f"Error creating referral_program_partecipation: {e}")
            raise e
 
    def update_referral_program_partecipation(self, pk, data) -> ReferralProgramPartecipation:
        try:
            referral_program_partecipation = self.get_referral_program_partecipation(pk)
            for key, value in data.items():
                setattr(referral_program_partecipation, key, value)
            referral_program_partecipation.save()
            logger.info(f"ReferralProgramPartecipation updated: {referral_program_partecipation}")
            return referral_program_partecipation
        except ReferralProgramPartecipation.DoesNotExist:
            logger.warning(f"ReferralProgramPartecipation not found: {pk}")
            raise ValueError("ReferralProgramPartecipation not found")
        except Exception as e:
            logger.error(f"Error updating referral_program_partecipation: {e}")
            raise e
    
    def delete_referral_program_partecipation(self, pk) -> None:
        try:
            referral_program_partecipation = self.get_referral_program_partecipation(pk)
            referral_program_partecipation.delete()
            logger.info(f"ReferralProgramPartecipation deleted: {referral_program_partecipation}")
        except ReferralProgramPartecipation.DoesNotExist:
            logger.warning(f"ReferralProgramPartecipation not found: {pk}")
            raise ValueError("ReferralProgramPartecipation not found")
        except Exception as e:
            logger.error(f"Error deleting referral_program_partecipation: {e}")
            raise e
        