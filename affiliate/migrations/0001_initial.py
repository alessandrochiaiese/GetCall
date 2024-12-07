# Generated by Django 5.1.3 on 2024-11-24 14:22

import django.db.models.deletion
import django.utils.timezone
from decimal import Decimal
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounts', '__first__'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Affiliate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('email', models.EmailField(max_length=254)),
                ('phone', models.CharField(blank=True, max_length=15)),
                ('date_joined', models.DateField()),
                ('status', models.CharField(max_length=50)),
                ('total_earnings', models.DecimalField(decimal_places=2, max_digits=10)),
                ('country', models.CharField(max_length=50)),
                ('profile_picture', models.ImageField(blank=True, upload_to='profile_pics/')),
                ('account_balance', models.DecimalField(decimal_places=2, max_digits=10)),
                ('last_login', models.DateTimeField(blank=True, null=True)),
                ('referral_source', models.CharField(max_length=255)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='affiliate_user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='AffiliateAudit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('action_taken', models.TextField()),
                ('action_date', models.DateField()),
                ('ip_address', models.GenericIPAddressField()),
                ('device_info', models.TextField()),
                ('location', models.CharField(max_length=100)),
                ('affiliates', models.ManyToManyField(blank=True, related_name='affiliate_audit_affiliates', to='affiliate.affiliate')),
            ],
            options={
                'verbose_name': 'Affiliate Audit',
                'verbose_name_plural': 'Affiliate Audits',
                'ordering': ['-action_date'],
            },
        ),
        migrations.CreateModel(
            name='AffiliateNotification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.TextField()),
                ('date_sent', models.DateField()),
                ('is_read', models.BooleanField(default=False)),
                ('priority', models.CharField(max_length=50)),
                ('notification_type', models.CharField(max_length=50)),
                ('affiliates', models.ManyToManyField(related_name='affiliate_notification_affiliates', to='affiliate.affiliate')),
            ],
            options={
                'verbose_name': 'Affiliate Notification',
                'verbose_name_plural': 'Affiliate Notifications',
                'ordering': ['-date_sent'],
            },
        ),
        migrations.CreateModel(
            name='AffiliatePayout',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('currency', models.CharField(max_length=10)),
                ('payout_date', models.DateField()),
                ('payout_method', models.CharField(max_length=50)),
                ('payout_status', models.CharField(max_length=50)),
                ('transaction_id', models.CharField(max_length=255)),
                ('processing_fee', models.DecimalField(decimal_places=2, max_digits=5)),
                ('net_amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('payout_provider', models.CharField(max_length=50)),
                ('affiliates', models.ManyToManyField(related_name='affiliate_payout_affiliates', to='affiliate.affiliate')),
            ],
            options={
                'verbose_name': 'Affiliate Payout',
                'verbose_name_plural': 'Affiliate Payouts',
                'ordering': ['-payout_date'],
            },
        ),
        migrations.CreateModel(
            name='AffiliatePerformance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('period', models.CharField(max_length=50)),
                ('total_clicks', models.IntegerField()),
                ('total_conversions', models.IntegerField()),
                ('conversion_rate', models.DecimalField(decimal_places=2, max_digits=5)),
                ('total_earnings', models.DecimalField(decimal_places=2, max_digits=10)),
                ('average_order_value', models.DecimalField(decimal_places=2, max_digits=10)),
                ('refund_rate', models.DecimalField(decimal_places=2, max_digits=5)),
                ('customer_lifetime_value', models.DecimalField(decimal_places=2, max_digits=10)),
                ('top_product', models.CharField(max_length=255)),
                ('affiliates', models.ManyToManyField(related_name='affiliate_performance_affiliates', to='affiliate.affiliate')),
            ],
            options={
                'verbose_name': 'Affiliate Perfomance',
                'verbose_name_plural': 'Affiliate Perfomances',
            },
        ),
        migrations.CreateModel(
            name='AffiliateProgram',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('commission_rate', models.DecimalField(decimal_places=2, max_digits=5)),
                ('currency', models.CharField(max_length=10)),
                ('min_payout_threshold', models.DecimalField(decimal_places=2, max_digits=10)),
                ('max_payout_limit', models.DecimalField(decimal_places=2, max_digits=10)),
                ('date_created', models.DateField()),
                ('is_active', models.BooleanField(default=True)),
                ('duration', models.IntegerField()),
                ('target_industry', models.CharField(max_length=100)),
                ('allowed_countries', models.ManyToManyField(related_name='affiliate_program_countries', to='accounts.country')),
            ],
            options={
                'verbose_name': 'Affiliate Program',
                'verbose_name_plural': 'Affiliate Programs',
                'ordering': ['-date_created'],
            },
        ),
        migrations.CreateModel(
            name='AffiliateLink',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.URLField()),
                ('click_count', models.IntegerField(default=0)),
                ('conversion_count', models.IntegerField(default=0)),
                ('date_created', models.DateField()),
                ('last_used', models.DateTimeField(blank=True, null=True)),
                ('link_status', models.CharField(max_length=50)),
                ('landing_page', models.URLField(blank=True)),
                ('custom_tracking_id', models.CharField(blank=True, max_length=255)),
                ('affiliates', models.ManyToManyField(related_name='affiliate_link_affiliates', to='affiliate.affiliate')),
                ('programs', models.ManyToManyField(related_name='affiliate_link_programs', to='affiliate.affiliateprogram')),
            ],
            options={
                'verbose_name': 'Affiliate Link',
                'verbose_name_plural': 'Affiliate Links',
                'ordering': ['-date_created'],
            },
        ),
        migrations.CreateModel(
            name='AffiliateIncentive',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('incentive_type', models.CharField(choices=[('click', 'Click'), ('signup', 'Signup'), ('purchase', 'Purchase')], max_length=20)),
                ('date', models.DateTimeField(default=django.utils.timezone.now)),
                ('amount', models.DecimalField(decimal_places=2, default=Decimal('0.00'), max_digits=10)),
                ('currency', models.CharField(default='USD', max_length=10)),
                ('status', models.CharField(choices=[('pending', 'Pending'), ('approved', 'Approved'), ('declined', 'Declined'), ('expired', 'Expired')], default='pending', max_length=20)),
                ('description', models.TextField(blank=True, null=True)),
                ('ip_address', models.GenericIPAddressField(blank=True, null=True)),
                ('device_info', models.CharField(blank=True, max_length=255, null=True)),
                ('tracking_id', models.CharField(blank=True, max_length=50, null=True)),
                ('expiration_date', models.DateTimeField(blank=True, null=True)),
                ('is_incentive_active', models.BooleanField(default=True)),
                ('affiliate', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='affiliate_incentive_affiliate', to='affiliate.affiliate')),
                ('program', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='affiliate_incentive_program', to='affiliate.affiliateprogram')),
            ],
            options={
                'verbose_name': 'Affiliate Incentive',
                'verbose_name_plural': 'Affiliate Incentives',
                'ordering': ['-date'],
            },
        ),
        migrations.CreateModel(
            name='AffiliateCommission',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('currency', models.CharField(max_length=10)),
                ('date_awarded', models.DateField()),
                ('status', models.CharField(max_length=50)),
                ('approved_by', models.CharField(max_length=255)),
                ('commission_type', models.CharField(max_length=50)),
                ('description', models.TextField(blank=True)),
                ('tier', models.CharField(max_length=50)),
                ('affiliates', models.ManyToManyField(related_name='affiliate_commission_affiliates', to='affiliate.affiliate')),
                ('programs', models.ManyToManyField(related_name='affiliate_commission_programs', to='affiliate.affiliateprogram')),
            ],
            options={
                'verbose_name': 'Affiliate Commission',
                'verbose_name_plural': 'Affiliate Commissions',
                'ordering': ['-date_awarded'],
            },
        ),
        migrations.CreateModel(
            name='AffiliateCampaign',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('campaign_name', models.CharField(max_length=255)),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('goal', models.TextField()),
                ('budget', models.DecimalField(decimal_places=2, max_digits=10)),
                ('spending_to_date', models.DecimalField(decimal_places=2, max_digits=10)),
                ('programs', models.ManyToManyField(related_name='affiliate_campaign_programs', to='affiliate.affiliateprogram')),
            ],
            options={
                'verbose_name': 'Affiliate Campaign',
                'verbose_name_plural': 'Affiliate Campaigns',
                'ordering': ['-start_date'],
            },
        ),
        migrations.CreateModel(
            name='AffiliateProgramPartecipation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_joined', models.DateTimeField(auto_now_add=True)),
                ('commission_earned', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('status', models.CharField(choices=[('active', 'Active'), ('inactive', 'Inactive')], max_length=50)),
                ('affiliate', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='affiliate_program_partecipation_affiliate', to='affiliate.affiliate')),
                ('program', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='affiliate_program_partecipation_program', to='affiliate.affiliateprogram')),
            ],
            options={
                'verbose_name': 'Affiliate Program Partecipation',
                'verbose_name_plural': 'Affiliate Program Partecipations',
                'ordering': ['-date_joined'],
            },
        ),
        migrations.CreateModel(
            name='AffiliateReward',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('affiliate', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='affiliate_reward_affiliates', to='affiliate.affiliate')),
            ],
            options={
                'verbose_name': 'Affiliate Reward',
                'verbose_name_plural': 'Affiliate Rewards',
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='AffiliateSettings',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('preferred_currency', models.CharField(max_length=10)),
                ('preferred_payment_method', models.CharField(max_length=50)),
                ('payout_schedule', models.CharField(max_length=50)),
                ('notification_preference', models.CharField(max_length=50)),
                ('dashboard_layout', models.CharField(max_length=50)),
                ('affiliates', models.ManyToManyField(related_name='affiiate_setting_affiliates', to='affiliate.affiliate')),
            ],
            options={
                'verbose_name': 'Affiliate Setting',
                'verbose_name_plural': 'Affiliate Settings',
            },
        ),
        migrations.CreateModel(
            name='AffiliateSupportTicket',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ticket_number', models.CharField(max_length=100)),
                ('subject', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('status', models.CharField(max_length=50)),
                ('date_created', models.DateField()),
                ('date_closed', models.DateField(blank=True, null=True)),
                ('priority', models.CharField(max_length=50)),
                ('assigned_agent', models.CharField(max_length=255)),
                ('affiliates', models.ManyToManyField(related_name='affiliate_supportticket_affiliates', to='affiliate.affiliate')),
            ],
            options={
                'verbose_name': 'Affiliate Support Ticket',
                'verbose_name_plural': 'Affiliate Support Tickets',
            },
        ),
        migrations.CreateModel(
            name='AffiliateTier',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tier_name', models.CharField(max_length=50)),
                ('min_sales', models.IntegerField()),
                ('commission_rate', models.DecimalField(decimal_places=2, max_digits=5)),
                ('tier_benefits', models.TextField(blank=True)),
                ('access_level', models.IntegerField()),
                ('next_tier_threshold', models.IntegerField()),
                ('tier_expiration', models.DateField(blank=True, null=True)),
                ('programs', models.ManyToManyField(related_name='affiliate_tier_programs', to='affiliate.affiliateprogram')),
            ],
            options={
                'verbose_name': 'Affiliate Tier',
                'verbose_name_plural': 'Affiliate Tiers',
            },
        ),
        migrations.CreateModel(
            name='AffiliateTransaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('transaction_amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('transaction_date', models.DateField()),
                ('order_id', models.CharField(max_length=255)),
                ('product_id', models.CharField(max_length=255)),
                ('status', models.CharField(max_length=50)),
                ('payment_date', models.DateField(blank=True, null=True)),
                ('commission_rate', models.DecimalField(decimal_places=2, max_digits=5)),
                ('discount_applied', models.DecimalField(decimal_places=2, default=0.0, max_digits=5)),
                ('coupon_code', models.CharField(blank=True, max_length=255)),
                ('affiliates', models.ManyToManyField(related_name='affiliate_transaction_affiliates', to='affiliate.affiliate')),
                ('commissions', models.ManyToManyField(related_name='affiliate_transaction_commissions', to='affiliate.affiliatecommission')),
            ],
            options={
                'verbose_name': 'Affiliate Transaction',
                'verbose_name_plural': 'Affiliate Transactions',
            },
        ),
    ]
