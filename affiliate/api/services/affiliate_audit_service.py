import datetime
import logging
from typing import List
from django.http import JsonResponse
from affiliate.models.affiliate import Affiliate
from affiliate.models.affiliate_audit import AffiliateAudit
from affiliate.api.serializers import AffiliateAuditSerializer 

# Set up a logger
logger = logging.getLogger(__name__)

class AffiliateAuditService():
    def __init__(self) -> None:
        pass

    def get_affiliate_audits(self) ->  List[AffiliateAudit]:
        try:
            affiliate_audits = AffiliateAudit.objects.all() 
            return affiliate_audits
        except AffiliateAudit.DoesNotExist:
            logger.warning(f"AffiliateAudit not found")
            raise ValueError("AffiliateAudit not found")
     
    def get_affiliate_audit(self, pk) -> AffiliateAudit:
        try:
            affiliate_audit = AffiliateAudit.objects.get(id=pk)
            return affiliate_audit
        except AffiliateAudit.DoesNotExist:
            logger.warning(f"AffiliateAudit not found: {pk}")
            raise ValueError("AffiliateAudit not found")
     
    def create_affiliate_audit(self, data) -> AffiliateAudit:
        try:
            affiliate_audit = AffiliateAudit( 
                action_taken = data.get('action_taken'),
                action_date = data.get('action_date'),
                ip_address = data.get('ip_address'),
                device_info = data.get('device_info'),
                location = data.get('location'))
            affiliate_audit.save()
 
            affiliates = Affiliate.objects.filter(id__in=data['affiliates'])
            affiliate_audit.affiliates.set(affiliates)

            logger.info(f"AffiliateAudit created: {affiliate_audit}")
            return affiliate_audit
        except Exception as e:
            logger.error(f"Error creating affiliate_audit: {e}")
            raise e
 
    def update_affiliate_audit(self, pk, data) -> AffiliateAudit:
        try:
            affiliate_audit = self.get_affiliate_audit(pk)
            for key, value in data.items():
                setattr(affiliate_audit, key, value)
            affiliate_audit.save()
            logger.info(f"AffiliateAudit updated: {affiliate_audit}")
            return affiliate_audit
        except Exception as e:
            logger.error(f"Error updating affiliate_audit: {e}")
            raise e
    
    def delete_affiliate_audit(self, pk) -> None:
        try:
            affiliate_audit = self.get_affiliate_audit(pk)
            affiliate_audit.delete()
            logger.info(f"AffiliateAudit deleted: {affiliate_audit}")
        except Exception as e:
            logger.error(f"Error deleting affiliate_audit: {e}")
            raise e