import datetime
import logging
from typing import List
from django.http import JsonResponse
from affiliate.models.affiliate import Affiliate
from affiliate.models.affiliate_tier import AffiliateTier
from affiliate.api.serializers import AffiliateTierSerializer 

# Set up a logger
logger = logging.getLogger(__name__)

class AffiliateTierService():
    def __init__(self) -> None:
        pass

    def get_affiliate_tiers(self) ->  List[AffiliateTier]:
        try:
            affiliate_tiers = AffiliateTier.objects.all() 
            return affiliate_tiers
        except AffiliateTier.DoesNotExist:
            logger.warning(f"AffiliateTier not found")
            raise ValueError("AffiliateTier not found")
     
    def get_affiliate_tier(self, pk) -> AffiliateTier:
        try:
            affiliate_tier = AffiliateTier.objects.get(id=pk)
            return affiliate_tier
        except AffiliateTier.DoesNotExist:
            logger.warning(f"AffiliateTier not found: {pk}")
            raise ValueError("AffiliateTier not found")
     
    def create_affiliate_tier(self, data) -> AffiliateTier:
        try:
            affiliate_tier = AffiliateTier( 
                tier_name = data.get('tier_name'),
                min_sales = data.get('min_sales'),
                commission_rate = data.get('commission_rate'),
                tier_benefits = data.get('tier_benefits'),
                access_level = data.get('access_level'),
                next_tier_threshold = data.get('next_tier_threshold'),
                tier_expiration = data.get('tier_expiration'))
            
            affiliate_tier.save()
 
            programs = Affiliate.objects.filter(id__in=data['programs'])
            affiliate_tier.programs.set(programs)

            logger.info(f"AffiliateTier created: {affiliate_tier}")
            return affiliate_tier
        except Exception as e:
            logger.error(f"Error creating affiliate_tier: {e}")
            raise e
 
    def update_affiliate_tier(self, pk, data) -> AffiliateTier:
        try:
            affiliate_tier = self.get_affiliate_tier(pk)
            for key, value in data.items():
                setattr(affiliate_tier, key, value)
            affiliate_tier.save()
            logger.info(f"AffiliateTier updated: {affiliate_tier}")
            return affiliate_tier
        except Exception as e:
            logger.error(f"Error updating affiliate_tier: {e}")
            raise e
    
    def delete_affiliate_tier(self, pk) -> None:
        try:
            affiliate_tier = self.get_affiliate_tier(pk)
            affiliate_tier.delete()
            logger.info(f"AffiliateTier deleted: {affiliate_tier}")
        except Exception as e:
            logger.error(f"Error deleting affiliate_tier: {e}")
            raise e