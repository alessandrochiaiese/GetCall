from django.shortcuts import render, get_object_or_404, redirect
from affiliate.models import AffiliatePayout  # Importiamo il modello AffiliatePayout
from affiliate.forms import AffiliatePayoutForm
from django.contrib.auth.decorators import login_required

# LIST: Mostra tutte le trascrizioni
@login_required
def affiliate_payout_list(request):
    affiliate_payouts = AffiliatePayout.objects.all()
    return render(request, 'affiliate/affiliate_payout_list.html', {'affiliate_payouts': affiliate_payouts})

# DETAIL: Mostra il dettaglio di una trascrizione
@login_required
def affiliate_payout_detail(request, affiliate_payout_id):
    affiliate_payout = get_object_or_404(AffiliatePayout, id=affiliate_payout_id)
    return render(request, 'affiliate/affiliate_payout_detail.html', {'affiliate_payout': affiliate_payout})

# CREATE: Crea una nuova trascrizione
@login_required
def create_affiliate_payout(request):
    if request.method == 'POST':
        form = AffiliatePayoutForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('affiliate/affiliate_payout_list')
    else:
        form = AffiliatePayoutForm()
    return render(request, 'affiliate/create_affiliate_payout.html', {'form': form})

# UPDATE: Modifica una trascrizione
@login_required
def update_affiliate_payout(request, affiliate_payout_id):
    affiliate_payout = get_object_or_404(AffiliatePayout, id=affiliate_payout_id)
    if request.method == 'POST':
        form = AffiliatePayoutForm(request.POST, instance=affiliate_payout)
        if form.is_valid():
            form.save()
            return redirect('affiliate/affiliate_payout_detail', affiliate_payout_id=affiliate_payout_id)
    else:
        form = AffiliatePayoutForm(instance=affiliate_payout)
    return render(request, 'affiliate/update_affiliate_payout.html', {'form': form})

# DELETE: Elimina una trascrizione
@login_required
def delete_affiliate_payout(request, affiliate_payout_id):
    affiliate_payout = get_object_or_404(AffiliatePayout, id=affiliate_payout_id)
    if request.method == 'POST':
        affiliate_payout.delete()
        return redirect('affiliate/affiliate_payout_list')
    return render(request, 'delete_affiliate_payout.html', {'affiliate_payout': affiliate_payout})
