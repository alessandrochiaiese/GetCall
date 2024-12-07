# referral_system/services.py

import logging

from django.db.models.manager import BaseManager
from django.contrib.auth import get_user_model

from referral.models.referral_campaign import ReferralCampaign
from referral.models.referral_program import ReferralProgram

User = get_user_model()


# Set up a logger
logger = logging.getLogger(__name__)


class ReferralCampaignService():
    def __init__(self) -> None:
        pass
    
    def get_referral_campaigns(self) -> BaseManager[ReferralCampaign]:
        try:
            referral_campaigns = ReferralCampaign.objects.all() 
            return referral_campaigns
        except ReferralCampaign.DoesNotExist:
            logger.warning(f"ReferralCampaign not found")
            raise ValueError("ReferralCampaign not found")
     
    def get_referral_campaign(self, pk) -> ReferralCampaign:
        try:
            referral_campaign = ReferralCampaign.objects.get(id=pk)
            return referral_campaign
        except ReferralCampaign.DoesNotExist:
            logger.warning(f"ReferralCampaign not found: {pk}")
            raise ValueError("ReferralCampaign not found")
     
    def create_referral_campaign(self, data) -> ReferralCampaign:
        try:
            # Associa il programma esistente
            program = ReferralProgram.objects.get(id=data['program_id'])

            referral_campaign = ReferralCampaign( 
                campaign_name = data.get('campaign_name'),
                start_date = data.get('start_date'),
                end_date = data.get('end_date'),
                goal = data.get('goal'),
                budget = data.get('budget'),
                spending_to_date = 0, #data.get('spending_to_date'),
                target_audience = data.get('target_audience', None))
            referral_campaign.save()

            referral_programs = ReferralProgram.objects.filter(id__in=data['referral_programs'])
            referral_campaign.programs.set(referral_programs)

            # Aggiorna le statistiche del programma
            program.stats.total_campaigns += 1
            program.stats.save()

            logger.info(f"ReferralCampaign created: {referral_campaign}")
            return referral_campaign
        except Exception as e:
            logger.error(f"Error creating referral_campaign: {e}")
            raise e
 
    def update_referral_campaign(self, pk, data) -> ReferralCampaign:
        try:
            referral_campaign = self.get_referral_campaign(pk)
            for key, value in data.items():
                setattr(referral_campaign, key, value)
            referral_campaign.save()
            logger.info(f"ReferralCampaign updated: {referral_campaign}")
            return referral_campaign
        except ReferralCampaign.DoesNotExist:
            logger.warning(f"ReferralCampaign not found: {pk}")
            raise ValueError("ReferralCampaign not found")
        except Exception as e:
            logger.error(f"Error updating referral_campaign: {e}")
            raise e
    
    def delete_referral_campaign(self, pk) -> None:
        try:
            referral_campaign = self.get_referral_campaign(pk)
            referral_campaign.delete()
            logger.info(f"ReferralCampaign deleted: {referral_campaign}")
        except ReferralCampaign.DoesNotExist:
            logger.warning(f"ReferralCampaign not found: {pk}")
            raise ValueError("ReferralCampaign not found")
        except Exception as e:
            logger.error(f"Error deleting referral_campaign: {e}")
            raise e
        