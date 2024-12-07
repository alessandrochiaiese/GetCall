# referral_system/models.py

import email
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

"""
class ReferralRelation(models.Model):
    referrer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="referrals_made")
    referred = models.ForeignKey(User, on_delete=models.CASCADE, related_name="referrals_received")
    referral_level = models.IntegerField(default=1)  # Imposta il livello di separazione
    referral_program = models.ForeignKey('ReferralProgram', on_delete=models.CASCADE, related_name="referral_relations", null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('referrer', 'referred')  # Un referral è unico per ogni coppia referrer-referred

"""
class Referral(models.Model):
    program = models.OneToOneField('ReferralProgram', on_delete=models.CASCADE, related_name="referrals", null=True, blank=True)
    referrer = models.OneToOneField(User, on_delete=models.CASCADE, related_name="referrals_made")
    referred = models.ManyToManyField(User, related_name="referrals_received") 
    #referrer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="referrals")
    #referred = models.ForeignKey(User, on_delete=models.CASCADE, related_name="referred_by")  # non nullable
    reward_given = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        #if self.referred != None:
        #    return f"{self.referrer.username} referred {self.referred.username}"

        return f"{self.referrer.username} have not yet invited anyone"
    
    class Meta: 
        verbose_name = "Referral"
        verbose_name_plural = "Referrals"

"""
class ReferralRelationship(models.Model):
    # who invite 
    referrer = models.ForeignKey(
        AUTH_USER_MODEL,
        related_name='inviter',
        verbose_name="inviter",
        on_delete=models.CASCADE,
    )
    # who connected 
    referred = models.ForeignKey(
        AUTH_USER_MODEL,
        related_name='invited',
        verbose_name="invited",
        on_delete=models.CASCADE,
    )
    # referral code
    refer_token = models.ForeignKey(
        "ReferralCode",
        verbose_name="referral_code",
        on_delete=models.CASCADE,
    )
    def __str__(self) -> str:
        return f"{self.referrer}_{self.referred}"
"""