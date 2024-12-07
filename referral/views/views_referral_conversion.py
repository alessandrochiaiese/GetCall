from django.shortcuts import render, get_object_or_404, redirect
from referral.models import ReferralConversion  # Importiamo il modello ReferralConversion
from referral.forms import ReferralConversionForm
from django.contrib.auth.decorators import login_required

# LIST: Mostra tutte le trascrizioni
@login_required
def referral_conversion_list(request):
    referral_conversions = ReferralConversion.objects.all()
    return render(request, 'referral/referral_conversion_list.html', {'referral_conversions': referral_conversions})

# DETAIL: Mostra il dettaglio di una trascrizione
@login_required
def referral_conversion_detail(request, referral_conversion_id):
    referral_conversion = get_object_or_404(ReferralConversion, id=referral_conversion_id)
    return render(request, 'referral/referral_conversion_detail.html', {'referral_conversion': referral_conversion})

# CREATE: Crea una nuova trascrizione
@login_required
def create_referral_conversion(request):
    if request.method == 'POST':
        form = ReferralConversionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('referral/referral_conversion_list')
    else:
        form = ReferralConversionForm()
    return render(request, 'referral/create_referral_conversion.html', {'form': form})

# UPDATE: Modifica una trascrizione
@login_required
def update_referral_conversion(request, referral_conversion_id):
    referral_conversion = get_object_or_404(ReferralConversion, id=referral_conversion_id)
    if request.method == 'POST':
        form = ReferralConversionForm(request.POST, instance=referral_conversion)
        if form.is_valid():
            form.save()
            return redirect('referral/referral_conversion_detail', referral_conversion_id=referral_conversion_id)
    else:
        form = ReferralConversionForm(instance=referral_conversion)
    return render(request, 'referral/update_referral_conversion.html', {'form': form})

# DELETE: Elimina una trascrizione
@login_required
def delete_referral_conversion(request, referral_conversion_id):
    referral_conversion = get_object_or_404(ReferralConversion, id=referral_conversion_id)
    if request.method == 'POST':
        referral_conversion.delete()
        return redirect('referral/referral_conversion_list')
    return render(request, 'delete_referral_conversion.html', {'referral_conversion': referral_conversion})
