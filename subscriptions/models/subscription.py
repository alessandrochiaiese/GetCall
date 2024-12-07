from django.db import models
from django.utils.timezone import now

from accounts.models.user import User


class Subscription(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    plan = models.ForeignKey('Plan', on_delete=models.SET_NULL, null=True)
    tokens_available = models.PositiveIntegerField(default=0)
    expires_at = models.DateTimeField()

    def is_active(self):
        return self.expires_at > now()

    def renew(self):
        """Rinnova l'abbonamento aggiungendo la durata del piano."""
        if self.plan:
            self.expires_at = now() + self.plan.get_duration_timedelta()
            self.tokens_available += self.plan.tokens_included
            self.save()
