# referral_system/services.py

import logging

from django.db.models.manager import BaseManager 
from django.contrib.auth import get_user_model

from referral.models.referral_code import ReferralCode
from referral.models.referral_stats import ReferralStats

User = get_user_model()


# Set up a logger
logger = logging.getLogger(__name__)


class ReferralStatsService():
    def __init__(self) -> None:
        pass
    
    def get_referral_stats(self) -> BaseManager[ReferralStats]:
        try:
            referral_stats = ReferralStats.objects.all() 
            return referral_stats
        except ReferralStats.DoesNotExist:
            logger.warning(f"ReferralStats not found")
            raise ValueError("ReferralStats not found")
     
    def get_referral_stat(self, pk) -> ReferralStats:
        try:
            referral_stat = ReferralStats.objects.get(id=pk)
            return referral_stat
        except ReferralStats.DoesNotExist:
            logger.warning(f"ReferralStats not found: {pk}")
            raise ValueError("ReferralStats not found")
     
    def create_referral_stat(self, data) -> ReferralStats:
        try:
            referral_stat = ReferralStats(
                user = data.get('user'),
                period = data.get('period'),
                click_count = data.get('click_count'),
                conversion_count = data.get('conversion_count'),
                total_rewards = data.get('total_rewards'),
                average_conversion_value = data.get('average_conversion_value'),
                highest_referral_earning = data.get('highest_referral_earning')
            )
            referral_stat.save()
            referral_codes = ReferralCode.objects.filter(id__in=data['referral_codes'])
            referral_stat.referral_codes.set(referral_codes)

            logger.info(f"ReferralStats created: {referral_stat}")
            return referral_stat
        except Exception as e:
            logger.error(f"Error creating referral_stat: {e}")
            raise e
 
    def update_referral_stat(self, pk, data) -> ReferralStats:
        try:
            referral_stat = self.get_referral_stat(pk)
            for key, value in data.items():
                setattr(referral_stat, key, value)
            referral_stat.save()
            logger.info(f"ReferralStats updated: {referral_stat}")
            return referral_stat
        except ReferralStats.DoesNotExist:
            logger.warning(f"ReferralStats not found: {pk}")
            raise ValueError("ReferralStats not found")
        except Exception as e:
            logger.error(f"Error updating referral_stat: {e}")
            raise e
    
    def delete_referral_stat(self, pk) -> None:
        try:
            referral_stat = self.get_referral_stat(pk)
            referral_stat.delete()
            logger.info(f"ReferralStats deleted: {referral_stat}")
        except ReferralStats.DoesNotExist:
            logger.warning(f"ReferralStats not found: {pk}")
            raise ValueError("ReferralStats not found")
        except Exception as e:
            logger.error(f"Error deleting referral_stat: {e}")
            raise e
        