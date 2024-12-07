from django.shortcuts import render, get_object_or_404, redirect
from referral.models.referral_bonus import ReferralBonus  # Importiamo il modello ReferralBonus
from referral.forms import ReferralBonusForm
from django.contrib.auth.decorators import login_required

# LIST: Mostra tutte le trascrizioni
@login_required
def referral_bonus_list(request):
    referral_bonus = ReferralBonus.objects.all()
    return render(request, 'referral/referral_bonus_list.html', {'referral_bonus': referral_bonus})

# DETAIL: Mostra il dettaglio di una trascrizione
@login_required
def referral_bonus_detail(request, referral_bonus_id):
    referral_bonus = get_object_or_404(ReferralBonus, id=referral_bonus_id)
    return render(request, 'referral/referral_bonus_detail.html', {'referral_bonus': referral_bonus})

# CREATE: Crea una nuova trascrizione
@login_required
def create_referral_bonus(request):
    if request.method == 'POST':
        form = ReferralBonusForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('referral/referral_bonus_list')
    else:
        form = ReferralBonusForm()
    return render(request, 'referral/create_referral_bonus.html', {'form': form})

# UPDATE: Modifica una trascrizione
@login_required
def update_referral_bonus(request, referral_bonus_id):
    referral_bonus = get_object_or_404(ReferralBonus, id=referral_bonus_id)
    if request.method == 'POST':
        form = ReferralBonusForm(request.POST, instance=referral_bonus)
        if form.is_valid():
            form.save()
            return redirect('referral/referral_bonus_detail', referral_bonus_id=referral_bonus_id)
    else:
        form = ReferralBonusForm(instance=referral_bonus)
    return render(request, 'referral/update_referral_bonus.html', {'form': form})

# DELETE: Elimina una trascrizione
@login_required
def delete_referral_bonus(request, referral_bonus_id):
    referral_bonus = get_object_or_404(ReferralBonus, id=referral_bonus_id)
    if request.method == 'POST':
        referral_bonus.delete()
        return redirect('referral/referral_bonus_list')
    return render(request, 'delete_referral_bonus.html', {'referral_bonus': referral_bonus})
