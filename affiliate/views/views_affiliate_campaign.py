from django.shortcuts import render, get_object_or_404, redirect
from affiliate.models import AffiliateCampaign  # Importiamo il modello AffiliateCampaign
from affiliate.forms import AffiliateCampaignForm
from django.contrib.auth.decorators import login_required

# LIST: Mostra tutte le trascrizioni
@login_required
def affiliate_campaign_list(request):
    affiliate_campaigns = AffiliateCampaign.objects.all()
    return render(request, 'affiliate/affiliate_campaign_list.html', {'affiliate_campaigns': affiliate_campaigns})

# DETAIL: Mostra il dettaglio di una trascrizione
@login_required
def affiliate_campaign_detail(request, affiliate_campaign_id):
    affiliate_campaign = get_object_or_404(AffiliateCampaign, id=affiliate_campaign_id)
    return render(request, 'affiliate/affiliate_campaign_detail.html', {'affiliate_campaign': affiliate_campaign})

# CREATE: Crea una nuova trascrizione
@login_required
def create_affiliate_campaign(request):
    if request.method == 'POST':
        form = AffiliateCampaignForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('affiliate/affiliate_campaign_list')
    else:
        form = AffiliateCampaignForm()
    return render(request, 'affiliate/create_affiliate_campaign.html', {'form': form})

# UPDATE: Modifica una trascrizione
@login_required
def update_affiliate_campaign(request, affiliate_campaign_id):
    affiliate_campaign = get_object_or_404(AffiliateCampaign, id=affiliate_campaign_id)
    if request.method == 'POST':
        form = AffiliateCampaignForm(request.POST, instance=affiliate_campaign)
        if form.is_valid():
            form.save()
            return redirect('affiliate/affiliate_campaign_detail', affiliate_campaign_id=affiliate_campaign_id)
    else:
        form = AffiliateCampaignForm(instance=affiliate_campaign)
    return render(request, 'affiliate/update_affiliate_campaign.html', {'form': form})

# DELETE: Elimina una trascrizione
@login_required
def delete_affiliate_campaign(request, affiliate_campaign_id):
    affiliate_campaign = get_object_or_404(AffiliateCampaign, id=affiliate_campaign_id)
    if request.method == 'POST':
        affiliate_campaign.delete()
        return redirect('affiliate/affiliate_campaign_list')
    return render(request, 'delete_affiliate_campaign.html', {'affiliate_campaign': affiliate_campaign})
