from django.shortcuts import render, get_object_or_404, redirect
from affiliate.models import AffiliateIncentive  # Importiamo il modello AffiliateIncentive
from affiliate.forms import AffiliateIncentiveForm
from django.contrib.auth.decorators import login_required

# LIST: Mostra tutte le trascrizioni
@login_required
def affiliate_incentive_list(request):
    affiliate_incentives = AffiliateIncentive.objects.all()
    return render(request, 'affiliate/affiliate_incentive_list.html', {'affiliate_incentives': affiliate_incentives})

# DETAIL: Mostra il dettaglio di una trascrizione
@login_required
def affiliate_incentive_detail(request, affiliate_incentive_id):
    affiliate_incentive = get_object_or_404(AffiliateIncentive, id=affiliate_incentive_id)
    return render(request, 'affiliate/affiliate_incentive_detail.html', {'affiliate_incentive': affiliate_incentive})

# CREATE: Crea una nuova trascrizione
@login_required
def create_affiliate_incentive(request):
    if request.method == 'POST':
        form = AffiliateIncentiveForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('affiliate/affiliate_incentive_list')
    else:
        form = AffiliateIncentiveForm()
    return render(request, 'affiliate/create_affiliate_incentive.html', {'form': form})

# UPDATE: Modifica una trascrizione
@login_required
def update_affiliate_incentive(request, affiliate_incentive_id):
    affiliate_incentive = get_object_or_404(AffiliateIncentive, id=affiliate_incentive_id)
    if request.method == 'POST':
        form = AffiliateIncentiveForm(request.POST, instance=affiliate_incentive)
        if form.is_valid():
            form.save()
            return redirect('affiliate/affiliate_incentive_detail', affiliate_incentive_id=affiliate_incentive_id)
    else:
        form = AffiliateIncentiveForm(instance=affiliate_incentive)
    return render(request, 'affiliate/update_affiliate_incentive.html', {'form': form})

# DELETE: Elimina una trascrizione
@login_required
def delete_affiliate_incentive(request, affiliate_incentive_id):
    affiliate_incentive = get_object_or_404(AffiliateIncentive, id=affiliate_incentive_id)
    if request.method == 'POST':
        affiliate_incentive.delete()
        return redirect('affiliate/affiliate_incentive_list')
    return render(request, 'delete_affiliate_incentive.html', {'affiliate_incentive': affiliate_incentive})
