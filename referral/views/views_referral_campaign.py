from django.shortcuts import render, get_object_or_404, redirect
from referral.models import ReferralCampaign  # Importiamo il modello ReferralCampaign
from referral.forms import ReferralCampaignForm
from django.contrib.auth.decorators import login_required

# LIST: Mostra tutte le trascrizioni
@login_required
def referral_campaign_list(request):
    referral_campaigns = ReferralCampaign.objects.all()
    return render(request, 'referral/referral_campaign_list.html', {'referral_campaigns': referral_campaigns})

# DETAIL: Mostra il dettaglio di una trascrizione
@login_required
def referral_campaign_detail(request, referral_campaign_id):
    referral_campaign = get_object_or_404(ReferralCampaign, id=referral_campaign_id)
    return render(request, 'referral/referral_campaign_detail.html', {'referral_campaign': referral_campaign})

# CREATE: Crea una nuova trascrizione
@login_required
def create_referral_campaign(request):
    if request.method == 'POST':
        form = ReferralCampaignForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('referral/referral_campaign_list')
    else:
        form = ReferralCampaignForm()
    return render(request, 'referral/create_referral_campaign.html', {'form': form})

# UPDATE: Modifica una trascrizione
@login_required
def update_referral_campaign(request, referral_campaign_id):
    referral_campaign = get_object_or_404(ReferralCampaign, id=referral_campaign_id)
    if request.method == 'POST':
        form = ReferralCampaignForm(request.POST, instance=referral_campaign)
        if form.is_valid():
            form.save()
            return redirect('referral/referral_campaign_detail', referral_campaign_id=referral_campaign_id)
    else:
        form = ReferralCampaignForm(instance=referral_campaign)
    return render(request, 'referral/update_referral_campaign.html', {'form': form})

# DELETE: Elimina una trascrizione
@login_required
def delete_referral_campaign(request, referral_campaign_id):
    referral_campaign = get_object_or_404(ReferralCampaign, id=referral_campaign_id)
    if request.method == 'POST':
        referral_campaign.delete()
        return redirect('referral/referral_campaign_list')
    return render(request, 'delete_referral_campaign.html', {'referral_campaign': referral_campaign})
