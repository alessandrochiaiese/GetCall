import datetime
import logging
from typing import List
from django.http import JsonResponse
from affiliate.models.affiliate import Affiliate
from affiliate.models.affiliate_reward import AffiliateReward
from affiliate.api.serializers import AffiliateRewardSerializer 

# Set up a logger
logger = logging.getLogger(__name__)

class AffiliateRewardService():
    def __init__(self) -> None:
        pass

    def get_affiliate_rewards(self) ->  List[AffiliateReward]:
        try:
            affiliate_rewards = AffiliateReward.objects.all() 
            return affiliate_rewards
        except AffiliateReward.DoesNotExist:
            logger.warning(f"AffiliateReward not found")
            raise ValueError("AffiliateReward not found")
     
    def get_affiliate_reward(self, pk) -> AffiliateReward:
        try:
            affiliate_reward = AffiliateReward.objects.get(id=pk)
            return affiliate_reward
        except AffiliateReward.DoesNotExist:
            logger.warning(f"AffiliateReward not found: {pk}")
            raise ValueError("AffiliateReward not found")
     
    def create_affiliate_reward(self, data) -> AffiliateReward:
        try:
            affiliate_reward = AffiliateReward( 
                affiliate = data.get('affiliate'),
                amount = data.get('amount'),
                created_at = data.get('created_at'))
            affiliate_reward.save() 
             
            logger.info(f"AffiliateReward created: {affiliate_reward}")
            return affiliate_reward
        except Exception as e:
            logger.error(f"Error creating affiliate_reward: {e}")
            raise e
 
    def update_affiliate_reward(self, pk, data) -> AffiliateReward:
        try:
            affiliate_reward = self.get_affiliate_reward(pk)
            for key, value in data.items():
                setattr(affiliate_reward, key, value)
            affiliate_reward.save()
            logger.info(f"AffiliateReward updated: {affiliate_reward}")
            return affiliate_reward
        except Exception as e:
            logger.error(f"Error updating affiliate_reward: {e}")
            raise e
    
    def delete_affiliate_reward(self, pk) -> None:
        try:
            affiliate_reward = self.get_affiliate_reward(pk)
            affiliate_reward.delete()
            logger.info(f"AffiliateReward deleted: {affiliate_reward}")
        except Exception as e:
            logger.error(f"Error deleting affiliate_reward: {e}")
            raise e