# referral_system/services.py

import logging
 
from django.contrib.auth import get_user_model
from typing import List

from referral.models.referral_code import ReferralCode
from referral.models.referral_conversion import ReferralConversion
 

User = get_user_model()


# Set up a logger
logger = logging.getLogger(__name__)


class ReferralConversionService():
    def __init__(self) -> None:
        pass
    
    def get_referral_conversions(self) -> List[ReferralConversion]:
        try:
            referral_conversions = ReferralConversion.objects.all() 
            return referral_conversions
        except ReferralConversion.DoesNotExist:
            logger.warning(f"ReferralConversion not found")
            raise ValueError("ReferralConversion not found")
     
    def get_referral_conversion(self, pk) -> ReferralConversion:
        try:
            referral_conversion = ReferralConversion.objects.get(id=pk)
            return referral_conversion
        except ReferralConversion.DoesNotExist:
            logger.warning(f"ReferralConversion not found: {pk}")
            raise ValueError("ReferralConversion not found")
     
    def create_referral_conversion(self, data) -> ReferralConversion:
        try:
            referral_conversion = ReferralConversion(
                referral_user = data.get('referral_user'),
                conversion_date = data.get('conversion_date'),
                conversion_value = data.get('conversion_value'),
                conversion = data.get('conversion'),
                status = data.get('status'),
                reward_issued = data.get('reward_issued'),
                conversion_source = data.get('conversion_source'),
                referral_type = data.get('referral_type'))
            referral_conversion.save() 
            
            referral_codes = ReferralCode.objects.filter(id__in=data['referral_codes'])
            referral_conversion.referral_codes.set(referral_codes)

            logger.info(f"ReferralConversion created: {referral_conversion}")
            return referral_conversion
        except Exception as e:
            logger.error(f"Error creating referral_conversion: {e}")
            raise e
 
    def update_referral_conversion(self, pk, data) -> ReferralConversion:
        try:
            referral_conversion = self.get_referral_conversion(pk)
            for key, value in data.items():
                setattr(referral_conversion, key, value)
            referral_conversion.save()
            logger.info(f"ReferralConversion updated: {referral_conversion}")
            return referral_conversion
        except ReferralConversion.DoesNotExist:
            logger.warning(f"ReferralConversion not found: {pk}")
            raise ValueError("ReferralConversion not found")
        except Exception as e:
            logger.error(f"Error updating referral_conversion: {e}")
            raise e
    
    def delete_referral_conversion(self, pk) -> None:
        try:
            referral_conversion = self.get_referral_conversion(pk)
            referral_conversion.delete()
            logger.info(f"ReferralConversion deleted: {referral_conversion}")
        except ReferralConversion.DoesNotExist:
            logger.warning(f"ReferralConversion not found: {pk}")
            raise ValueError("ReferralConversion not found")
        except Exception as e:
            logger.error(f"Error deleting referral_conversion: {e}")
            raise e
        