from django.shortcuts import render, get_object_or_404, redirect
from referral.models.referral_engagement import ReferralEngagement  # Importiamo il modello ReferralEngagement
from referral.forms import ReferralEngagementForm
from django.contrib.auth.decorators import login_required

# LIST: Mostra tutte le trascrizioni
@login_required
def referral_engagement_list(request):
    referral_engagements = ReferralEngagement.objects.all()
    return render(request, 'referral/referral_engagement_list.html', {'referral_engagements': referral_engagements})

# DETAIL: Mostra il dettaglio di una trascrizione
@login_required
def referral_engagement_detail(request, referral_engagement_id):
    referral_engagement = get_object_or_404(ReferralEngagement, id=referral_engagement_id)
    return render(request, 'referral/referral_engagement_detail.html', {'referral_engagement': referral_engagement})

# CREATE: Crea una nuova trascrizione
@login_required
def create_referral_engagement(request):
    if request.method == 'POST':
        form = ReferralEngagementForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('referral/referral_engagement_list')
    else:
        form = ReferralEngagementForm()
    return render(request, 'referral/create_referral_engagement.html', {'form': form})

# UPDATE: Modifica una trascrizione
@login_required
def update_referral_engagement(request, referral_engagement_id):
    referral_engagement = get_object_or_404(ReferralEngagement, id=referral_engagement_id)
    if request.method == 'POST':
        form = ReferralEngagementForm(request.POST, instance=referral_engagement)
        if form.is_valid():
            form.save()
            return redirect('referral/referral_engagement_detail', referral_engagement_id=referral_engagement_id)
    else:
        form = ReferralEngagementForm(instance=referral_engagement)
    return render(request, 'referral/update_referral_engagement.html', {'form': form})

# DELETE: Elimina una trascrizione
@login_required
def delete_referral_engagement(request, referral_engagement_id):
    referral_engagement = get_object_or_404(ReferralEngagement, id=referral_engagement_id)
    if request.method == 'POST':
        referral_engagement.delete()
        return redirect('referral/referral_engagement_list')
    return render(request, 'delete_referral_engagement.html', {'referral_engagement': referral_engagement})
