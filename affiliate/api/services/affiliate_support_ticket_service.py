import datetime
import logging
from typing import List
from django.http import JsonResponse
from affiliate.models.affiliate import Affiliate
from affiliate.models.affiliate_support_ticket import AffiliateSupportTicket
from affiliate.api.serializers import AffiliateSupportTicketSerializer 

# Set up a logger
logger = logging.getLogger(__name__)

class AffiliateSupportTicketService():
    def __init__(self) -> None:
        pass

    def get_affiliate_support_tickets(self) ->  List[AffiliateSupportTicket]:
        try:
            affiliate_support_tickets = AffiliateSupportTicket.objects.all() 
            return affiliate_support_tickets
        except AffiliateSupportTicket.DoesNotExist:
            logger.warning(f"AffiliateSupportTicket not found")
            raise ValueError("AffiliateSupportTicket not found")
     
    def get_affiliate_support_ticket(self, pk) -> AffiliateSupportTicket:
        try:
            affiliate_support_ticket = AffiliateSupportTicket.objects.get(id=pk)
            return affiliate_support_ticket
        except AffiliateSupportTicket.DoesNotExist:
            logger.warning(f"AffiliateSupportTicket not found: {pk}")
            raise ValueError("AffiliateSupportTicket not found")
     
    def create_affiliate_support_ticket(self, data) -> AffiliateSupportTicket:
        try:
            affiliate_support_ticket = AffiliateSupportTicket( 
                ticket_number = data.get('ticket_number'),
                subject = data.get('subject'),
                description = data.get('description'),
                status = data.get('status'),
                date_created = data.get('date_created'),
                date_closed = data.get('date_closed'),
                priority = data.get('priority'),
                assigned_agent = data.get('assigned_agent'))

            affiliate_support_ticket.save() 
            
            affiliates = Affiliate.objects.filter(id__in=data['affiliates'])
            affiliate_support_ticket.affiliates.set(affiliates)

            logger.info(f"AffiliateSupportTicket created: {affiliate_support_ticket}")
            return affiliate_support_ticket
        except Exception as e:
            logger.error(f"Error creating affiliate_support_ticket: {e}")
            raise e
 
    def update_affiliate_support_ticket(self, pk, data) -> AffiliateSupportTicket:
        try:
            affiliate_support_ticket = self.get_affiliate_support_ticket(pk)
            for key, value in data.items():
                setattr(affiliate_support_ticket, key, value)
            affiliate_support_ticket.save()
            logger.info(f"AffiliateSupportTicket updated: {affiliate_support_ticket}")
            return affiliate_support_ticket
        except Exception as e:
            logger.error(f"Error updating affiliate_support_ticket: {e}")
            raise e
    
    def delete_affiliate_support_ticket(self, pk) -> None:
        try:
            affiliate_support_ticket = self.get_affiliate_support_ticket(pk)
            affiliate_support_ticket.delete()
            logger.info(f"AffiliateSupportTicket deleted: {affiliate_support_ticket}")
        except Exception as e:
            logger.error(f"Error deleting affiliate_support_ticket: {e}")
            raise e