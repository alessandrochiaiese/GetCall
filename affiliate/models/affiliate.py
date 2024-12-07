# affiliate_system/models.py

from django.db import models
from django.contrib.auth import get_user_model
from django.utils.crypto import get_random_string

User = get_user_model()

class Affiliate(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='affiliate_user')
    name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=15, blank=True)
    date_joined = models.DateField()
    status = models.CharField(max_length=50)
    total_earnings = models.DecimalField(max_digits=10, decimal_places=2)
    country = models.CharField(max_length=50)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True)
    account_balance = models.DecimalField(max_digits=10, decimal_places=2)
    last_login = models.DateTimeField(null=True, blank=True)
    referral_source = models.CharField(max_length=255)

"""
class Affiliate(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    programs = models.ManyToManyField('AffiliateProgram', through='AffiliateProgramPartecipation', related_name="affiliates")
    name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=20, null=True, blank=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, choices=[("active", "Active"), ("suspended", "Suspended")])
    total_earnings = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    country = models.CharField(max_length=100)
    profile_picture = models.ImageField(upload_to='affiliate_profiles/', null=True, blank=True)
    account_balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    last_login = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.name} - {self.date_joined}"
    
class Affiliate(models.Model):
    user = models.OneToOneField('User', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=20, null=True, blank=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, choices=[("active", "Active"), ("suspended", "Suspended")])
    total_earnings = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    country = models.CharField(max_length=100)
    profile_picture = models.ImageField(upload_to='affiliate_profiles/', null=True, blank=True)
    account_balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    last_login = models.DateTimeField(null=True, blank=True)

class Affiliate(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="affiliate")
    code = models.CharField(max_length=10, unique=True, default=get_random_string)
    total_rewards = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return f"{self.user.username} - {self.code}"

    def generate_code(self):
        self.code = get_random_string(10)
        self.save()"""
