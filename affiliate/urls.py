
from django.conf.urls.static import static
from django.urls import include, path, re_path as url

from affiliate.views.views_affiliate_audit import create_affiliate_audit, delete_affiliate_audit, update_affiliate_audit
from affiliate.views.views_home import index_view
from getcall import settings 
#from  affiliate.views.views_affiliate import * 
from  affiliate.views.views_affiliate_audit import * 
from  affiliate.views.views_affiliate_campaign import * 
from  affiliate.views.views_affiliate_commission import * 
from  affiliate.views.views_affiliate_incentive import * 
from  affiliate.views.views_affiliate_link import * 
from  affiliate.views.views_affiliate_notification import * 
from  affiliate.views.views_affiliate_payout import * 
from  affiliate.views.views_affiliate_performance import * 
from  affiliate.views.views_affiliate_program import * 
from  affiliate.views.views_affiliate_program_partecipation import * 
from  affiliate.views.views_affiliate_reward import * 
from  affiliate.views.views_affiliate_setting import * 
from  affiliate.views.views_affiliate_support_ticket import * 
from  affiliate.views.views_affiliate_tier import * 
from  affiliate.views.views_affiliate_transaction import * 
urlpatterns = [   
    path('affiliate/audits/', affiliate_audit_list, name='affiliate_audit_list'),
    path('affiliate/audits/<int:affiliate_audit_id>/', affiliate_audit_detail, name='affiliate_audit_detail'),
    path('affiliate/audits/create/', create_affiliate_audit, name='affiliate_create_audit'),
    path('affiliate/audits/update/<str:affiliate_audit_id>/', update_affiliate_audit, name='affiliate_update_audit'),
    path('affiliate/audits/delete/<str:affiliate_audit_id>/', delete_affiliate_audit, name='affiliate_delete_audit'),

    path('affiliate/campaigns/', affiliate_campaign_list, name='affiliate_campaign_list'),
    path('affiliate/campaigns/<int:affiliate_campaign_id>/', affiliate_campaign_detail, name='affiliate_campaign_detail'),
    path('affiliate/campaigns/create/', create_affiliate_campaign, name='affiliate_create_campaign'),
    path('affiliate/campaigns/update/<str:affiliate_campaign_id>/', update_affiliate_campaign, name='affiliate_update_campaign'),
    path('affiliate/campaigns/delete/<str:affiliate_campaign_id>/', delete_affiliate_campaign, name='affiliate_delete_campaign'),
    
    path('affiliate/commissions/', affiliate_commission_list, name='affiliate_commission_list'),
    path('affiliate/commissions/<int:affiliate_commission_id>/', affiliate_commission_detail, name='affiliate_commission_detail'),
    path('affiliate/commissions/create/', create_affiliate_commission, name='affiliate_create_commission'),
    path('affiliate/commissions/update/<str:affiliate_commission_id>/', update_affiliate_commission, name='affiliate_update_commission'),
    path('affiliate/commissions/delete/<str:affiliate_commission_id>/', delete_affiliate_commission, name='affiliate_delete_commission'),
    
    path('affiliate/incentives/', affiliate_incentive_list, name='affiliate_incentive_list'),
    path('affiliate/incentives/<int:affiliate_incentive_id>/', affiliate_incentive_detail, name='affiliate_incentive_detail'),
    path('affiliate/incentives/create/', create_affiliate_incentive, name='affiliate_create_incentive'),
    path('affiliate/incentives/update/<str:affiliate_incentive_id>/', update_affiliate_incentive, name='affiliate_update_incentive'),
    path('affiliate/incentives/delete/<str:affiliate_incentive_id>/', delete_affiliate_incentive, name='affiliate_delete_incentive'),
    
    path('affiliate/links/', affiliate_link_list, name='affiliate_link_list'),
    path('affiliate/links/<int:affiliate_link_id>/', affiliate_link_detail, name='affiliate_link_detail'),
    path('affiliate/links/create/', create_affiliate_link, name='affiliate_create_link'),
    path('affiliate/links/update/<str:affiliate_link_id>/', update_affiliate_link, name='affiliate_update_link'),
    path('affiliate/links/delete/<str:affiliate_link_id>/', delete_affiliate_link, name='affiliate_delete_link'),
    
    path('affiliate/notifications/', affiliate_notification_list, name='affiliate_notification_list'),
    path('affiliate/notifications/<int:affiliate_notification_id>/', affiliate_notification_detail, name='affiliate_notification_detail'),
    path('affiliate/notifications/create/', create_affiliate_notification, name='affiliate_create_notification'),
    path('affiliate/notifications/update/<str:affiliate_notification_id>/', update_affiliate_notification, name='affiliate_update_notification'),
    path('affiliate/notifications/delete/<str:affiliate_notification_id>/', delete_affiliate_notification, name='affiliate_delete_notification'),
    
    path('affiliate/payouts/', affiliate_payout_list, name='affiliate_payout_list'),
    path('affiliate/payouts/<int:affiliate_payout_id>/', affiliate_payout_detail, name='affiliate_payout_detail'),
    path('affiliate/payouts/create/', create_affiliate_payout, name='affiliate_create_payout'),
    path('affiliate/payouts/update/<str:affiliate_payout_id>/', update_affiliate_payout, name='affiliate_update_payout'),
    path('affiliate/payouts/delete/<str:affiliate_payout_id>/', delete_affiliate_payout, name='affiliate_delete_payout'),
    
    path('affiliate/performances/', affiliate_performance_list, name='affiliate_performance_list'),
    path('affiliate/performances/<int:affiliate_performance_id>/', affiliate_performance_detail, name='affiliate_performance_detail'),
    path('affiliate/performances/create/', create_affiliate_performance, name='affiliate_create_performance'),
    path('affiliate/performances/update/<str:affiliate_performance_id>/', update_affiliate_performance, name='affiliate_update_performance'),
    path('affiliate/performances/delete/<str:affiliate_performance_id>/', delete_affiliate_performance, name='affiliate_delete_performance'),

    path('affiliate/programs/', affiliate_program_list, name='affiliate_program_list'),
    path('affiliate/programs/<int:affiliate_program_id>/', affiliate_program_detail, name='affiliate_program_detail'),
    path('affiliate/programs/create/', create_affiliate_program, name='affiliate_create_program'),
    path('affiliate/programs/update/<str:affiliate_program_id>/', update_affiliate_program, name='affiliate_update_program'),
    path('affiliate/programs/delete/<str:affiliate_program_id>/', delete_affiliate_program, name='affiliate_delete_program'),
    
    path('affiliate/programs/<int:affiliate_program_id>/partecipations/', affiliate_program_partecipation_list, name='affiliate_program_partecipation_list'),
    path('affiliate/programs/<int:affiliate_program_id>/partecipations/<int:affiliate_program_partecipation_id>/', affiliate_program_partecipation_detail, name='affiliate_program_partecipation_detail'),
    path('affiliate/programs/create/', create_affiliate_program, name='affiliate_create_program'),
    path('affiliate/programs/update/<str:affiliate_program_partecipation_id>/', update_affiliate_program, name='affiliate_update_program'),
    path('affiliate/programs/delete/<str:affiliate_program_partecipation_id>/', delete_affiliate_program, name='affiliate_delete_program'),
    
    path('affiliate/rewards/', affiliate_reward_list, name='affiliate_reward_list'),
    path('affiliate/rewards/<int:affiliate_reward_id>/', affiliate_reward_detail, name='affiliate_reward_detail'),
    path('affiliate/rewards/create/', create_affiliate_reward, name='affiliate_create_reward'),
    path('affiliate/rewards/update/<str:affiliate_reward_id>/', update_affiliate_reward, name='affiliate_update_reward'),
    path('affiliate/rewards/delete/<str:affiliate_reward_id>/', delete_affiliate_reward, name='affiliate_delete_reward'),
    
    path('affiliate/settings/', affiliate_setting_list, name='affiliate_setting_list'),
    path('affiliate/settings/<int:affiliate_setting_id>/', affiliate_setting_detail, name='affiliate_setting_detail'),
    path('affiliate/settings/create/', create_affiliate_setting, name='affiliate_create_setting'),
    path('affiliate/settings/update/<str:affiliate_setting_id>/', update_affiliate_setting, name='affiliate_update_setting'),
    path('affiliate/settings/delete/<str:affiliate_setting_id>/', delete_affiliate_setting, name='affiliate_delete_setting'),
    
    path('affiliate/support-tickets/', affiliate_support_ticket_list, name='affiliate_support_ticket_list'),
    path('affiliate/support-tickets/<int:affiliate_support_ticket_id>/', affiliate_support_ticket_detail, name='affiliate_support_ticket_detail'),
    path('affiliate/support-tickets/create/', create_affiliate_support_ticket, name='affiliate_create_support_ticket'),
    path('affiliate/support-tickets/update/<str:affiliate_support_ticket_id>/', update_affiliate_support_ticket, name='affiliate_update_support_ticket'),
    path('affiliate/support-tickets/delete/<str:affiliate_support_ticket_id>/', delete_affiliate_support_ticket, name='affiliate_delete_support_ticket'),
    
    path('affiliate/tiers/', affiliate_tier_list, name='affiliate_tier_list'),
    path('affiliate/tiers/<int:affiliate_tier_id>/', affiliate_tier_detail, name='affiliate_tier_detail'),
    path('affiliate/tiers/create/', create_affiliate_tier, name='affiliate_create_tier'),
    path('affiliate/tiers/update/<str:affiliate_tier_id>/', update_affiliate_tier, name='affiliate_update_tier'),
    path('affiliate/tiers/delete/<str:affiliate_tier_id>/', delete_affiliate_tier, name='affiliate_delete_tier'),
    
    path('affiliate/transactions/', affiliate_transaction_list, name='affiliate_transaction_list'),
    path('affiliate/transactions/<int:affiliate_transaction_id>/', affiliate_transaction_detail, name='affiliate_transaction_detail'),
    path('affiliate/transactions/create/', create_affiliate_transaction, name='affiliate_create_transaction'),
    path('affiliate/transactions/update/<str:affiliate_transaction_id>/', update_affiliate_transaction, name='affiliate_update_transaction'),
    path('affiliate/transactions/delete/<str:affiliate_transaction_id>/', delete_affiliate_transaction, name='affiliate_delete_transaction'),






    path('api/v0/affiliate/', include('affiliate.api.urls'), name='api_affiliate_v0'),
]  + static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)
