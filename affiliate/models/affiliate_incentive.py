from django.db import models
from django.utils import timezone
from decimal import Decimal 

class AffiliateIncentive(models.Model):
    INCENTIVE_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('declined', 'Declined'),
        ('expired', 'Expired'),
    ]
    
    INCENTIVE_TYPE_CHOICES = [
        ('click', 'Click'),
        ('signup', 'Signup'),
        ('purchase', 'Purchase'),
    ]

    affiliate = models.OneToOneField('Affiliate', on_delete=models.CASCADE, related_name='affiliate_incentive_affiliate')
    program = models.OneToOneField('AffiliateProgram', on_delete=models.CASCADE, related_name='affiliate_incentive_program')
    incentive_type = models.CharField(max_length=20, choices=INCENTIVE_TYPE_CHOICES)
    date = models.DateTimeField(default=timezone.now)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    currency = models.CharField(max_length=10, default='USD')
    status = models.CharField(max_length=20, choices=INCENTIVE_STATUS_CHOICES, default='pending')
    description = models.TextField(blank=True, null=True)

    # Campi addizionali di tracciamento e gestione dell'incentivo
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    device_info = models.CharField(max_length=255, blank=True, null=True)
    tracking_id = models.CharField(max_length=50, blank=True, null=True)
    expiration_date = models.DateTimeField(null=True, blank=True)
    is_incentive_active = models.BooleanField(default=True)
    
    def __str__(self):
        return f"Incentive {self.id} - {self.affiliate} for Program {self.program}"

    def apply_incentive(self):
        """
        Logica di esempio per calcolare e applicare l'incentivo, come per esempio
        approvare l'incentivo se l'azione è confermata, e aggiungere il valore all'account.
        """
        if self.status == 'pending':
            self.status = 'approved'
            self.affiliate.account_balance += self.amount
            self.affiliate.save()
            self.save()
    
    class Meta:
        ordering = ['-date']
        verbose_name = "Affiliate Incentive"
        verbose_name_plural = "Affiliate Incentives"
