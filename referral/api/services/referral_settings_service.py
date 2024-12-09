# referral_system/services.py

import logging

from typing import List 
from django.contrib.auth import get_user_model

from referral.models.referral_settings import ReferralSettings

User = get_user_model()


# Set up a logger
logger = logging.getLogger(__name__)


class ReferralSettingsService():
    def __init__(self) -> None:
        pass
    
    def get_referral_settings(self) -> List[ReferralSettings]:
        try:
            referral_settings = ReferralSettings.objects.all() 
            return referral_settings
        except ReferralSettings.DoesNotExist:
            logger.warning(f"ReferralSettings not found")
            raise ValueError("ReferralSettings not found")
     
    def get_referral_setting(self, pk) -> ReferralSettings:
        try:
            referral_setting = ReferralSettings.objects.get(id=pk)
            return referral_setting
        except ReferralSettings.DoesNotExist:
            logger.warning(f"ReferralSettings not found: {pk}")
            raise ValueError("ReferralSettings not found")
     
    def create_referral_setting(self, data) -> ReferralSettings:
        try:
            referral_setting = ReferralSettings(
                user = data.get('user'),
                default_reward_type = data.get('default_reward_type'),
                max_referrals_allowed = data.get('max_referrals_allowed'),
                notification_preference = data.get('notification_preference'),
                auto_share_setting = data.get('auto_share_setting'),
                social_share_message = data.get('social_share_message')
            )
            referral_setting.save()
            
            logger.info(f"ReferralSettings created: {referral_setting}")
            return referral_setting
        except Exception as e:
            logger.error(f"Error creating referral_setting: {e}")
            raise e
 
    def update_referral_setting(self, pk, data) -> ReferralSettings:
        try:
            referral_setting = self.get_referral_setting(pk)
            for key, value in data.items():
                setattr(referral_setting, key, value)
            referral_setting.save()
            logger.info(f"ReferralSettings updated: {referral_setting}")
            return referral_setting
        except ReferralSettings.DoesNotExist:
            logger.warning(f"ReferralSettings not found: {pk}")
            raise ValueError("ReferralSettings not found")
        except Exception as e:
            logger.error(f"Error updating referral_setting: {e}")
            raise e
    
    def delete_referral_setting(self, pk) -> None:
        try:
            referral_setting = self.get_referral_setting(pk)
            referral_setting.delete()
            logger.info(f"ReferralSettings deleted: {referral_setting}")
        except ReferralSettings.DoesNotExist:
            logger.warning(f"ReferralSettings not found: {pk}")
            raise ValueError("ReferralSettings not found")
        except Exception as e:
            logger.error(f"Error deleting referral_setting: {e}")
            raise e
        