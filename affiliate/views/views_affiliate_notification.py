from django.shortcuts import render, get_object_or_404, redirect
from affiliate.models import AffiliateNotification  # Importiamo il modello AffiliateNotification
from affiliate.forms import AffiliateNotificationForm
from django.contrib.auth.decorators import login_required

# LIST: Mostra tutte le trascrizioni
@login_required
def affiliate_notification_list(request):
    affiliate_notifications = AffiliateNotification.objects.all()
    return render(request, 'affiliate/affiliate_notification_list.html', {'affiliate_notifications': affiliate_notifications})

# DETAIL: Mostra il dettaglio di una trascrizione
@login_required
def affiliate_notification_detail(request, affiliate_notification_id):
    affiliate_notification = get_object_or_404(AffiliateNotification, id=affiliate_notification_id)
    return render(request, 'affiliate/affiliate_notification_detail.html', {'affiliate_notification': affiliate_notification})

# CREATE: Crea una nuova trascrizione
@login_required
def create_affiliate_notification(request):
    if request.method == 'POST':
        form = AffiliateNotificationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('affiliate/affiliate_notification_list')
    else:
        form = AffiliateNotificationForm()
    return render(request, 'affiliate/create_affiliate_notification.html', {'form': form})

# UPDATE: Modifica una trascrizione
@login_required
def update_affiliate_notification(request, affiliate_notification_id):
    affiliate_notification = get_object_or_404(AffiliateNotification, id=affiliate_notification_id)
    if request.method == 'POST':
        form = AffiliateNotificationForm(request.POST, instance=affiliate_notification)
        if form.is_valid():
            form.save()
            return redirect('affiliate/affiliate_notification_detail', affiliate_notification_id=affiliate_notification_id)
    else:
        form = AffiliateNotificationForm(instance=affiliate_notification)
    return render(request, 'affiliate/update_affiliate_notification.html', {'form': form})

# DELETE: Elimina una trascrizione
@login_required
def delete_affiliate_notification(request, affiliate_notification_id):
    affiliate_notification = get_object_or_404(AffiliateNotification, id=affiliate_notification_id)
    if request.method == 'POST':
        affiliate_notification.delete()
        return redirect('affiliate/affiliate_notification_list')
    return render(request, 'delete_affiliate_notification.html', {'affiliate_notification': affiliate_notification})
