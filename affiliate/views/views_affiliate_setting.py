from django.shortcuts import render, get_object_or_404, redirect
from affiliate.models import AffiliateSettings  # Importiamo il modello AffiliateSettings
from affiliate.forms import AffiliateSettingsForm
from django.contrib.auth.decorators import login_required

# LIST: Mostra tutte le trascrizioni
@login_required
def affiliate_setting_list(request):
    affiliate_settings = AffiliateSettings.objects.all()
    return render(request, 'affiliate/affiliate_setting_list.html', {'affiliate_settings': affiliate_settings})

# DETAIL: Mostra il dettaglio di una trascrizione
@login_required
def affiliate_setting_detail(request, affiliate_setting_id):
    affiliate_setting = get_object_or_404(AffiliateSettings, id=affiliate_setting_id)
    return render(request, 'affiliate/affiliate_setting_detail.html', {'affiliate_setting': affiliate_setting})

# CREATE: Crea una nuova trascrizione
@login_required
def create_affiliate_setting(request):
    if request.method == 'POST':
        form = AffiliateSettingsForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('affiliate/affiliate_setting_list')
    else:
        form = AffiliateSettingsForm()
    return render(request, 'affiliate/create_affiliate_setting.html', {'form': form})

# UPDATE: Modifica una trascrizione
@login_required
def update_affiliate_setting(request, affiliate_setting_id):
    affiliate_setting = get_object_or_404(AffiliateSettings, id=affiliate_setting_id)
    if request.method == 'POST':
        form = AffiliateSettingsForm(request.POST, instance=affiliate_setting)
        if form.is_valid():
            form.save()
            return redirect('affiliate/affiliate_setting_detail', affiliate_setting_id=affiliate_setting_id)
    else:
        form = AffiliateSettingsForm(instance=affiliate_setting)
    return render(request, 'affiliate/update_affiliate_setting.html', {'form': form})

# DELETE: Elimina una trascrizione
@login_required
def delete_affiliate_setting(request, affiliate_setting_id):
    affiliate_setting = get_object_or_404(AffiliateSettings, id=affiliate_setting_id)
    if request.method == 'POST':
        affiliate_setting.delete()
        return redirect('affiliate/affiliate_setting_list')
    return render(request, 'delete_affiliate_setting.html', {'affiliate_setting': affiliate_setting})
