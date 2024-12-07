from django.forms import ModelForm
from django import forms
from affiliate.models import *

class AffiliateAuditForm(ModelForm):
    class Meta:
        model = AffiliateAudit
        fields = '__all__'

class AffiliateCampaignForm(ModelForm):
    class Meta:
        model = AffiliateCampaign
        fields = '__all__'

class AffiliateCommissionForm(ModelForm):
    class Meta:
        model = AffiliateCommission
        fields = '__all__'

class AffiliateLinkForm(ModelForm):
    class Meta:
        model = AffiliateLink
        fields = '__all__'
                  
class AffiliateNotificationForm(ModelForm):
    class Meta:
        model = AffiliateNotification
        fields = '__all__'
                  
class AffiliatePayoutForm(ModelForm):
    class Meta:
        model = AffiliatePayout
        fields = '__all__'
                  
class AffiliateIncentiveForm(ModelForm):
    class Meta:
        model = AffiliateIncentive
        fields = '__all__'
                  
class AffiliatePerformanceForm(ModelForm):
    class Meta:
        model = AffiliatePerformance
        fields = '__all__'
                  
class AffiliateProgramForm(ModelForm):
    class Meta:
        model = AffiliateProgram
        fields = '__all__'
                  
class AffiliateProgramPartecipationForm(ModelForm):
    class Meta:
        model = AffiliateProgramPartecipation
        fields = '__all__'
        
class AffiliateRewardForm(ModelForm):
    class Meta:
        model = AffiliateReward
        fields = '__all__'
                  
class AffiliateSettingsForm(ModelForm):
    class Meta:
        model = AffiliateSettings
        fields = '__all__'
                  
class AffiliateSupportTicketForm(ModelForm):
    class Meta:
        model = AffiliateSupportTicket
        fields = '__all__'
        
class AffiliateTierForm(ModelForm):
    class Meta:
        model = AffiliateTier
        fields = '__all__'
        
class AffiliateTransactionForm(ModelForm):
    class Meta:
        model = AffiliateTransaction
        fields = '__all__'
           