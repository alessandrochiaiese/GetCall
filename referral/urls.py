
from django.conf.urls.static import static
from django.urls import include, path, re_path as url
 
from getref import settings 
#from referral.views.views_referral import *
from referral.views.views_referral_audit import *
from referral.views.views_referral_campaign import *
from referral.views.views_referral_conversion import *
from referral.views.views_referral_bonus import *
from referral.views.views_referral_code import *
from referral.views.views_referral_notification import *
from referral.views.views_referral_engagement import *
from referral.views.views_referral_program import *
from referral.views.views_referral_program_partecipation import *
from referral.views.views_referral_reward import *
from referral.views.views_referral_setting import *
from referral.views.views_referral_stat import *
from referral.views.views_referral_transaction import *
urlpatterns = [        
    path('referral/audits/', referral_audit_list, name='referral_audit_list'),
    path('referral/audits/<int:referral_audit_id>/', referral_audit_detail, name='referral_audit_detail'),
    path('referral/audits/create/', create_referral_audit, name='referral_create_audit'),
    path('referral/audits/update/<str:referral_audit_id>/', update_referral_audit, name='referral_update_audit'),
    path('referral/audits/delete/<str:referral_audit_id>/', delete_referral_audit, name='referral_delete_audit'),

    path('referral/bonus/', referral_bonus_list, name='referral_bonus_list'),
    path('referral/bonus/<int:referral_bonus_id>/', referral_bonus_detail, name='referral_bonus_detail'),
    path('referral/bonus/create/', create_referral_bonus, name='referral_create_bonus'),
    path('referral/bonus/update/<str:referral_bonus_id>/', update_referral_bonus, name='referral_update_bonus'),
    path('referral/bonus/delete/<str:referral_bonus_id>/', delete_referral_bonus, name='referral_delete_bonus'),

    path('referral/campaigns/', referral_campaign_list, name='referral_campaign_list'),
    path('referral/campaigns/<int:referral_campaign_id>/', referral_campaign_detail, name='referral_campaign_detail'),
    path('referral/campaigns/create/', create_referral_campaign, name='referral_create_campaign'),
    path('referral/campaigns/update/<str:referral_campaign_id>/', update_referral_campaign, name='referral_update_campaign'),
    path('referral/campaigns/delete/<str:referral_campaign_id>/', delete_referral_campaign, name='referral_delete_campaign'),
    
    path('referral/codes/', referral_code_list, name='referral_code_list'),
    path('referral/codes/<int:referral_code_id>/', referral_code_detail, name='referral_code_detail'),
    path('referral/codes/create/', create_referral_code, name='referral_create_code'),
    path('referral/codes/update/<str:referral_code_id>/', update_referral_code, name='referral_update_code'),
    path('referral/codes/delete/<str:referral_code_id>/', delete_referral_code, name='referral_delete_code'),
    
    path('referral/conversions/', referral_conversion_list, name='referral_conversion_list'),
    path('referral/conversions/<int:referral_conversion_id>/', referral_conversion_detail, name='referral_conversion_detail'),
    path('referral/conversions/create/', create_referral_conversion, name='referral_create_conversion'),
    path('referral/conversions/update/<str:referral_conversion_id>/', update_referral_conversion, name='referral_update_conversion'),
    path('referral/conversions/delete/<str:referral_conversion_id>/', delete_referral_conversion, name='referral_delete_conversion'),
    
    path('referral/engagements/', referral_engagement_list, name='referral_engagement_list'),
    path('referral/engagements/<int:referral_engagement_id>/', referral_engagement_detail, name='referral_engagement_detail'),
    path('referral/engagements/create/', create_referral_engagement, name='referral_create_engagement'),
    path('referral/engagements/update/<str:referral_engagement_id>/', update_referral_engagement, name='referral_update_engagement'),
    path('referral/engagements/delete/<str:referral_engagement_id>/', delete_referral_engagement, name='referral_delete_engagement'),
    
    path('referral/notifications/', referral_notification_list, name='referral_notification_list'),
    path('referral/notifications/<int:referral_notification_id>/', referral_notification_detail, name='referral_notification_detail'),
    path('referral/notifications/create/', create_referral_notification, name='referral_create_notification'),
    path('referral/notifications/update/<str:referral_notification_id>/', update_referral_notification, name='referral_update_notification'),
    path('referral/notifications/delete/<str:referral_notification_id>/', delete_referral_notification, name='referral_delete_notification'),
     
    path('referral/programs/', referral_program_list, name='referral_program_list'),
    path('referral/programs/<int:referral_program_id>/', referral_program_detail, name='referral_program_detail'),
    path('referral/programs/create/', create_referral_program, name='referral_create_program'),
    path('referral/programs/update/<str:referral_program_id>/', update_referral_program, name='referral_update_program'),
    path('referral/programs/delete/<str:referral_program_id>/', delete_referral_program, name='referral_delete_program'),
     
    path('referral/programs/<int:referral_program_id>/partecipations/', referral_program_partecipation_list, name='referral_program_partecipation_list'),
    path('referral/programs/<int:referral_program_id>/partecipations/<int:referral_program_partecipation_id>/', referral_program_partecipation_detail, name='referral_program_partecipation_detail'),
    path('referral/programs/create/', create_referral_program, name='referral_create_program'),
    path('referral/programs/update/<str:referral_program_partecipation_id>/', update_referral_program, name='referral_update_program'),
    path('referral/programs/delete/<str:referral_program_partecipation_id>/', delete_referral_program, name='referral_delete_program'),
     
    path('referral/rewards/', referral_reward_list, name='referral_reward_list'),
    path('referral/rewards/<int:referral_reward_id>/', referral_reward_detail, name='referral_reward_detail'),
    path('referral/rewards/create/', create_referral_reward, name='referral_create_reward'),
    path('referral/rewards/update/<str:referral_reward_id>/', update_referral_reward, name='referral_update_reward'),
    path('referral/rewards/delete/<str:referral_reward_id>/', delete_referral_reward, name='referral_delete_reward'),
     
    path('referral/settings/', referral_setting_list, name='referral_setting_list'),
    path('referral/settings/<int:referral_setting_id>/', referral_setting_detail, name='referral_setting_detail'),
    path('referral/settings/create/', create_referral_setting, name='referral_create_setting'),
    path('referral/settings/update/<str:referral_setting_id>/', update_referral_setting, name='referral_update_setting'),
    path('referral/settings/delete/<str:referral_setting_id>/', delete_referral_setting, name='referral_delete_setting'),
     
    path('referral/stats/', referral_stat_list, name='referral_stat_list'),
    path('referral/stats/<int:referral_stat_id>/', referral_stat_detail, name='referral_stat_detail'),
    path('referral/stats/create/', create_referral_stat, name='referral_create_stat'),
    path('referral/stats/update/<str:referral_stat_id>/', update_referral_stat, name='referral_update_stat'),
    path('referral/stats/delete/<str:referral_stat_id>/', delete_referral_stat, name='referral_delete_stat'),
     
    path('referral/transactions/', referral_transaction_list, name='referral_transaction_list'),
    path('referral/transactions/<int:referral_transaction_id>/', referral_transaction_detail, name='referral_transaction_detail'),
    path('referral/transactions/create/', create_referral_transaction, name='referral_create_transaction'),
    path('referral/transactions/update/<str:referral_transaction_id>/', update_referral_transaction, name='referral_update_transaction'),
    path('referral/transactions/delete/<str:referral_transaction_id>/', delete_referral_transaction, name='referral_delete_transaction'),


    path('api/v0/referral/', include('referral.api.urls'), name='api_referral_v0'),
]  + static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)
