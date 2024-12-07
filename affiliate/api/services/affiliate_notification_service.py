import datetime
import logging
from typing import List
from django.http import JsonResponse
from affiliate.models.affiliate_notification import AffiliateNotification
from affiliate.api.serializers import AffiliateNotificationSerializer 

# Set up a logger
logger = logging.getLogger(__name__)

class AffiliateNotificationService():
    def __init__(self) -> None:
        pass

    def get_affiliate_notifications(self) ->  List[AffiliateNotification]:
        try:
            affiliate_notifications = AffiliateNotification.objects.all() 
            return affiliate_notifications
        except AffiliateNotification.DoesNotExist:
            logger.warning(f"AffiliateNotification not found")
            raise ValueError("AffiliateNotification not found")
     
    def get_affiliate_notification(self, pk) -> AffiliateNotification:
        try:
            affiliate_notification = AffiliateNotification.objects.get(id=pk)
            return affiliate_notification
        except AffiliateNotification.DoesNotExist:
            logger.warning(f"AffiliateNotification not found: {pk}")
            raise ValueError("AffiliateNotification not found")
     
    def create_affiliate_notification(self, data) -> AffiliateNotification:
        try:
            affiliate_notification = AffiliateNotification(
                message = data.get('message'),
                date_sent = data.get('date_sent'),
                is_read = data.get('is_read'),
                priority = data.get('priority'),
                notification_type = data.get('notification_type'))

            affiliate_notification.save()

            affiliates = AffiliateNotification.objects.filter(id__in=data['affiliates'])
            affiliate_notification.affiliates.set(affiliates)
            
            logger.info(f"AffiliateNotification created: {affiliate_notification}")
            return affiliate_notification
        except Exception as e:
            logger.error(f"Error creating affiliate_notification: {e}")
            raise e
 
    def update_affiliate_notification(self, pk, data) -> AffiliateNotification:
        try:
            affiliate_notification = self.get_affiliate_notification(pk)
            for key, value in data.items():
                setattr(affiliate_notification, key, value)
            affiliate_notification.save()
            logger.info(f"AffiliateNotification updated: {affiliate_notification}")
            return affiliate_notification
        except Exception as e:
            logger.error(f"Error updating affiliate_notification: {e}")
            raise e
    
    def delete_affiliate_notification(self, pk) -> None:
        try:
            affiliate_notification = self.get_affiliate_notification(pk)
            affiliate_notification.delete()
            logger.info(f"AffiliateNotification deleted: {affiliate_notification}")
        except Exception as e:
            logger.error(f"Error deleting affiliate_notification: {e}")
            raise e