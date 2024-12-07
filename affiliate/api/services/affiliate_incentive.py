import datetime
import logging
from typing import List
from django.http import JsonResponse
from affiliate.models.affiliate import Affiliate
from affiliate.models.affiliate_incentive import AffiliateIncentive
from affiliate.api.serializers import AffiliateIncentiveSerializer
from affiliate.models.affiliate_program import AffiliateProgram 

# Set up a logger
logger = logging.getLogger(__name__)

class AffiliateIncentiveService():
    def __init__(self) -> None:
        pass

    def get_affiliate_incentives(self) ->  List[AffiliateIncentive]:
        try:
            affiliate_incentives = AffiliateIncentive.objects.all() 
            return affiliate_incentives
        except AffiliateIncentive.DoesNotExist:
            logger.warning(f"AffiliateIncentive not found")
            raise ValueError("AffiliateIncentive not found")
     
    def get_affiliate_incentive(self, pk) -> AffiliateIncentive:
        try:
            affiliate_incentive = AffiliateIncentive.objects.get(id=pk)
            return affiliate_incentive
        except AffiliateIncentive.DoesNotExist:
            logger.warning(f"AffiliateIncentive not found: {pk}")
            raise ValueError("AffiliateIncentive not found")
     
    def create_affiliate_incentive(self, data) -> AffiliateIncentive:
        try:
            affiliate_incentive = AffiliateIncentive( 
                affiliate = data.get('affiliate'),
                program = data.get('program'),
                incentive_type = data.get('incentive_type'),
                date = data.get('date'),
                amount = data.get('amount'),
                currency = data.get('currency'),
                status = data.get('status'),
                description = data.get('description'),
                ip_address = data.get('ip_address'),
                device_info = data.get('device_info'),
                tracking_id = data.get('tracking_id'),
                expiration_date = data.get('expiration_date'),
                is_incentive_active = data.get('is_incentive_active'))

            affiliate_incentive.save()
 
            logger.info(f"AffiliateIncentive created: {affiliate_incentive}")
            return affiliate_incentive
        except Exception as e:
            logger.error(f"Error creating affiliate_incentive: {e}")
            raise e
 
    def update_affiliate_incentive(self, pk, data) -> AffiliateIncentive:
        try:
            affiliate_incentive = self.get_affiliate_incentive(pk)
            for key, value in data.items():
                setattr(affiliate_incentive, key, value)
            affiliate_incentive.save()
            logger.info(f"AffiliateIncentive updated: {affiliate_incentive}")
            return affiliate_incentive
        except Exception as e:
            logger.error(f"Error updating affiliate_incentive: {e}")
            raise e
    
    def delete_affiliate_incentive(self, pk) -> None:
        try:
            affiliate_incentive = self.get_affiliate_incentive(pk)
            affiliate_incentive.delete()
            logger.info(f"AffiliateIncentive deleted: {affiliate_incentive}")
        except Exception as e:
            logger.error(f"Error deleting affiliate_incentive: {e}")
            raise e