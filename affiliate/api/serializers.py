# affiliate_system/serializers.py

from rest_framework import serializers
from affiliate.models import *

class AffiliateAuditSerializer(serializers.ModelSerializer):
    class Meta:
        model = AffiliateAudit
        fields = ['id', 'action_taken', 'action_date', 'ip_address', 'device_info', 'location'] #'__all__'

class AffiliateCampaignSerializer(serializers.ModelSerializer):
    class Meta:
        model = AffiliateCampaign
        fields = '__all__'

class AffiliateCommissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = AffiliateCommission
        fields = '__all__'

class AffiliateLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = AffiliateLink
        fields = '__all__'
                  
class AffiliateNotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = AffiliateNotification
        fields = '__all__'
                  
class AffiliatePayoutSerializer(serializers.ModelSerializer):
    class Meta:
        model = AffiliatePayout
        fields = '__all__'
                  
class AffiliatePerformanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = AffiliatePerformance
        fields = '__all__'
                  
class AffiliateProgramSerializer(serializers.ModelSerializer):
    class Meta:
        model = AffiliateProgram
        fields = '__all__'
                  
class AffiliateProgramPartecipationSerializer(serializers.ModelSerializer):
    class Meta:
        model = AffiliateProgramPartecipation
        fields = '__all__'
        
class AffiliateRewardSerializer(serializers.ModelSerializer):
    class Meta:
        model = AffiliateReward
        fields = '__all__'
                  
class AffiliateSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = AffiliateSettings
        fields = '__all__'
                  
class AffiliateSupportTicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = AffiliateSupportTicket
        fields = '__all__'
        
class AffiliateTierSerializer(serializers.ModelSerializer):
    class Meta:
        model = AffiliateTier
        fields = '__all__'
        
class AffiliateTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = AffiliateTransaction
        fields = '__all__'
