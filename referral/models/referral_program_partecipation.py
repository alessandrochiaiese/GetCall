from django.db import models

class ReferralProgramPartecipation(models.Model):
    referral_codes = models.OneToOneField('ReferralCode', on_delete=models.CASCADE, related_name='engagement_program_partecipation_referral_codes')
    programs = models.OneToOneField('ReferralProgram', on_delete=models.CASCADE, related_name='engagement_program_partecipation_programs')
    date_joined = models.DateTimeField(auto_now_add=True)
    reward_earned = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    status = models.CharField(max_length=50, choices=[("active", "Active"), ("inactive", "Inactive")])

    class Meta:
        ordering = ['-date_joined']
        verbose_name = "Referral Program Partecipation"
        verbose_name_plural = "Referral Program Partecipations"
