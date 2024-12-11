from django.db import models
from django.contrib.auth.models import User
from PIL import Image

from affiliate.models.affiliate_transaction import AffiliateTransaction
import payments
from payments.models.payment_method import PaymentMethod

#User(username, first_name, last_name, email, is_staff, is_active, date_joined)

# Extending User Model Using a One-To-One Link
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE) 
    avatar = models.ImageField(default='default.jpg', upload_to='profile_images')
    bio = models.TextField(max_length=1024, null=True, blank=True)

    # base data profile
    birth_date = models.DateTimeField(null=True, blank=True)
    city = models.CharField(max_length=64, null=True, blank=True)
    street = models.CharField(max_length=64, null=True, blank=True)
    CAP = models.CharField(max_length=64, null=True, blank=True)
    phone_number = models.CharField(max_length=13, unique=True)


    # Differenet kind of profile (Business, Buyer, Base)
    is_business = models.BooleanField(default=False)
    is_buyer = models.BooleanField(default=False)
    
    # business
    name_business = models.CharField(max_length=64, default="getref", unique=True) # nome azienda
    is_owner = models.BooleanField(default=False)
    user_ower = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE, related_name="owner_business")
    iva = models.CharField(max_length=32, default="0000")
    office_number = models.CharField(max_length=13, unique=True) 
    
    
    # buyer
    transactions = models.ManyToManyField(AffiliateTransaction, related_name='txns')
    payment_method = models.OneToOneField(PaymentMethod, on_delete=models.CASCADE, related_name='payment')


    def __str__(self):
        return self.user.username

    # resizing images
    def save(self, *args, **kwargs):
        super().save()

        img = Image.open(self.avatar.path)

        if img.height > 100 or img.width > 100:
            new_img = (100, 100)
            img.thumbnail(new_img)
            img.save(self.avatar.path)
