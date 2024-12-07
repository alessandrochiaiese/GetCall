from django.contrib import admin
from referral.models import *

admin.site.register(Referral)
admin.site.register(ReferralAudit)
admin.site.register(ReferralBonus)
admin.site.register(ReferralCampaign)
admin.site.register(ReferralCode)
admin.site.register(ReferralConversion)
admin.site.register(ReferralEngagement)
admin.site.register(ReferralNotification)
admin.site.register(ReferralProgramPartecipation)
admin.site.register(ReferralProgram)
admin.site.register(ReferralReward)
admin.site.register(ReferralSettings)
admin.site.register(ReferralStats)
admin.site.register(ReferralTransaction)
admin.site.register(ReferralUser)