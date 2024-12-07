# referral_system/services.py

import logging

from django.db.models.manager import BaseManager 
from django.contrib.auth import get_user_model

from referral.models.referral_bonus import ReferralBonus
from referral.models.referral_program import ReferralProgram

User = get_user_model()

# Set up a logger
logger = logging.getLogger(__name__)


class ReferralBonusService():
    def __init__(self) -> None:
        pass
    
    def get_referral_bonus(self) -> BaseManager[ReferralBonus]:
        try:
            referral_bonus = ReferralBonus.objects.all() 
            return referral_bonus
        except ReferralBonus.DoesNotExist:
            logger.warning(f"ReferralBonus not found")
            raise ValueError("ReferralBonus not found")
     
    def get_referral_bonus(self, pk) -> ReferralBonus:
        try:
            referral_bonus = ReferralBonus.objects.get(id=pk)
            return referral_bonus
        except ReferralBonus.DoesNotExist:
            logger.warning(f"ReferralBonus not found: {pk}")
            raise ValueError("ReferralBonus not found")
     
    def create_referral_bonus(self, data) -> ReferralBonus:
        try:
            referral_bonus = ReferralBonus(
                bonus_type = data.get('bonus_type'),
                bonus_value = data.get('bonus_value'), 
                min_referrals_required = data.get('min_referrals_required'),
                bonus_date = data.get('bonus_date'),
                expiry_date = data.get('expiry_date'),
                max_usage = data.get('max_usage'),
                eligibility_criteria = data.get('eligibility_criteria')
            )
            referral_bonus.save()

            referral_programs = ReferralProgram.objects.filter(id__in=data['referral_programs'])
            referral_bonus.programs.set(referral_programs)

            logger.info(f"ReferralBonus created: {referral_bonus}")
            return referral_bonus
        except Exception as e:
            logger.error(f"Error creating referral_bonus: {e}")
            raise e
 
    def update_referral_bonus(self, pk, data) -> ReferralBonus:
        try:
            referral_bonus = self.get_referral_bonus(pk)
            for key, value in data.items():
                setattr(referral_bonus, key, value)
            referral_bonus.save()
            logger.info(f"ReferralBonus updated: {referral_bonus}")
            return referral_bonus
        except ReferralBonus.DoesNotExist:
            logger.warning(f"ReferralBonus not found: {pk}")
            raise ValueError("ReferralBonus not found")
        except Exception as e:
            logger.error(f"Error updating referral_bonus: {e}")
            raise e
    
    def delete_referral_bonus(self, pk) -> None:
        try:
            referral_bonus = self.get_referral_bonus(pk)
            referral_bonus.delete()
            logger.info(f"ReferralBonus deleted: {referral_bonus}")
        except ReferralBonus.DoesNotExist:
            logger.warning(f"ReferralBonus not found: {pk}")
            raise ValueError("ReferralBonus not found")
        except Exception as e:
            logger.error(f"Error deleting referral_bonus: {e}")
            raise e
        
"""class ReferralService:
    @staticmethod
    def create_referral_program(name, reward_amount, active=True):
        program = ReferralProgram.objects.create(name=name, reward_amount=reward_amount, active=active)
        return program

    @staticmethod
    def create_referral(program_id, referrer_id, referred_id):
        program = ReferralProgram.objects.get(id=program_id)
        referrer = User.objects.get(id=referrer_id)
        referred = User.objects.get(id=referred_id)
        referral = Referral.objects.create(program=program, referrer=referrer, referred=referred)
        return referral

    @staticmethod
    def reward_referral(referral_id, amount):
        referral = Referral.objects.get(id=referral_id)
        reward = ReferralReward.objects.create(referral=referral, amount=amount)
        referral.reward_given = True
        referral.save()
        return reward
"""