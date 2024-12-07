from django.shortcuts import render, get_object_or_404, redirect
from referral.models import ReferralNotification  # Importiamo il modello ReferralNotification
from referral.forms import ReferralNotificationForm
from django.contrib.auth.decorators import login_required

# LIST: Mostra tutte le trascrizioni
@login_required
def referral_notification_list(request):
    referral_notifications = ReferralNotification.objects.all()
    return render(request, 'referral/referral_notification_list.html', {'referral_notifications': referral_notifications})

# DETAIL: Mostra il dettaglio di una trascrizione
@login_required
def referral_notification_detail(request, referral_notification_id):
    referral_notification = get_object_or_404(ReferralNotification, id=referral_notification_id)
    return render(request, 'referral/referral_notification_detail.html', {'referral_notification': referral_notification})

# CREATE: Crea una nuova trascrizione
@login_required
def create_referral_notification(request):
    if request.method == 'POST':
        form = ReferralNotificationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('referral/referral_notification_list')
    else:
        form = ReferralNotificationForm()
    return render(request, 'referral/create_referral_notification.html', {'form': form})

# UPDATE: Modifica una trascrizione
@login_required
def update_referral_notification(request, referral_notification_id):
    referral_notification = get_object_or_404(ReferralNotification, id=referral_notification_id)
    if request.method == 'POST':
        form = ReferralNotificationForm(request.POST, instance=referral_notification)
        if form.is_valid():
            form.save()
            return redirect('referral/referral_notification_detail', referral_notification_id=referral_notification_id)
    else:
        form = ReferralNotificationForm(instance=referral_notification)
    return render(request, 'referral/update_referral_notification.html', {'form': form})

# DELETE: Elimina una trascrizione
@login_required
def delete_referral_notification(request, referral_notification_id):
    referral_notification = get_object_or_404(ReferralNotification, id=referral_notification_id)
    if request.method == 'POST':
        referral_notification.delete()
        return redirect('referral/referral_notification_list')
    return render(request, 'delete_referral_notification.html', {'referral_notification': referral_notification})
