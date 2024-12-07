from django.db import models

class Region(models.Model):
    country = models.OneToOneField('Country', on_delete=models.CASCADE, related_name='country')
    name = models.CharField(max_length=256)

    class Meta:
        verbose_name = "Region"
        verbose_name_plural = "Regions" 