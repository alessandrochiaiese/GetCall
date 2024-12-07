import datetime
import logging
from typing import List
from django.http import JsonResponse
from affiliate.models.affiliate import Affiliate
from affiliate.models.affiliate_commission import AffiliateCommission
from affiliate.api.serializers import AffiliateCommissionSerializer
from affiliate.models.affiliate_program import AffiliateProgram 

# Set up a logger
logger = logging.getLogger(__name__)

class AffiliateCommissionService():
    def __init__(self) -> None:
        pass

    def get_affiliate_commissions(self) ->  List[AffiliateCommission]:
        try:
            affiliate_commissions = AffiliateCommission.objects.all() 
            return affiliate_commissions
        except AffiliateCommission.DoesNotExist:
            logger.warning(f"AffiliateCommission not found")
            raise ValueError("AffiliateCommission not found")
     
    def get_affiliate_commission(self, pk) -> AffiliateCommission:
        try:
            affiliate_commission = AffiliateCommission.objects.get(id=pk)
            return affiliate_commission
        except AffiliateCommission.DoesNotExist:
            logger.warning(f"AffiliateCommission not found: {pk}")
            raise ValueError("AffiliateCommission not found")
     
    def create_affiliate_commission(self, data) -> AffiliateCommission:
        try:
            affiliate_commission = AffiliateCommission( 
                amount = data.get('amonut'),
                currency = data.get('currency'),
                date_awarded = data.get('date_awarded'),
                status = data.get('status'),
                approved_by = data.get('approved_by'), 
                commission_type = data.get('commission_type'),
                description = data.get('description'),
                tier = data.get('tier'))

            affiliate_commission.save()
 
            affiliates = Affiliate.objects.filter(id__in=data['affiliates'])
            affiliate_commission.affiliates.set(affiliates)

            programs = AffiliateProgram.objects.filter(id__in=data['programs'])
            affiliate_commission.programs.set(programs)

            logger.info(f"AffiliateCommission created: {affiliate_commission}")
            return affiliate_commission
        except Exception as e:
            logger.error(f"Error creating affiliate_commission: {e}")
            raise e
 
    def update_affiliate_commission(self, pk, data) -> AffiliateCommission:
        try:
            affiliate_commission = self.get_affiliate_commission(pk)
            for key, value in data.items():
                setattr(affiliate_commission, key, value)
            affiliate_commission.save()
            logger.info(f"AffiliateCommission updated: {affiliate_commission}")
            return affiliate_commission
        except Exception as e:
            logger.error(f"Error updating affiliate_commission: {e}")
            raise e
    
    def delete_affiliate_commission(self, pk) -> None:
        try:
            affiliate_commission = self.get_affiliate_commission(pk)
            affiliate_commission.delete()
            logger.info(f"AffiliateCommission deleted: {affiliate_commission}")
        except Exception as e:
            logger.error(f"Error deleting affiliate_commission: {e}")
            raise e