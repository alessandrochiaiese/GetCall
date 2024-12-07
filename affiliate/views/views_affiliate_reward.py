from django.shortcuts import render, get_object_or_404, redirect
from affiliate.models import AffiliateReward  # Importiamo il modello AffiliateReward
from affiliate.forms import AffiliateRewardForm
from django.contrib.auth.decorators import login_required

# LIST: Mostra tutte le trascrizioni
@login_required
def affiliate_reward_list(request):
    affiliate_rewards = AffiliateReward.objects.all()
    return render(request, 'affiliate/affiliate_reward_list.html', {'affiliate_rewards': affiliate_rewards})

# DETAIL: Mostra il dettaglio di una trascrizione
@login_required
def affiliate_reward_detail(request, affiliate_reward_id):
    affiliate_reward = get_object_or_404(AffiliateReward, id=affiliate_reward_id)
    return render(request, 'affiliate/affiliate_reward_detail.html', {'affiliate_reward': affiliate_reward})

# CREATE: Crea una nuova trascrizione
@login_required
def create_affiliate_reward(request):
    if request.method == 'POST':
        form = AffiliateRewardForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('affiliate/affiliate_reward_list')
    else:
        form = AffiliateRewardForm()
    return render(request, 'affiliate/create_affiliate_reward.html', {'form': form})

# UPDATE: Modifica una trascrizione
@login_required
def update_affiliate_reward(request, affiliate_reward_id):
    affiliate_reward = get_object_or_404(AffiliateReward, id=affiliate_reward_id)
    if request.method == 'POST':
        form = AffiliateRewardForm(request.POST, instance=affiliate_reward)
        if form.is_valid():
            form.save()
            return redirect('affiliate/affiliate_reward_detail', affiliate_reward_id=affiliate_reward_id)
    else:
        form = AffiliateRewardForm(instance=affiliate_reward)
    return render(request, 'affiliate/update_affiliate_reward.html', {'form': form})

# DELETE: Elimina una trascrizione
@login_required
def delete_affiliate_reward(request, affiliate_reward_id):
    affiliate_reward = get_object_or_404(AffiliateReward, id=affiliate_reward_id)
    if request.method == 'POST':
        affiliate_reward.delete()
        return redirect('affiliate/affiliate_reward_list')
    return render(request, 'delete_affiliate_reward.html', {'affiliate_reward': affiliate_reward})
