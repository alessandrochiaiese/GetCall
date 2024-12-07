from django.shortcuts import render, get_object_or_404, redirect
from referral.models import ReferralSettings  # Importiamo il modello ReferralSettings
from referral.forms import ReferralSettingsForm
from django.contrib.auth.decorators import login_required

# LIST: Mostra tutte le trascrizioni
@login_required
def referral_setting_list(request):
    referral_settings = ReferralSettings.objects.all()
    return render(request, 'referral/referral_setting_list.html', {'referral_settings': referral_settings})

# DETAIL: Mostra il dettaglio di una trascrizione
@login_required
def referral_setting_detail(request, referral_setting_id):
    referral_setting = get_object_or_404(ReferralSettings, id=referral_setting_id)
    return render(request, 'referral/referral_setting_detail.html', {'referral_setting': referral_setting})

# CREATE: Crea una nuova trascrizione
@login_required
def create_referral_setting(request):
    if request.method == 'POST':
        form = ReferralSettingsForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('referral/referral_setting_list')
    else:
        form = ReferralSettingsForm()
    return render(request, 'referral/create_referral_setting.html', {'form': form})

# UPDATE: Modifica una trascrizione
@login_required
def update_referral_setting(request, referral_setting_id):
    referral_setting = get_object_or_404(ReferralSettings, id=referral_setting_id)
    if request.method == 'POST':
        form = ReferralSettingsForm(request.POST, instance=referral_setting)
        if form.is_valid():
            form.save()
            return redirect('referral/referral_setting_detail', referral_setting_id=referral_setting_id)
    else:
        form = ReferralSettingsForm(instance=referral_setting)
    return render(request, 'referral/update_referral_setting.html', {'form': form})

# DELETE: Elimina una trascrizione
@login_required
def delete_referral_setting(request, referral_setting_id):
    referral_setting = get_object_or_404(ReferralSettings, id=referral_setting_id)
    if request.method == 'POST':
        referral_setting.delete()
        return redirect('referral/referral_setting_list')
    return render(request, 'delete_referral_setting.html', {'referral_setting': referral_setting})
