import datetime
import logging
from typing import List
from django.http import JsonResponse
from affiliate.models.affiliate_transaction import AffiliateTransaction
from affiliate.api.serializers import AffiliateTransactionSerializer 

# Set up a logger
logger = logging.getLogger(__name__)

class AffiliateTransactionService():
    def __init__(self) -> None:
        pass

    def get_affiliate_transactions(self) ->  List[AffiliateTransaction]:
        try:
            affiliate_transactions = AffiliateTransaction.objects.all() 
            return affiliate_transactions
        except AffiliateTransaction.DoesNotExist:
            logger.warning(f"AffiliateTransaction not found")
            raise ValueError("AffiliateTransaction not found")
     
    def get_affiliate_transaction(self, pk) -> AffiliateTransaction:
        try:
            affiliate_transaction = AffiliateTransaction.objects.get(id=pk)
            return affiliate_transaction
        except AffiliateTransaction.DoesNotExist:
            logger.warning(f"AffiliateTransaction not found: {pk}")
            raise ValueError("AffiliateTransaction not found")
     
    def create_affiliate_transaction(self, data) -> AffiliateTransaction:
        try:
            affiliate_transaction = AffiliateTransaction( 
                transaction_amount = data.get('transaction_amount'),
                transaction_date = data.get('transaction_date'),
                order_id = data.get('oreder_id'),
                product_id = data.get('product_id'),
                status = data.get('status'),
                payment_date = data.get('payment_date'),
                commission_rate = data.get('commission_rate'),
                discount_applied = data.get('discount_applied'),
                coupon_code = data.get('coupon_code')
            )
            affiliate_transaction.save()
 
            logger.info(f"AffiliateTransaction created: {affiliate_transaction}")
            return affiliate_transaction
        except Exception as e:
            logger.error(f"Error creating affiliate_transaction: {e}")
            raise e
 
    def update_affiliate_transaction(self, pk, data) -> AffiliateTransaction:
        try:
            affiliate_transaction = self.get_affiliate_transaction(pk)
            for key, value in data.items():
                setattr(affiliate_transaction, key, value)
            affiliate_transaction.save()
            logger.info(f"AffiliateTransaction updated: {affiliate_transaction}")
            return affiliate_transaction
        except Exception as e:
            logger.error(f"Error updating affiliate_transaction: {e}")
            raise e
    
    def delete_affiliate_transaction(self, pk) -> None:
        try:
            affiliate_transaction = self.get_affiliate_transaction(pk)
            affiliate_transaction.delete()
            logger.info(f"AffiliateTransaction deleted: {affiliate_transaction}")
        except Exception as e:
            logger.error(f"Error deleting affiliate_transaction: {e}")
            raise e