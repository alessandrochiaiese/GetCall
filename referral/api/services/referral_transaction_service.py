# referral_system/services.py

import logging

from django.db.models.manager import BaseManager
from django.contrib.auth import get_user_model

from referral.models.referral_transaction import ReferralTransaction

User = get_user_model()

# Set up a logger
logger = logging.getLogger(__name__)


class ReferralTransactionService():
    def __init__(self) -> None:
        pass
    
    def get_referral_transactions(self) -> BaseManager[ReferralTransaction]:
        try:
            referral_transactions = ReferralTransaction.objects.all() 
            return referral_transactions
        except ReferralTransaction.DoesNotExist:
            logger.warning(f"ReferralTransaction not found")
            raise ValueError("ReferralTransaction not found")
     
    def get_referral_transaction(self, pk) -> ReferralTransaction:
        try:
            referral_transaction = ReferralTransaction.objects.get(id=pk)
            return referral_transaction
        except ReferralTransaction.DoesNotExist:
            logger.warning(f"ReferralTransaction not found: {pk}")
            raise ValueError("ReferralTransaction not found")
     
    def create_referral_transaction(self, data) -> ReferralTransaction:
        try:
            referral_transaction = ReferralTransaction(
                program = data.get('program'),
                referred_users = data.get('referred_users'),
                transaction_date = data.get('transaction_date'),
                order_id = data.get('order_id'),
                transaction_amount = data.get('transaction_amount'),
                currency = data.get('currency'),
                conversion_value = data.get('conversion_value'),
                discount_value = data.get('discount_value'),
                coupon_code_used = data.get('coupon_code_used'),
                channel = data.get('channel')
            )
            referral_transaction.save()
            logger.info(f"ReferralTransaction created: {referral_transaction}")
            return referral_transaction
        except Exception as e:
            logger.error(f"Error creating referral_transaction: {e}")
            raise e
 
    def update_referral_transaction(self, pk, data) -> ReferralTransaction:
        try:
            referral_transaction = self.get_referral_transaction(pk)
            for key, value in data.items():
                setattr(referral_transaction, key, value)
            referral_transaction.save()
            logger.info(f"ReferralTransaction updated: {referral_transaction}")
            return referral_transaction
        except ReferralTransaction.DoesNotExist:
            logger.warning(f"ReferralTransaction not found: {pk}")
            raise ValueError("ReferralTransaction not found")
        except Exception as e:
            logger.error(f"Error updating referral_transaction: {e}")
            raise e
    
    def delete_referral_transaction(self, pk) -> None:
        try:
            referral_transaction = self.get_referral_transaction(pk)
            referral_transaction.delete()
            logger.info(f"ReferralTransaction deleted: {referral_transaction}")
        except ReferralTransaction.DoesNotExist:
            logger.warning(f"ReferralTransaction not found: {pk}")
            raise ValueError("ReferralTransaction not found")
        except Exception as e:
            logger.error(f"Error deleting referral_transaction: {e}")
            raise e
        