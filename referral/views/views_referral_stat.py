from django.shortcuts import render, get_object_or_404, redirect
from referral.models import ReferralStats  # Importiamo il modello ReferralStats
from referral.forms import ReferralStatsForm
from django.contrib.auth.decorators import login_required

# LIST: Mostra tutte le trascrizioni
@login_required
def referral_stat_list(request):
    referral_stats = ReferralStats.objects.all()
    return render(request, 'referral/referral_stat_list.html', {'referral_stats': referral_stats})

# DETAIL: Mostra il dettaglio di una trascrizione
@login_required
def referral_stat_detail(request, referral_stat_id):
    referral_stat = get_object_or_404(ReferralStats, id=referral_stat_id)
    return render(request, 'referral/referral_stat_detail.html', {'referral_stat': referral_stat})

# CREATE: Crea una nuova trascrizione
@login_required
def create_referral_stat(request):
    if request.method == 'POST':
        form = ReferralStatsForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('referral/referral_stat_list')
    else:
        form = ReferralStatsForm()
    return render(request, 'referral/create_referral_stat.html', {'form': form})

# UPDATE: Modifica una trascrizione
@login_required
def update_referral_stat(request, referral_stat_id):
    referral_stat = get_object_or_404(ReferralStats, id=referral_stat_id)
    if request.method == 'POST':
        form = ReferralStatsForm(request.POST, instance=referral_stat)
        if form.is_valid():
            form.save()
            return redirect('referral/referral_stat_detail', referral_stat_id=referral_stat_id)
    else:
        form = ReferralStatsForm(instance=referral_stat)
    return render(request, 'referral/update_referral_stat.html', {'form': form})

# DELETE: Elimina una trascrizione
@login_required
def delete_referral_stat(request, referral_stat_id):
    referral_stat = get_object_or_404(ReferralStats, id=referral_stat_id)
    if request.method == 'POST':
        referral_stat.delete()
        return redirect('referral/referral_stat_list')
    return render(request, 'delete_referral_stat.html', {'referral_stat': referral_stat})
