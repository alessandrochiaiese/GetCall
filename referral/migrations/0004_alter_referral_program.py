# Generated by Django 5.1.3 on 2024-11-27 19:17

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('referral', '0003_alter_referral_program_alter_referral_referred_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='referral',
            name='program',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='referrals', to='referral.referralprogram'),
        ),
    ]