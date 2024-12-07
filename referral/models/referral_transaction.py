from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class ReferralTransaction(models.Model):
    referral_codes = models.ManyToManyField('ReferralCode', related_name='referra_transaction_referral_codes')
    referred_user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True, related_name='referra_transaction_user')
    transaction_date = models.DateField()
    order_id = models.CharField(max_length=255)
    transaction_amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=10)
    status = models.CharField(max_length=50)
    conversion_value = models.DecimalField(max_digits=10, decimal_places=2)
    discount_value = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    coupon_code_used = models.CharField(max_length=100, blank=True)
    channel = models.CharField(max_length=50, blank=True)

    class Meta:
        ordering = ['-transaction_date']
        verbose_name = "Referral Transaction"
        verbose_name_plural = "Referral Transactions"

"""
class ReferralTransaction(models.Model):
    program = models.OneToOneField('ReferralProgram', on_delete=models.CASCADE)
    referred_users = models.ManyToManyField('User', related_name="referral_transactions")
    transaction_date = models.DateTimeField(auto_now_add=True)
    order_id = models.CharField(max_length=255)
    transaction_amount = models.DecimalField(max_digits=10, decimal_places=2)
    discount_value = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    channel = models.CharField(max_length=50, null=True, blank=True)

class ReferralTransaction(models.Model):
    referral_code = models.OneToOneField('ReferralCode', on_delete=models.CASCADE)
    referred_user = models.OneToOneField('User', on_delete=models.CASCADE, related_name="referred_user")
    transaction_date = models.DateTimeField(auto_now_add=True)
    order_id = models.CharField(max_length=255)
    transaction_amount = models.DecimalField(max_digits=10, decimal_places=2)
"""