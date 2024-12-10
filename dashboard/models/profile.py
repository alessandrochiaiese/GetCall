from django.db import models
from django.contrib.auth.models import User
from PIL import Image

from affiliate.models.affiliate_transaction import AffiliateTransaction


# Extending User Model Using a One-To-One Link
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    avatar = models.ImageField(default='default.jpg', upload_to='profile_images')
    bio = models.TextField()
    is_business = models.BooleanField(default=False)
    is_buyer = models.BooleanField(default=False)
    
    # business
    name_business = models# nome azienda
    user_ower = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE, related_name="owner_business")
    iva = models.CharField(max_length=32, default="0000")
    
    # buyer
    transactions = models.ManyToManyField(AffiliateTransaction, related_name='txns')


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
