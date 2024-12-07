
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class ReferralLevel(models.Model): 
    referrer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="referrals")
    referred = models.ForeignKey(User, on_delete=models.CASCADE, related_name="referred_by")  
    level = models.PositiveIntegerField(default=1)

