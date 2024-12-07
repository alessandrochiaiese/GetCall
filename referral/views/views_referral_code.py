from django.shortcuts import render, get_object_or_404, redirect
from referral.models import ReferralCode  # Importiamo il modello ReferralCode
from referral.forms import ReferralCodeForm
from django.contrib.auth.decorators import login_required

# LIST: Mostra tutte le trascrizioni
@login_required
def referral_code_list(request):
    referral_codes = ReferralCode.objects.all()
    return render(request, 'referral/referral_code_list.html', {'referral_codes': referral_codes})

# DETAIL: Mostra il dettaglio di una trascrizione
@login_required
def referral_code_detail(request, referral_code_id):
    referral_code = get_object_or_404(ReferralCode, id=referral_code_id)
    return render(request, 'referral/referral_code_detail.html', {'referral_code': referral_code})

# CREATE: Crea una nuova trascrizione
@login_required
def create_referral_code(request):
    if request.method == 'POST':
        form = ReferralCodeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('referral/referral_code_list')
    else:
        form = ReferralCodeForm()
    return render(request, 'referral/create_referral_code.html', {'form': form})

# UPDATE: Modifica una trascrizione
@login_required
def update_referral_code(request, referral_code_id):
    referral_code = get_object_or_404(ReferralCode, id=referral_code_id)
    if request.method == 'POST':
        form = ReferralCodeForm(request.POST, instance=referral_code)
        if form.is_valid():
            form.save()
            return redirect('referral/referral_code_detail', referral_code_id=referral_code_id)
    else:
        form = ReferralCodeForm(instance=referral_code)
    return render(request, 'referral/update_referral_code.html', {'form': form})

# DELETE: Elimina una trascrizione
@login_required
def delete_referral_code(request, referral_code_id):
    referral_code = get_object_or_404(ReferralCode, id=referral_code_id)
    if request.method == 'POST':
        referral_code.delete()
        return redirect('referral/referral_code_list')
    return render(request, 'delete_referral_code.html', {'referral_code': referral_code})
