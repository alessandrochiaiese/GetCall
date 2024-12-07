from django.shortcuts import render, get_object_or_404, redirect
from affiliate.models import AffiliateTransaction  # Importiamo il modello AffiliateTransaction
from affiliate.forms import AffiliateTransactionForm
from django.contrib.auth.decorators import login_required

# LIST: Mostra tutte le trascrizioni
@login_required
def affiliate_transaction_list(request):
    affiliate_transactions = AffiliateTransaction.objects.all()
    return render(request, 'affiliate/affiliate_transaction_list.html', {'affiliate_transactions': affiliate_transactions})

# DETAIL: Mostra il dettaglio di una trascrizione
@login_required
def affiliate_transaction_detail(request, affiliate_transaction_id):
    affiliate_transaction = get_object_or_404(AffiliateTransaction, id=affiliate_transaction_id)
    return render(request, 'affiliate/affiliate_transaction_detail.html', {'affiliate_transaction': affiliate_transaction})

# CREATE: Crea una nuova trascrizione
@login_required
def create_affiliate_transaction(request):
    if request.method == 'POST':
        form = AffiliateTransactionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('affiliate/affiliate_transaction_list')
    else:
        form = AffiliateTransactionForm()
    return render(request, 'affiliate/create_affiliate_transaction.html', {'form': form})

# UPDATE: Modifica una trascrizione
@login_required
def update_affiliate_transaction(request, affiliate_transaction_id):
    affiliate_transaction = get_object_or_404(AffiliateTransaction, id=affiliate_transaction_id)
    if request.method == 'POST':
        form = AffiliateTransactionForm(request.POST, instance=affiliate_transaction)
        if form.is_valid():
            form.save()
            return redirect('affiliate/affiliate_transaction_detail', affiliate_transaction_id=affiliate_transaction_id)
    else:
        form = AffiliateTransactionForm(instance=affiliate_transaction)
    return render(request, 'affiliate/update_affiliate_transaction.html', {'form': form})

# DELETE: Elimina una trascrizione
@login_required
def delete_affiliate_transaction(request, affiliate_transaction_id):
    affiliate_transaction = get_object_or_404(AffiliateTransaction, id=affiliate_transaction_id)
    if request.method == 'POST':
        affiliate_transaction.delete()
        return redirect('affiliate/affiliate_transaction_list')
    return render(request, 'delete_affiliate_transaction.html', {'affiliate_transaction': affiliate_transaction})
