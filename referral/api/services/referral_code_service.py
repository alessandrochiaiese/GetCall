# referral_system/services.py

import logging

from typing import List
from django.contrib.auth import get_user_model
from django.urls import reverse

from referral.models.referral_code import ReferralCode
from referral.models.referral_program import ReferralProgram

User = get_user_model()


# Set up a logger
logger = logging.getLogger(__name__)


class ReferralCodeService():
    def __init__(self) -> None:
        pass
    
    def get_referral_codes(self) -> List[ReferralCode]:
        try:
            referral_codes = ReferralCode.objects.all() 
            return referral_codes
        except ReferralCode.DoesNotExist:
            logger.warning(f"ReferralCode not found")
            raise ValueError("ReferralCode not found")
     
    def get_referral_code(self, pk) -> ReferralCode:
        try:
            referral_code = ReferralCode.objects.get(id=pk)
            return referral_code
        except ReferralCode.DoesNotExist:
            logger.warning(f"ReferralCode not found: {pk}")
            raise ValueError("ReferralCode not found")
     
    """def create_referral_code(self, data) -> ReferralCode:
        try:
            referral_code = ReferralCode(
                user = data.get('user'),
                code = data.get('code'),
                usage_count = data.get('usage_count'),
                date_created = data.get('date_created'),
                status = data.get('status'),
                expiry_date = data.get('expiry_date'),
                referred_user_count = data.get('referred_user_count'),
                unique_url = data.get('unique_url'),
                campaign_source = data.get('campaign_source'),
                campaign_medium = data.get('campaign_medium'))
            referral_code.save()

            referral_programs = ReferralProgram.objects.filter(id__in=data['referral_programs'])
            referral_code.programs.set(referral_programs)

            logger.info(f"ReferralCode created: {referral_code}")
            return referral_code
        except Exception as e:
            logger.error(f"Error creating referral_code: {e}")
            raise e"""


    def create_referral_code(self, data) -> ReferralCode:
        try:
            # Creazione dell'oggetto ReferralCode
            referral_code = ReferralCode(
                user = data.get('user'),
                code = data.get('code'),
                usage_count = data.get('usage_count'),
                date_created = data.get('date_created'),
                status = data.get('status'),
                expiry_date = data.get('expiry_date'),
                referred_user_count = data.get('referred_user_count'),
                unique_url = data.get('unique_url'),
                campaign_source = data.get('campaign_source'),
                campaign_medium = data.get('campaign_medium')
            )

            # Generazione dell'URL di referral unico
            current_site = data.get('url') #Site.objects.get_current()
            referral_url = f"{data.host}{reverse('referral', kwargs={'referral_code': referral_code.code})}"

            # Impostazione del URL di referral
            referral_code.unique_url = referral_url
            
            # Salvataggio del ReferralCode
            referral_code.save()

            # Associare i programmi di affiliazione
            referral_programs = ReferralProgram.objects.filter(id__in=data['referral_programs'])
            referral_code.programs.set(referral_programs)

            logger.info(f"ReferralCode created: {referral_code}")
            return referral_code
        except Exception as e:
            logger.error(f"Error creating referral_code: {e}")
            raise e

    def update_referral_code(self, pk, data) -> ReferralCode:
        try:
            referral_code = self.get_referral_code(pk)
            for key, value in data.items():
                setattr(referral_code, key, value)
            referral_code.save()
            logger.info(f"ReferralCode updated: {referral_code}")
            return referral_code
        except ReferralCode.DoesNotExist:
            logger.warning(f"ReferralCode not found: {pk}")
            raise ValueError("ReferralCode not found")
        except Exception as e:
            logger.error(f"Error updating referral_code: {e}")
            raise e
    
    def delete_referral_code(self, pk) -> None:
        try:
            referral_code = self.get_referral_code(pk)
            referral_code.delete()
            logger.info(f"ReferralCode deleted: {referral_code}")
        except ReferralCode.DoesNotExist:
            logger.warning(f"ReferralCode not found: {pk}")
            raise ValueError("ReferralCode not found")
        except Exception as e:
            logger.error(f"Error deleting referral_code: {e}")
            raise e
        