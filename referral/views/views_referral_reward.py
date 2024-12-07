from django.shortcuts import render, get_object_or_404, redirect
from referral.models import ReferralReward  # Importiamo il modello ReferralReward
from referral.forms import ReferralRewardForm
from django.contrib.auth.decorators import login_required

# LIST: Mostra tutte le trascrizioni
@login_required
def referral_reward_list(request):
    referral_rewards = ReferralReward.objects.all()
    return render(request, 'referral/referral_reward_list.html', {'referral_rewards': referral_rewards})

# DETAIL: Mostra il dettaglio di una trascrizione
@login_required
def referral_reward_detail(request, referral_reward_id):
    referral_reward = get_object_or_404(ReferralReward, id=referral_reward_id)
    return render(request, 'referral/referral_reward_detail.html', {'referral_reward': referral_reward})

# CREATE: Crea una nuova trascrizione
@login_required
def create_referral_reward(request):
    if request.method == 'POST':
        form = ReferralRewardForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('referral/referral_reward_list')
    else:
        form = ReferralRewardForm()
    return render(request, 'referral/create_referral_reward.html', {'form': form})

# UPDATE: Modifica una trascrizione
@login_required
def update_referral_reward(request, referral_reward_id):
    referral_reward = get_object_or_404(ReferralReward, id=referral_reward_id)
    if request.method == 'POST':
        form = ReferralRewardForm(request.POST, instance=referral_reward)
        if form.is_valid():
            form.save()
            return redirect('referral/referral_reward_detail', referral_reward_id=referral_reward_id)
    else:
        form = ReferralRewardForm(instance=referral_reward)
    return render(request, 'referral/update_referral_reward.html', {'form': form})

# DELETE: Elimina una trascrizione
@login_required
def delete_referral_reward(request, referral_reward_id):
    referral_reward = get_object_or_404(ReferralReward, id=referral_reward_id)
    if request.method == 'POST':
        referral_reward.delete()
        return redirect('referral/referral_reward_list')
    return render(request, 'delete_referral_reward.html', {'referral_reward': referral_reward})
