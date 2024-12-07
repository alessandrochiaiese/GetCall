import datetime
import logging
from typing import List
from django.http import JsonResponse
from affiliate.models.affiliate import Affiliate
from affiliate.models.affiliate_link import AffiliateLink
from affiliate.api.serializers import AffiliateLinkSerializer
from affiliate.models.affiliate_program import AffiliateProgram 

# Set up a logger
logger = logging.getLogger(__name__)

class AffiliateLinkService():
    def __init__(self) -> None:
        pass

    def get_affiliate_links(self) ->  List[AffiliateLink]:
        try:
            affiliate_links = AffiliateLink.objects.all() 
            return affiliate_links
        except AffiliateLink.DoesNotExist:
            logger.warning(f"AffiliateLink not found")
            raise ValueError("AffiliateLink not found")
     
    def get_affiliate_link(self, pk) -> AffiliateLink:
        try:
            affiliate_link = AffiliateLink.objects.get(id=pk)
            return affiliate_link
        except AffiliateLink.DoesNotExist:
            logger.warning(f"AffiliateLink not found: {pk}")
            raise ValueError("AffiliateLink not found")
     
    def create_affiliate_link(self, data) -> AffiliateLink:
        try:
            affiliate_link = AffiliateLink( 
                url = data.get('url'),
                click_count = data.get('click_count'),
                conversion_count = data.get('date_created'),
                date_created = data.get('program'),
                last_used = data.get('last_used'),
                link_status = data.get('link_status'),
                landing_page = data.get('landing_page'), 
                custom_tracking_id = data.get('custom_tracking_id'))

            affiliate_link.save()

            affiliates = Affiliate.objects.filter(id__in=data['affiliates'])
            affiliate_link.affiliates.set(affiliates)
            
            programs = AffiliateProgram.objects.filter(id__in=data['programs'])
            affiliate_link.programs.set(programs)
            
            logger.info(f"AffiliateLink created: {affiliate_link}")
            return affiliate_link
        except Exception as e:
            logger.error(f"Error creating affiliate_link: {e}")
            raise e
 
    def update_affiliate_link(self, pk, data) -> AffiliateLink:
        try:
            affiliate_link = self.get_affiliate_link(pk)
            for key, value in data.items():
                setattr(affiliate_link, key, value)
            affiliate_link.save()
            logger.info(f"AffiliateLink updated: {affiliate_link}")
            return affiliate_link
        except Exception as e:
            logger.error(f"Error updating affiliate_link: {e}")
            raise e
    
    def delete_affiliate_link(self, pk) -> None:
        try:
            affiliate_link = self.get_affiliate_link(pk)
            affiliate_link.delete()
            logger.info(f"AffiliateLink deleted: {affiliate_link}")
        except Exception as e:
            logger.error(f"Error deleting affiliate_link: {e}")
            raise e