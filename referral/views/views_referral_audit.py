from django.shortcuts import render, get_object_or_404, redirect
from referral.models import ReferralAudit  # Importiamo il modello ReferralAudit
from referral.forms import ReferralAuditForm
from django.contrib.auth.decorators import login_required

# LIST: Mostra tutte le trascrizioni
@login_required
def referral_audit_list(request):
    referral_audits = ReferralAudit.objects.all()
    return render(request, 'referral/referral_audit_list.html', {'referral_audits': referral_audits})

# DETAIL: Mostra il dettaglio di una trascrizione
@login_required
def referral_audit_detail(request, referral_audit_id):
    referral_audit = get_object_or_404(ReferralAudit, id=referral_audit_id)
    return render(request, 'referral/referral_audit_detail.html', {'referral_audit': referral_audit})

# CREATE: Crea una nuova trascrizione
@login_required
def create_referral_audit(request):
    if request.method == 'POST':
        form = ReferralAuditForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('referral/referral_audit_list')
    else:
        form = ReferralAuditForm()
    return render(request, 'referral/create_referral_audit.html', {'form': form})

# UPDATE: Modifica una trascrizione
@login_required
def update_referral_audit(request, referral_audit_id):
    referral_audit = get_object_or_404(ReferralAudit, id=referral_audit_id)
    if request.method == 'POST':
        form = ReferralAuditForm(request.POST, instance=referral_audit)
        if form.is_valid():
            form.save()
            return redirect('referral/referral_audit_detail', referral_audit_id=referral_audit_id)
    else:
        form = ReferralAuditForm(instance=referral_audit)
    return render(request, 'referral/update_referral_audit.html', {'form': form})

# DELETE: Elimina una trascrizione
@login_required
def delete_referral_audit(request, referral_audit_id):
    referral_audit = get_object_or_404(ReferralAudit, id=referral_audit_id)
    if request.method == 'POST':
        referral_audit.delete()
        return redirect('referral/referral_audit_list')
    return render(request, 'delete_referral_audit.html', {'referral_audit': referral_audit})
