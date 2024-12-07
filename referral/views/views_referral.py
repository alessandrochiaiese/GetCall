
from django.shortcuts import render
from django.urls import path

# View per visualizzare la lista di referenze
def referral_list_view(request):
    return render(request, 'referral/referral_list.html')

# View per visualizzare i dettagli di un affiliato specifico
def referral_detail_view(request, pk):
    return render(request, 'referral/referral_detail.html', {'referral_id': pk})


# View per visualizzare la lista di bonus referenze
def referral_bonus_list_view(request):
    return render(request, 'referral/referral_bonus_list.html')

# View per visualizzare i dettagli di un bonus affiliato specifico
def referral_bonus_detail_view(request, pk):
    return render(request, 'referral/referral_bonus_detail.html', {'referral_bonus_id': pk})


# View per visualizzare la lista di link referenze
def referral_link_list_view(request):
    return render(request, 'referral/referral_link_list.html')

# View per visualizzare i dettagli di un link affiliato specifico
def referral_link_detail_view(request, pk):
    return render(request, 'referral/referral_link_detail.html', {'referral_link_id': pk})


# View per visualizzare la lista di audit referenze
def referral_audit_list_view(request):
    return render(request, 'referral/referral_audit_list.html')

# View per visualizzare i dettagli di un audit affiliato specifico
def referral_audit_detail_view(request, pk):
    return render(request, 'referral/referral_audit_detail.html', {'referral_audit_id': pk})


# View per visualizzare la lista di campaign referenze
def referral_campaign_list_view(request):
    return render(request, 'referral/referral_campaign_list.html')

# View per visualizzare i dettagli di un campaign affiliato specifico
def referral_campaign_detail_view(request, pk):
    return render(request, 'referral/referral_campaign_detail.html', {'referral_campaign_id': pk})


# View per visualizzare la lista di conversion referenze
def referral_conversion_list_view(request):
    return render(request, 'referral/referral_conversion_list.html')

# View per visualizzare i dettagli di un conversion affiliato specifico
def referral_conversion_detail_view(request, pk):
    return render(request, 'referral/referral_conversion_detail.html', {'referral_conversion_id': pk})


# View per visualizzare la lista di notification referenze
def referral_notification_list_view(request):
    return render(request, 'referral/referral_notification_list.html')

# View per visualizzare i dettagli di un notification affiliato specifico
def referral_notification_detail_view(request, pk):
    return render(request, 'referral/referral_notification_detail.html', {'referral_notification_id': pk})


# View per visualizzare la lista di engagement referenze
def referral_engagement_list_view(request):
    return render(request, 'referral/referral_engagement_list.html')

# View per visualizzare i dettagli di un engagement affiliato specifico
def referral_engagement_detail_view(request, pk):
    return render(request, 'referral/referral_engagement_detail.html', {'referral_engagement_id': pk})
 

# View per visualizzare la lista di program referenze
def referral_program_list_view(request):
    return render(request, 'referral/referral_program_list.html')

# View per visualizzare i dettagli di un program affiliato specifico
def referral_program_detail_view(request, pk):
    return render(request, 'referral/referral_program_detail.html', {'referral_program_id': pk})


# View per visualizzare la lista di program_partecipation referenze
def referral_program_partecipation_list_view(request):
    return render(request, 'referral/referral_program_partecipation_list.html')

# View per visualizzare i dettagli di un program_partecipation affiliato specifico
def referral_program_partecipation_detail_view(request, pk):
    return render(request, 'referral/referral_program_partecipation_detail.html', {'referral_program_partecipation_id': pk})


# View per visualizzare la lista di reward referenze
def referral_reward_list_view(request):
    return render(request, 'referral/referral_reward_list.html')

# View per visualizzare i dettagli di un reward affiliato specifico
def referral_reward_detail_view(request, pk):
    return render(request, 'referral/referral_reward_detail.html', {'referral_reward_id': pk})


# View per visualizzare la lista di setting referenze
def referral_setting_list_view(request):
    return render(request, 'referral/referral_setting_list.html')

# View per visualizzare i dettagli di un setting affiliato specifico
def referral_setting_detail_view(request, pk):
    return render(request, 'referral/referral_setting_detail.html', {'referral_setting_id': pk})


# View per visualizzare la lista di stat referenze
def referral_stat_list_view(request):
    return render(request, 'referral/referral_stat_list.html')

# View per visualizzare i dettagli di un stat affiliato specifico
def referral_stat_detail_view(request, pk):
    return render(request, 'referral/referral_stat_detail.html', {'referral_stat_id': pk})
 
 
# View per visualizzare la lista di transaction referenze
def referral_transaction_list_view(request):
    return render(request, 'referral/referral_transaction_list.html')

# View per visualizzare i dettagli di un transaction affiliato specifico
def referral_transaction_detail_view(request, pk):
    return render(request, 'referral/referral_transaction_detail.html', {'referral_transaction_id': pk})
 

# View per visualizzare la lista di user referenze
def referral_user_list_view(request):
    return render(request, 'referral/referral_user_list.html')

# View per visualizzare i dettagli di un user affiliato specifico
def referral_user_detail_view(request, pk):
    return render(request, 'referral/referral_user_detail.html', {'referral_user_id': pk})
 

"""from django.views.generic import TemplateView, ListView, FormView
from referral.models import ReferralProgram, Referral, ReferralReward
from ..forms import ReferralForm

class ReferralProgramListView(ListView):
    model = ReferralProgram
    template_name = 'referral_system/referral_program_list.html'
    context_object_name = 'programs'

class ReferralCreateView(FormView):
    template_name = 'referral_system/referral_create.html'
    form_class = ReferralForm
    success_url = '/referral_system/referral/success/'  # URL di successo dopo il referral

    def form_valid(self, form):
        form.save()  # Esegue il salvataggio del referral
        return super().form_valid(form)

class ReferralRewardListView(ListView):
    model = ReferralReward
    template_name = 'referral_system/referral_reward_list.html'
    context_object_name = 'rewards'


# Views per il sistema di referral
class ReferralCodesPageView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'referral/referral_codes.html')

class ReferralProgramsPageView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'referral/referral_programs.html')"""