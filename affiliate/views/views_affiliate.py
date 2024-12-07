
from django.shortcuts import render
from django.urls import path

# View per visualizzare la lista di affiliati
def affiliate_list_view(request):
    return render(request, 'affiliate/affiliate_list.html')

# View per visualizzare i dettagli di un affiliato specifico
def affiliate_detail_view(request, pk):
    return render(request, 'affiliate/affiliate_detail.html', {'affiliate_id': pk})


# View per visualizzare la lista di link affiliati
def affiliate_link_list_view(request):
    return render(request, 'affiliate/affiliate_link_list.html')

# View per visualizzare i dettagli di un link affiliato specifico
def affiliate_link_detail_view(request, pk):
    return render(request, 'affiliate/affiliate_link_detail.html', {'affiliate_link_id': pk})


# View per visualizzare la lista di audit affiliati
def affiliate_audit_list_view(request):
    return render(request, 'affiliate/affiliate_audit_list.html')

# View per visualizzare i dettagli di un audit affiliato specifico
def affiliate_audit_detail_view(request, pk):
    return render(request, 'affiliate/affiliate_audit_detail.html', {'affiliate_audit_id': pk})


# View per visualizzare la lista di campaign affiliati
def affiliate_campaign_list_view(request):
    return render(request, 'affiliate/affiliate_campaign_list.html')

# View per visualizzare i dettagli di un campaign affiliato specifico
def affiliate_campaign_detail_view(request, pk):
    return render(request, 'affiliate/affiliate_campaign_detail.html', {'affiliate_campaign_id': pk})


# View per visualizzare la lista di commission affiliati
def affiliate_commission_list_view(request):
    return render(request, 'affiliate/affiliate_commission_list.html')

# View per visualizzare i dettagli di un commission affiliato specifico
def affiliate_commission_detail_view(request, pk):
    return render(request, 'affiliate/affiliate_commission_detail.html', {'affiliate_commission_id': pk})


# View per visualizzare la lista di notification affiliati
def affiliate_notification_list_view(request):
    return render(request, 'affiliate/affiliate_notification_list.html')

# View per visualizzare i dettagli di un notification affiliato specifico
def affiliate_notification_detail_view(request, pk):
    return render(request, 'affiliate/affiliate_notification_detail.html', {'affiliate_notification_id': pk})


# View per visualizzare la lista di payout affiliati
def affiliate_payout_list_view(request):
    return render(request, 'affiliate/affiliate_payout_list.html')

# View per visualizzare i dettagli di un payout affiliato specifico
def affiliate_payout_detail_view(request, pk):
    return render(request, 'affiliate/affiliate_payout_detail.html', {'affiliate_payout_id': pk})


# View per visualizzare la lista di performance affiliati
def affiliate_performance_list_view(request):
    return render(request, 'affiliate/affiliate_performance_list.html')

# View per visualizzare i dettagli di un performance affiliato specifico
def affiliate_performance_detail_view(request, pk):
    return render(request, 'affiliate/affiliate_performance_detail.html', {'affiliate_performance_id': pk})


# View per visualizzare la lista di program affiliati
def affiliate_program_list_view(request):
    return render(request, 'affiliate/affiliate_program_list.html')

# View per visualizzare i dettagli di un program affiliato specifico
def affiliate_program_detail_view(request, pk):
    return render(request, 'affiliate/affiliate_program_detail.html', {'affiliate_program_id': pk})


# View per visualizzare la lista di program_partecipation affiliati
def affiliate_program_partecipation_list_view(request):
    return render(request, 'affiliate/affiliate_program_partecipation_list.html')

# View per visualizzare i dettagli di un program_partecipation affiliato specifico
def affiliate_program_partecipation_detail_view(request, pk):
    return render(request, 'affiliate/affiliate_program_partecipation_detail.html', {'affiliate_program_partecipation_id': pk})


# View per visualizzare la lista di reward affiliati
def affiliate_reward_list_view(request):
    return render(request, 'affiliate/affiliate_reward_list.html')

# View per visualizzare i dettagli di un reward affiliato specifico
def affiliate_reward_detail_view(request, pk):
    return render(request, 'affiliate/affiliate_reward_detail.html', {'affiliate_reward_id': pk})


# View per visualizzare la lista di setting affiliati
def affiliate_setting_list_view(request):
    return render(request, 'affiliate/affiliate_setting_list.html')

# View per visualizzare i dettagli di un setting affiliato specifico
def affiliate_setting_detail_view(request, pk):
    return render(request, 'affiliate/affiliate_setting_detail.html', {'affiliate_setting_id': pk})


# View per visualizzare la lista di support_ticket affiliati
def affiliate_support_ticket_list_view(request):
    return render(request, 'affiliate/affiliate_support_ticket_list.html')

# View per visualizzare i dettagli di un support_ticket affiliato specifico
def affiliate_support_ticket_detail_view(request, pk):
    return render(request, 'affiliate/affiliate_support_ticket_detail.html', {'affiliate_support_ticket_id': pk})


# View per visualizzare la lista di tier affiliati
def affiliate_tier_list_view(request):
    return render(request, 'affiliate/affiliate_tier_list.html')

# View per visualizzare i dettagli di un tier affiliato specifico
def affiliate_tier_detail_view(request, pk):
    return render(request, 'affiliate/affiliate_tier_detail.html', {'affiliate_tier_id': pk})


# View per visualizzare la lista di transaction affiliati
def affiliate_transaction_list_view(request):
    return render(request, 'affiliate/affiliate_transaction_list.html')

# View per visualizzare i dettagli di un transaction affiliato specifico
def affiliate_transaction_detail_view(request, pk):
    return render(request, 'affiliate/affiliate_transaction_detail.html', {'affiliate_transaction_id': pk})
 

"""from django.views.generic import TemplateView, ListView, DetailView
from affiliate.models import Affiliate, AffiliateLink, AffiliateReward
from ..forms import AffiliateLinkForm

class AffiliateDetailView(DetailView):
    model = Affiliate
    template_name = 'affiliate_system/affiliate_detail.html'
    context_object_name = 'affiliate'

class AffiliateLinkListView(ListView):
    model = AffiliateLink
    template_name = 'affiliate_system/affiliate_link_list.html'
    context_object_name = 'links'

    def get_queryset(self):
        affiliate_id = self.kwargs.get("affiliate_id")
        return AffiliateLink.objects.filter(affiliate_id=affiliate_id)

class AffiliateRewardListView(ListView):
    model = AffiliateReward
    template_name = 'affiliate_system/affiliate_reward_list.html'
    context_object_name = 'rewards'

    def get_queryset(self):
        affiliate_id = self.kwargs.get("affiliate_id")
        return AffiliateReward.objects.filter(affiliate_id=affiliate_id)
    
    
from django.shortcuts import render
from django.views.generic import View

# Views per il sistema di affiliazione
class AffiliateProgramsPageView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'affiliate/affiliate_programs.html')

class AffiliateLinksPageView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'ffiliate_links.html')

class AffiliateCommissionsPageView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'affiliate/affiliate_commissions.html')

"""