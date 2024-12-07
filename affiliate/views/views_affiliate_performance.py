from django.shortcuts import render, get_object_or_404, redirect
from affiliate.models.affiliate_performance import AffiliatePerformance  # Importiamo il modello AffiliatePerformance
from affiliate.forms import AffiliatePerformanceForm
from django.contrib.auth.decorators import login_required

# LIST: Mostra tutte le trascrizioni
@login_required
def affiliate_performance_list(request):
    affiliate_performances = AffiliatePerformance.objects.all()
    return render(request, 'affiliate/affiliate_performance_list.html', {'affiliate_performances': affiliate_performances})

# DETAIL: Mostra il dettaglio di una trascrizione
@login_required
def affiliate_performance_detail(request, affiliate_performance_id):
    affiliate_performance = get_object_or_404(AffiliatePerformance, id=affiliate_performance_id)
    return render(request, 'affiliate/affiliate_performance_detail.html', {'affiliate_performance': affiliate_performance})

# CREATE: Crea una nuova trascrizione
@login_required
def create_affiliate_performance(request):
    if request.method == 'POST':
        form = AffiliatePerformanceForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('affiliate/affiliate_performance_list')
    else:
        form = AffiliatePerformanceForm()
    return render(request, 'affiliate/create_affiliate_performance.html', {'form': form})

# UPDATE: Modifica una trascrizione
@login_required
def update_affiliate_performance(request, affiliate_performance_id):
    affiliate_performance = get_object_or_404(AffiliatePerformance, id=affiliate_performance_id)
    if request.method == 'POST':
        form = AffiliatePerformanceForm(request.POST, instance=affiliate_performance)
        if form.is_valid():
            form.save()
            return redirect('affiliate/affiliate_performance_detail', affiliate_performance_id=affiliate_performance_id)
    else:
        form = AffiliatePerformanceForm(instance=affiliate_performance)
    return render(request, 'affiliate/update_affiliate_performance.html', {'form': form})

# DELETE: Elimina una trascrizione
@login_required
def delete_affiliate_performance(request, affiliate_performance_id):
    affiliate_performance = get_object_or_404(AffiliatePerformance, id=affiliate_performance_id)
    if request.method == 'POST':
        affiliate_performance.delete()
        return redirect('affiliate/affiliate_performance_list')
    return render(request, 'delete_affiliate_performance.html', {'affiliate_performance': affiliate_performance})
