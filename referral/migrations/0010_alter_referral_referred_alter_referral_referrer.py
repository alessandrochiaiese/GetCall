# Generated by Django 5.1.3 on 2024-11-30 12:14

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('referral', '0009_auto_20241129_2221'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='referral',
            name='referred',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='referred_by', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='referral',
            name='referrer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='referrals', to=settings.AUTH_USER_MODEL),
        ),
    ]
