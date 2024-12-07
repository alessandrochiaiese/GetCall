import datetime
import logging
from typing import List
from django.http import JsonResponse
import affiliate
from affiliate.models.affiliate import Affiliate
from affiliate.models.affiliate_performance import AffiliatePerformance
from affiliate.api.serializers import AffiliatePerformanceSerializer 

# Set up a logger
logger = logging.getLogger(__name__)

class AffiliatePerformanceService():
    def __init__(self) -> None:
        pass

    def get_affiliate_performances(self) ->  List[AffiliatePerformance]:
        try:
            affiliate_performances = AffiliatePerformance.objects.all() 
            return affiliate_performances
        except AffiliatePerformance.DoesNotExist:
            logger.warning(f"AffiliatePerformance not found")
            raise ValueError("AffiliatePerformance not found")
     
    def get_affiliate_performance(self, pk) -> AffiliatePerformance:
        try:
            affiliate_performance = AffiliatePerformance.objects.get(id=pk)
            return affiliate_performance
        except AffiliatePerformance.DoesNotExist:
            logger.warning(f"AffiliatePerformance not found: {pk}")
            raise ValueError("AffiliatePerformance not found")
     
    def create_affiliate_performance(self, data) -> AffiliatePerformance:
        try:
            affiliate_performance = AffiliatePerformance( 
                period = data.get('period'),
                total_clicks = data.get('total_clicks'),
                total_conversions = data.get('total_conversions'),
                conversion_rate = data.get('conversion_rate'),
                total_earnings = data.get('total_earnings'),
                average_order_value = data.get('average_order_value'),
                refund_rate = data.get('refund_rate'),
                customer_lifetime_value = data.get('customer_lifetime_value'),
                top_product = data.get('top_product'))

            affiliate_performance.save()
            
            affiliates = Affiliate.objects.filter(id__in=data['affiliates'])
            affiliate_performance.affiliates.set(affiliates)

            logger.info(f"AffiliatePerformance created: {affiliate_performance}")
            return affiliate_performance
        except Exception as e:
            logger.error(f"Error creating affiliate_performance: {e}")
            raise e
 
    def update_affiliate_performance(self, pk, data) -> AffiliatePerformance:
        try:
            affiliate_performance = self.get_affiliate_performance(pk)
            for key, value in data.items():
                setattr(affiliate_performance, key, value)
            affiliate_performance.save()
            logger.info(f"AffiliatePerformance updated: {affiliate_performance}")
            return affiliate_performance
        except Exception as e:
            logger.error(f"Error updating affiliate_performance: {e}")
            raise e
    
    def delete_affiliate_performance(self, pk) -> None:
        try:
            affiliate_performance = self.get_affiliate_performance(pk)
            affiliate_performance.delete()
            logger.info(f"AffiliatePerformance deleted: {affiliate_performance}")
        except Exception as e:
            logger.error(f"Error deleting affiliate_performance: {e}")
            raise e