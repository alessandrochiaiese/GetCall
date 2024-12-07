
from django.db import models

class Role(models.Model): 
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=256)

    # If you need to initialize with arguments, you can pass them to the parent class
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
 
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
        }

    class Meta:
        db_table = 'Roles'