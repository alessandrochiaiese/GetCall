# referral_system/services.py
 
from datetime import datetime
import logging

from django.db.models.manager import BaseManager
from accounts.models.region import Region
from referral.abstracts.test import ReferralCode
from referral.models import ReferralProgram
from django.contrib.auth import get_user_model

from referral.models.referral_stats import ReferralStats
from referral.models.referral_user import ReferralUser

User = get_user_model()

# Set up a logger
logger = logging.getLogger(__name__)


class ReferralProgramService():
    def __init__(self) -> None:
        pass
    
    def get_referral_programs(self) -> BaseManager[ReferralProgram]:
        try:
            referral_programs = ReferralProgram.objects.all() 
            return referral_programs
        except ReferralProgram.DoesNotExist:
            logger.warning(f"ReferralProgram not found")
            raise ValueError("ReferralProgram not found")
     
    def get_referral_program(self, pk) -> ReferralProgram:
        try:
            referral_program = ReferralProgram.objects.get(id=pk)
            return referral_program
        except ReferralProgram.DoesNotExist:
            logger.warning(f"ReferralProgram not found: {pk}")
            raise ValueError("ReferralProgram not found")
     
    def create_referral_program(self, data, user) -> ReferralProgram:
        try:
            referral_program = ReferralProgram( 
                name = data.get('name'),
                description = data.get('description'),
                reward_type = data.get('reward_type'),
                reward_value = data.get('reward_value'),
                currency = data.get('currency'),
                min_referral_count = data.get('min_referral_count'),
                max_referrals_per_user = data.get('max_referrals_per_user'),
                date_created = datetime.now(),#data.get('date_created'),
                is_active = True, #data.get('is_active'),
                program_duration = data.get('program_duration'), 
                target_industry = data.get('target_industry'))
            referral_program.save()
                
            # Creazione ReferralCode per l'utente creatore
            referral_code = ReferralCode.objects.create(
                user=user,
                program=referral_program,
                code=f"{user.username}-{referral_program.name}",
                usage_count=0,
                date_created=datetime.now(),
                status="active",
                referred_user_count=0
            )

            # Creazione Stats iniziali
            ReferralStats.objects.create(
                referral_code=referral_code,
                period="daily",  # Esempio: può essere settimanale o mensile
                click_count=0,
                conversion_count=0,
                total_rewards=0
            )

            # Creazione o aggiornamento ReferralUser
            referral_user, created = ReferralUser.objects.get_or_create(user=user)
            referral_user.total_referrals += 1
            referral_user.save()

            logger.info(f"ReferralProgram created: {referral_program}")
            return referral_program
        except Exception as e:
            logger.error(f"Error creating referral_program: {e}")
            raise e
 
    def update_referral_program(self, pk, data) -> ReferralProgram:
        try:
            referral_program = self.get_referral_program(pk)
            for key, value in data.items():
                setattr(referral_program, key, value)
            referral_program.save()
            logger.info(f"ReferralProgram updated: {referral_program}")
            return referral_program
        except ReferralProgram.DoesNotExist:
            logger.warning(f"ReferralProgram not found: {pk}")
            raise ValueError("ReferralProgram not found")
        except Exception as e:
            logger.error(f"Error updating referral_program: {e}")
            raise e
    
    def delete_referral_program(self, pk) -> None:
        try:
            referral_program = self.get_referral_program(pk)
            referral_program.delete()
            logger.info(f"ReferralProgram deleted: {referral_program}")
        except ReferralProgram.DoesNotExist:
            logger.warning(f"ReferralProgram not found: {pk}")
            raise ValueError("ReferralProgram not found")
        except Exception as e:
            logger.error(f"Error deleting referral_program: {e}")
            raise e
        