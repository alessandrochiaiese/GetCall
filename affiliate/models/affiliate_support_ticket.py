from django.db import models

class AffiliateSupportTicket(models.Model):
    affiliates = models.ManyToManyField('Affiliate', related_name='affiliate_supportticket_affiliates') 
    ticket_number = models.CharField(max_length=100)
    subject = models.CharField(max_length=255)
    description = models.TextField()
    status = models.CharField(max_length=50)
    date_created = models.DateField()
    date_closed = models.DateField(null=True, blank=True)
    priority = models.CharField(max_length=50)
    assigned_agent = models.CharField(max_length=255)

    class Meta: 
        verbose_name = "Affiliate Support Ticket"
        verbose_name_plural = "Affiliate Support Tickets"

"""
class AffiliateSupportTicket(models.Model):
    affiliate = models.OneToOneField('Affiliate', on_delete=models.CASCADE)
    ticket_number = models.CharField(max_length=255, unique=True)
    subject = models.CharField(max_length=255)
    description = models.TextField()
    status = models.CharField(max_length=50, choices=[("open", "Open"), ("closed", "Closed")])
    date_created = models.DateTimeField(auto_now_add=True)
    date_closed = models.DateTimeField(null=True, blank=True)
"""