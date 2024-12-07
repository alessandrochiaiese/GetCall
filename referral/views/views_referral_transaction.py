from django.shortcuts import render, get_object_or_404, redirect
from referral.models import ReferralTransaction  # Importiamo il modello ReferralTransaction
from referral.forms import ReferralTransactionForm
from django.contrib.auth.decorators import login_required

# LIST: Mostra tutte le trascrizioni
@login_required
def referral_transaction_list(request):
    referral_transactions = ReferralTransaction.objects.all()
    return render(request, 'referral/referral_transaction_list.html', {'referral_transactions': referral_transactions})

# DETAIL: Mostra il dettaglio di una trascrizione
@login_required
def referral_transaction_detail(request, referral_transaction_id):
    referral_transaction = get_object_or_404(ReferralTransaction, id=referral_transaction_id)
    return render(request, 'referral/referral_transaction_detail.html', {'referral_transaction': referral_transaction})

# CREATE: Crea una nuova trascrizione
@login_required
def create_referral_transaction(request):
    if request.method == 'POST':
        form = ReferralTransactionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('referral/referral_transaction_list')
    else:
        form = ReferralTransactionForm()
    return render(request, 'referral/create_referral_transaction.html', {'form': form})

# UPDATE: Modifica una trascrizione
@login_required
def update_referral_transaction(request, referral_transaction_id):
    referral_transaction = get_object_or_404(ReferralTransaction, id=referral_transaction_id)
    if request.method == 'POST':
        form = ReferralTransactionForm(request.POST, instance=referral_transaction)
        if form.is_valid():
            form.save()
            return redirect('referral/referral_transaction_detail', referral_transaction_id=referral_transaction_id)
    else:
        form = ReferralTransactionForm(instance=referral_transaction)
    return render(request, 'referral/update_referral_transaction.html', {'form': form})

# DELETE: Elimina una trascrizione
@login_required
def delete_referral_transaction(request, referral_transaction_id):
    referral_transaction = get_object_or_404(ReferralTransaction, id=referral_transaction_id)
    if request.method == 'POST':
        referral_transaction.delete()
        return redirect('referral/referral_transaction_list')
    return render(request, 'delete_referral_transaction.html', {'referral_transaction': referral_transaction})
