from django.urls import path 
from affiliate.api.views.views_affiliate_audit import AffiliateAuditAPIView
from affiliate.api.views.views_affiliate_commission import AffiliateCommissionAPIView
from affiliate.api.views.views_affiliate_campaign import AffiliateCampaignAPIView
from affiliate.api.views.views_affiliate_link import AffiliateLinkAPIView
from affiliate.api.views.views_affiliate_notification import AffiliateNotificationAPIView
from affiliate.api.views.views_affiliate_payout import AffiliatePayoutAPIView
from affiliate.api.views.views_affiliate_performance import AffiliatePerformanceAPIView
from affiliate.api.views.views_affiliate_program import AffiliateProgramAPIView
from affiliate.api.views.views_affiliate_program_partecipaation import AffiliateProgramPartecipationAPIView
from affiliate.api.views.views_affiliate_settings import AffiliateSettingsAPIView
from affiliate.api.views.views_affiliate_reward import AffiliateRewardAPIView
from affiliate.api.views.views_affiliate_support_ticket import AffiliateSupportTicketAPIView
from affiliate.api.views.views_affiliate_tier import AffiliateTierAPIView
from affiliate.api.views.views_affiliate_transaction import AffiliateTransactionAPIView

urlpatterns = [  
    path('audits/', AffiliateAuditAPIView.as_view(), name='affiliate_audits'),
    path('audits/<int:affiliate_audit_id>/', AffiliateAuditAPIView.as_view(), name='affiliate_audit'),

    path('commissions/', AffiliateCommissionAPIView.as_view(), name='affiliate_commissions'),
    path('commissions/<int:affiliate_commission_id>/', AffiliateCommissionAPIView.as_view(), name='affiliate_commission'),

    path('campaigns/', AffiliateCampaignAPIView.as_view(), name='affiliate_campaigns'),
    path('campaigns/<int:affiliate_campaign_id>/', AffiliateCampaignAPIView.as_view(), name='affiliate_campaign'),

    path('links/', AffiliateLinkAPIView.as_view(), name='affiliate_links'),
    path('links/<int:affiliate_link_id>/', AffiliateLinkAPIView.as_view(), name='affiliate_link'),

    path('notifications/', AffiliateNotificationAPIView.as_view(), name='affiliate_notifications'),
    path('notifications/<int:affiliate_notification_id>/', AffiliateNotificationAPIView.as_view(), name='affiliate_notification'),

    path('payouts/', AffiliatePayoutAPIView.as_view(), name='affiliate_payouts'),
    path('payouts/<int:affiliate_payout_id>/', AffiliatePayoutAPIView.as_view(), name='affiliate_payout'),

    path('performances/', AffiliatePerformanceAPIView.as_view(), name='affiliate_performances'),
    path('performances/<int:affiliate_performance_id>/', AffiliatePerformanceAPIView.as_view(), name='affiliate_performance'),
    
    path('programs/', AffiliateProgramAPIView.as_view(), name='affiliate_programs'),
    path('programs/<int:affiliate_program_id>/', AffiliateProgramAPIView.as_view(), name='affiliate_program'),
    
    path('programs/<int:affiliate_program_id>/partecipations/', AffiliateProgramPartecipationAPIView.as_view(), name='affiliate_program_partecipations'),
    path('programs/<int:affiliate_program_id>/partecipations/<int:affiliate_program_partecipation_id>', AffiliateProgramPartecipationAPIView.as_view(), name='affiliate_program_partecipation'),
    
    path('settings/', AffiliateSettingsAPIView.as_view(), name='affiliate_settings'),
    path('settings/<int:affiliate_setting_id>/', AffiliateSettingsAPIView.as_view(), name='affiliate_setting'),
    
    path('rewards/', AffiliateRewardAPIView.as_view(), name='affiliate_rewards'),
    path('rewards/<int:affiliate_reward_id>/', AffiliateRewardAPIView.as_view(), name='affiliate_reward'),
    
    path('support-tickets/', AffiliateSupportTicketAPIView.as_view(), name='affiliate_support-tickets'),
    path('support-tickets/<int:affiliate_support_ticket_id>/', AffiliateSupportTicketAPIView.as_view(), name='affiliate_support-ticket'),
    
    path('tiers/', AffiliateTierAPIView.as_view(), name='affiliate_tiers'),
    path('tiers/<int:affiliate_tier_id>/', AffiliateTierAPIView.as_view(), name='affiliate_tier'),
    
    path('transactions/', AffiliateTransactionAPIView.as_view(), name='affiliate_transactions'),
    path('transactions/<int:affiliate_transaction_id>/', AffiliateTransactionAPIView.as_view(), name='affiliate_transaction'),
    
]
