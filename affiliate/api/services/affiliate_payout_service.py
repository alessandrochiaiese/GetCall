import datetime
import logging
from typing import List
from django.http import JsonResponse
from affiliate.models.affiliate import Affiliate
from affiliate.models.affiliate_payout import AffiliatePayout
from affiliate.api.serializers import AffiliatePayoutSerializer 

# Set up a logger
logger = logging.getLogger(__name__)

class AffiliatePayoutService():
    def __init__(self) -> None:
        pass

    def get_affiliate_payouts(self) ->  List[AffiliatePayout]:
        try:
            affiliate_payouts = AffiliatePayout.objects.all() 
            return affiliate_payouts
        except AffiliatePayout.DoesNotExist:
            logger.warning(f"AffiliatePayout not found")
            raise ValueError("AffiliatePayout not found")
     
    def get_affiliate_payout(self, pk) -> AffiliatePayout:
        try:
            affiliate_payout = AffiliatePayout.objects.get(id=pk)
            return affiliate_payout
        except AffiliatePayout.DoesNotExist:
            logger.warning(f"AffiliatePayout not found: {pk}")
            raise ValueError("AffiliatePayout not found")
     
    def create_affiliate_payout(self, data) -> AffiliatePayout:
        try:
            affiliate_payout = AffiliatePayout( 
                amount = data.get('amount'),
                currency = data.get('currency'),
                payout_date = data.get('payout_date'),
                payout_method = data.get('payout_method'),
                payout_status = data.get('payout_status'),
                transaction_id = data.get('transaction_id'),
                processing_fee = data.get('processing_fee'),
                net_amount = data.get('net_amount'),
                payout_provider = data.get('payout_provider'))

            affiliate_payout.save()

            affiliates = Affiliate.objects.filter(id__in=data['affiliates'])
            affiliate_payout.affiliates.set(affiliates)
            
            logger.info(f"AffiliatePayout created: {affiliate_payout}")
            return affiliate_payout
        except Exception as e:
            logger.error(f"Error creating affiliate_payout: {e}")
            raise e
 
    def update_affiliate_payout(self, pk, data) -> AffiliatePayout:
        try:
            affiliate_payout = self.get_affiliate_payout(pk)
            for key, value in data.items():
                setattr(affiliate_payout, key, value)
            affiliate_payout.save()
            logger.info(f"AffiliatePayout updated: {affiliate_payout}")
            return affiliate_payout
        except Exception as e:
            logger.error(f"Error updating affiliate_payout: {e}")
            raise e
    
    def delete_affiliate_payout(self, pk) -> None:
        try:
            affiliate_payout = self.get_affiliate_payout(pk)
            affiliate_payout.delete()
            logger.info(f"AffiliatePayout deleted: {affiliate_payout}")
        except Exception as e:
            logger.error(f"Error deleting affiliate_payout: {e}")
            raise e