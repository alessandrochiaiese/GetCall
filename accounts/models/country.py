from django.db import models

class Country(models.Model):
    name = models.CharField(max_length=256)

    class Meta:
        verbose_name = "Country"
        verbose_name_plural = "Countries" 