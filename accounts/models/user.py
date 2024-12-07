from django.db import models

from django.contrib.auth import get_user_model

DjangoUser = get_user_model()

class User(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.OneToOneField(DjangoUser, on_delete=models.CASCADE, related_name="django_user")
    email = models.CharField(max_length=256)
    phone = models.CharField(max_length=256)
    first_name = models.CharField(max_length=256)
    last_name = models.CharField(max_length=256)
    password = models.CharField(max_length=256)
    roles = models.ManyToManyField('Role', related_name='roles')
    date_created = models.DateField(auto_now=True)
    date_modified = models.DateField(auto_now=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def to_dict(self):
        return {
            'id': self.id,
            'email': self.email,
            'phone': self.phone,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'password': self.password,
            'roles': self.roles,
            'date_created': self.date_created,
            'date_modified': self.date_modified
        }

    class Meta:
        db_table = 'Users'