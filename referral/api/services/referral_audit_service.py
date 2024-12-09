# referral_system/services.py

import logging

from typing import List 
from django.contrib.auth import get_user_model

from referral.models.referral_audit import ReferralAudit
from referral.models.referral_code import ReferralCode

User = get_user_model()

# Set up a logger
logger = logging.getLogger(__name__)


class ReferralAuditService():
    def __init__(self) -> None:
        pass
    
    def get_referral_audits(self) -> List[ReferralAudit]:
        try:
            referral_audits = ReferralAudit.objects.all() 
            return referral_audits
        except ReferralAudit.DoesNotExist:
            logger.warning(f"ReferralAudit not found")
            raise ValueError("ReferralAudit not found")
     
    def get_referral_audit(self, pk) -> ReferralAudit:
        try:
            referral_audit = ReferralAudit.objects.get(id=pk)
            return referral_audit
        except ReferralAudit.DoesNotExist:
            logger.warning(f"ReferralAudit not found: {pk}")
            raise ValueError("ReferralAudit not found")
     
    def create_referral_audit(self, data) -> ReferralAudit:
        try:
            referral_audit = ReferralAudit( 
                action_taken = data.get('action_taken'),
                action_date = data.get('action_date'),
                user = data.get('user'),
                ip_address = data.get('ip_address'),
                device_info = data.get('device_info'),
                location = data.get('location ')
            )
            referral_audit.save()
            
            referral_codes = ReferralCode.objects.filter(id__in=data['referral_codes'])
            referral_audit.referral_codes.set(referral_codes)

            logger.info(f"ReferralAudit created: {referral_audit}")
            return referral_audit
        except Exception as e:
            logger.error(f"Error creating referral_audit: {e}")
            raise e
 
    def update_referral_audit(self, pk, data) -> ReferralAudit:
        try:
            referral_audit = self.get_referral_audit(pk)
            for key, value in data.items():
                setattr(referral_audit, key, value)
            referral_audit.save()
            logger.info(f"ReferralAudit updated: {referral_audit}")
            return referral_audit
        except ReferralAudit.DoesNotExist:
            logger.warning(f"ReferralAudit not found: {pk}")
            raise ValueError("ReferralAudit not found")
        except Exception as e:
            logger.error(f"Error updating referral_audit: {e}")
            raise e
    
    def delete_referral_audit(self, pk) -> None:
        try:
            referral_audit = self.get_referral_audit(pk)
            referral_audit.delete()
            logger.info(f"ReferralAudit deleted: {referral_audit}")
        except ReferralAudit.DoesNotExist:
            logger.warning(f"ReferralAudit not found: {pk}")
            raise ValueError("ReferralAudit not found")
        except Exception as e:
            logger.error(f"Error deleting referral_audit: {e}")
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