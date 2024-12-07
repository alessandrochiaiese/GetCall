from django.shortcuts import render, get_object_or_404, redirect
from affiliate.models import AffiliateCommission  # Importiamo il modello AffiliateCommission
from affiliate.forms import AffiliateCommissionForm
from django.contrib.auth.decorators import login_required

# LIST: Mostra tutte le trascrizioni
@login_required
def affiliate_commission_list(request):
    affiliate_commissions = AffiliateCommission.objects.all()
    return render(request, 'affiliate/affiliate_commission_list.html', {'affiliate_commissions': affiliate_commissions})

# DETAIL: Mostra il dettaglio di una trascrizione
@login_required
def affiliate_commission_detail(request, affiliate_commission_id):
    affiliate_commission = get_object_or_404(AffiliateCommission, id=affiliate_commission_id)
    return render(request, 'affiliate/affiliate_commission_detail.html', {'affiliate_commission': affiliate_commission})

# CREATE: Crea una nuova trascrizione
@login_required
def create_affiliate_commission(request):
    if request.method == 'POST':
        form = AffiliateCommissionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('affiliate/affiliate_commission_list')
    else:
        form = AffiliateCommissionForm()
    return render(request, 'affiliate/create_affiliate_commission.html', {'form': form})

# UPDATE: Modifica una trascrizione
@login_required
def update_affiliate_commission(request, affiliate_commission_id):
    affiliate_commission = get_object_or_404(AffiliateCommission, id=affiliate_commission_id)
    if request.method == 'POST':
        form = AffiliateCommissionForm(request.POST, instance=affiliate_commission)
        if form.is_valid():
            form.save()
            return redirect('affiliate/affiliate_commission_detail', affiliate_commission_id=affiliate_commission_id)
    else:
        form = AffiliateCommissionForm(instance=affiliate_commission)
    return render(request, 'affiliate/update_affiliate_commission.html', {'form': form})

# DELETE: Elimina una trascrizione
@login_required
def delete_affiliate_commission(request, affiliate_commission_id):
    affiliate_commission = get_object_or_404(AffiliateCommission, id=affiliate_commission_id)
    if request.method == 'POST':
        affiliate_commission.delete()
        return redirect('affiliate/affiliate_commission_list')
    return render(request, 'delete_affiliate_commission.html', {'affiliate_commission': affiliate_commission})
