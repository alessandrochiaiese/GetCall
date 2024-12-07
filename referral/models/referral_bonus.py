from django.db import models


class ReferralBonus(models.Model):
    programs = models.ManyToManyField('ReferralProgram', related_name='referral_bonus_programs')
    bonus_type = models.CharField(max_length=50)
    bonus_value = models.DecimalField(max_digits=10, decimal_places=2)
    min_referrals_required = models.IntegerField(default=0)
    bonus_date = models.DateField()
    expiry_date = models.DateField(null=True, blank=True)
    max_usage = models.IntegerField(default=1)
    eligibility_criteria = models.TextField(blank=True)

    class Meta:
        ordering = ['-expiry_date']
        verbose_name = "Referral Bonus"
        verbose_name_plural = "Referral Bonus"


"""class ReferralBonus(models.Model):
    program_id = models.IntegerField()  # Reference to a program
    bonus_type = models.CharField(max_length=255)  # E.g., percentage, flat amount
    bonus_value = models.DecimalField(max_digits=10, decimal_places=2)
    min_referrals_required = models.IntegerField()
    bonus_date = models.DateTimeField()
    expiry_date = models.DateTimeField()
    max_usage = models.IntegerField()
    eligibility_criteria = models.TextField()

    def __str__(self):
        return f"Bonus for Program {self.program_id}"
"""