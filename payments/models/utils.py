
from django.conf import settings
from django.db import models
from django.template.defaultfilters import slugify

User = settings.AUTH_USER_MODEL

def get_image_filename(instance, filename):
    name = instance.name
    slug = slugify(name)
    return f"products/{slug}-{filename}"
