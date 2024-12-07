import datetime
import logging
from typing import List
from django.http import JsonResponse
from affiliate.models.affiliate_campaign import AffiliateCampaign
from affiliate.api.serializers import AffiliateCampaignSerializer
from affiliate.models.affiliate_program import AffiliateProgram 

# Set up a logger
logger = logging.getLogger(__name__)

class AffiliateCampaignService():
    def __init__(self) -> None:
        pass

    def get_affiliate_campaigns(self) ->  List[AffiliateCampaign]:
        try:
            affiliate_campaigns = AffiliateCampaign.objects.all() 
            return affiliate_campaigns
        except AffiliateCampaign.DoesNotExist:
            logger.warning(f"AffiliateCampaign not found")
            raise ValueError("AffiliateCampaign not found")
     
    def get_affiliate_campaign(self, pk) -> AffiliateCampaign:
        try:
            affiliate_campaign = AffiliateCampaign.objects.get(id=pk)
            return affiliate_campaign
        except AffiliateCampaign.DoesNotExist:
            logger.warning(f"AffiliateCampaign not found: {pk}")
            raise ValueError("AffiliateCampaign not found")
     
    def create_affiliate_campaign(self, data) -> AffiliateCampaign:
        try:
            affiliate_campaign = AffiliateCampaign( 
                campaign_name = data.get('campaign_name'),
                start_date = data.get('start_date'),
                end_date = data.get('end_date'),
                goal = data.get('goal'),
                budget = data.get('budget'),
                spending_to_date = data.get('spending_to_date'))
            affiliate_campaign.save()

            programs = AffiliateProgram.objects.filter(id__in=data['programs'])
            affiliate_campaign.programs.set(programs)

            logger.info(f"AffiliateCampaign created: {affiliate_campaign}")
            return affiliate_campaign
        except Exception as e:
            logger.error(f"Error creating affiliate_campaign: {e}")
            raise e
 
    def update_affiliate_campaign(self, pk, data) -> AffiliateCampaign:
        try:
            affiliate_campaign = self.get_affiliate_campaign(pk)
            for key, value in data.items():
                setattr(affiliate_campaign, key, value)
            affiliate_campaign.save()
            logger.info(f"AffiliateCampaign updated: {affiliate_campaign}")
            return affiliate_campaign
        except Exception as e:
            logger.error(f"Error updating affiliate_campaign: {e}")
            raise e
    
    def delete_affiliate_campaign(self, pk) -> None:
        try:
            affiliate_campaign = self.get_affiliate_campaign(pk)
            affiliate_campaign.delete()
            logger.info(f"AffiliateCampaign deleted: {affiliate_campaign}")
        except Exception as e:
            logger.error(f"Error deleting affiliate_campaign: {e}")
            raise e