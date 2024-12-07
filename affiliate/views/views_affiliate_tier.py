from django.shortcuts import render, get_object_or_404, redirect
from affiliate.models import AffiliateTier  # Importiamo il modello AffiliateTier
from affiliate.forms import AffiliateTierForm
from django.contrib.auth.decorators import login_required

# LIST: Mostra tutte le trascrizioni
@login_required
def affiliate_tier_list(request):
    affiliate_tiers = AffiliateTier.objects.all()
    return render(request, 'affiliate/affiliate_tier_list.html', {'affiliate_tiers': affiliate_tiers})

# DETAIL: Mostra il dettaglio di una trascrizione
@login_required
def affiliate_tier_detail(request, affiliate_tier_id):
    affiliate_tier = get_object_or_404(AffiliateTier, id=affiliate_tier_id)
    return render(request, 'affiliate/affiliate_tier_detail.html', {'affiliate_tier': affiliate_tier})

# CREATE: Crea una nuova trascrizione
@login_required
def create_affiliate_tier(request):
    if request.method == 'POST':
        form = AffiliateTierForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('affiliate/affiliate_tier_list')
    else:
        form = AffiliateTierForm()
    return render(request, 'affiliate/create_affiliate_tier.html', {'form': form})

# UPDATE: Modifica una trascrizione
@login_required
def update_affiliate_tier(request, affiliate_tier_id):
    affiliate_tier = get_object_or_404(AffiliateTier, id=affiliate_tier_id)
    if request.method == 'POST':
        form = AffiliateTierForm(request.POST, instance=affiliate_tier)
        if form.is_valid():
            form.save()
            return redirect('affiliate/affiliate_tier_detail', affiliate_tier_id=affiliate_tier_id)
    else:
        form = AffiliateTierForm(instance=affiliate_tier)
    return render(request, 'affiliate/update_affiliate_tier.html', {'form': form})

# DELETE: Elimina una trascrizione
@login_required
def delete_affiliate_tier(request, affiliate_tier_id):
    affiliate_tier = get_object_or_404(AffiliateTier, id=affiliate_tier_id)
    if request.method == 'POST':
        affiliate_tier.delete()
        return redirect('affiliate/affiliate_tier_list')
    return render(request, 'delete_affiliate_tier.html', {'affiliate_tier': affiliate_tier})
