# referral_system/services.py

import logging

from django.db.models.manager import BaseManager
from referral.models import ReferralReward
from django.contrib.auth import get_user_model

User = get_user_model()

# Set up a logger
logger = logging.getLogger(__name__)


class ReferralRewardService():
    def __init__(self) -> None:
        pass
    
    def get_referral_rewards(self) -> BaseManager[ReferralReward]:
        try:
            referral_rewards = ReferralReward.objects.all() 
            return referral_rewards
        except ReferralReward.DoesNotExist:
            logger.warning(f"ReferralReward not found")
            raise ValueError("ReferralReward not found")
     
    def get_referral_reward(self, pk) -> ReferralReward:
        try:
            referral_reward = ReferralReward.objects.get(id=pk)
            return referral_reward
        except ReferralReward.DoesNotExist:
            logger.warning(f"ReferralReward not found: {pk}")
            raise ValueError("ReferralReward not found")
     
    def create_referral_reward(self, data) -> ReferralReward:
        try:
            referral_reward = ReferralReward(
                user = data.get('user'),
                reward_type = data.get('reward_type'),
                reward_value = data.get('reward_value'),
                date_awarded = data.get('date_awarded'),
                status = data.get('status'),
                expiry_date = data.get('expiry_date'),
                reward_description = data.get('reward_description'),
                reward_source = data.get('reward_source'))
            referral_reward.save()
            logger.info(f"ReferralReward created: {referral_reward}")
            return referral_reward
        except Exception as e:
            logger.error(f"Error creating referral_reward: {e}")
            raise e
 
    def update_referral_reward(self, pk, data) -> ReferralReward:
        try:
            referral_reward = self.get_referral_reward(pk)
            for key, value in data.items():
                setattr(referral_reward, key, value)
            referral_reward.save()
            logger.info(f"ReferralReward updated: {referral_reward}")
            return referral_reward
        except ReferralReward.DoesNotExist:
            logger.warning(f"ReferralReward not found: {pk}")
            raise ValueError("ReferralReward not found")
        except Exception as e:
            logger.error(f"Error updating referral_reward: {e}")
            raise e
    
    def delete_referral_reward(self, pk) -> None:
        try:
            referral_reward = self.get_referral_reward(pk)
            referral_reward.delete()
            logger.info(f"ReferralReward deleted: {referral_reward}")
        except ReferralReward.DoesNotExist:
            logger.warning(f"ReferralReward not found: {pk}")
            raise ValueError("ReferralReward not found")
        except Exception as e:
            logger.error(f"Error deleting referral_reward: {e}")
            raise e
        