import datetime
import logging
from typing import List
from django.http import JsonResponse
from affiliate.models import AffiliateSettings
from affiliate.api.serializers import AffiliateSettingsSerializer
from affiliate.models.affiliate import Affiliate 

# Set up a logger
logger = logging.getLogger(__name__)

class AffiliateSettingsService():
    def __init__(self) -> None:
        pass

    def get_affiliate_settings(self) ->  List[AffiliateSettings]:
        try:
            affiliate_settings = AffiliateSettings.objects.all() 
            return affiliate_settings
        except AffiliateSettings.DoesNotExist:
            logger.warning(f"AffiliateSettings not found")
            raise ValueError("AffiliateSettings not found")
     
    def get_affiliate_setting(self, pk) -> AffiliateSettings:
        try:
            affiliate_setting = AffiliateSettings.objects.get(id=pk)
            return affiliate_setting
        except AffiliateSettings.DoesNotExist:
            logger.warning(f"AffiliateSettings not found: {pk}")
            raise ValueError("AffiliateSettings not found")
     
    def create_affiliate_setting(self, data) -> AffiliateSettings:
        try:
            affiliate_setting = AffiliateSettings(
                preferred_currency = data.get('preferred_currency'),
                preferred_payment_method = data.get('preferred_payment_method'),
                payout_schedule = data.get('payout_schedule'),
                notification_preference = data.get('notification_preference'),
                dashboard_layout = data.get('dashboard_layout'))

            affiliate_setting.save() 
            
            affiliates = Affiliate.objects.filter(id__in=data['affiliates'])
            affiliate_setting.affiliates.set(affiliates)

            logger.info(f"AffiliateSettings created: {affiliate_setting}")
            return affiliate_setting
        except Exception as e:
            logger.error(f"Error creating affiliate_setting: {e}")
            raise e
 
    def update_affiliate_setting(self, pk, data) -> AffiliateSettings:
        try:
            affiliate_setting = self.get_affiliate_setting(pk)
            for key, value in data.items():
                setattr(affiliate_setting, key, value)
            affiliate_setting.save()
            logger.info(f"AffiliateSettings updated: {affiliate_setting}")
            return affiliate_setting
        except Exception as e:
            logger.error(f"Error updating affiliate_setting: {e}")
            raise e
    
    def delete_affiliate_setting(self, pk) -> None:
        try:
            affiliate_setting = self.get_affiliate_setting(pk)
            affiliate_setting.delete()
            logger.info(f"AffiliateSettings deleted: {affiliate_setting}")
        except Exception as e:
            logger.error(f"Error deleting affiliate_setting: {e}")
            raise e