from django.shortcuts import render, get_object_or_404, redirect
from affiliate.models import AffiliateAudit  # Importiamo il modello AffiliateAudit
from affiliate.forms import AffiliateAuditForm
from django.contrib.auth.decorators import login_required

# LIST: Mostra tutte le trascrizioni
@login_required
def affiliate_audit_list(request):
    affiliate_audits = AffiliateAudit.objects.all()
    return render(request, 'affiliate/affiliate_audit_list.html', {'affiliate_audits': affiliate_audits})

# DETAIL: Mostra il dettaglio di una trascrizione
@login_required
def affiliate_audit_detail(request, affiliate_audit_id):
    affiliate_audit = get_object_or_404(AffiliateAudit, id=affiliate_audit_id)
    return render(request, 'affiliate/affiliate_audit_detail.html', {'affiliate_audit': affiliate_audit})

# CREATE: Crea una nuova trascrizione
@login_required
def create_affiliate_audit(request):
    if request.method == 'POST':
        form = AffiliateAuditForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('affiliate/affiliate_audit_list')
    else:
        form = AffiliateAuditForm()
    return render(request, 'affiliate/create_affiliate_audit.html', {'form': form})

# UPDATE: Modifica una trascrizione
@login_required
def update_affiliate_audit(request, affiliate_audit_id):
    affiliate_audit = get_object_or_404(AffiliateAudit, id=affiliate_audit_id)
    if request.method == 'POST':
        form = AffiliateAuditForm(request.POST, instance=affiliate_audit)
        if form.is_valid():
            form.save()
            return redirect('affiliate/affiliate_audit_detail', affiliate_audit_id=affiliate_audit_id)
    else:
        form = AffiliateAuditForm(instance=affiliate_audit)
    return render(request, 'affiliate/update_affiliate_audit.html', {'form': form})

# DELETE: Elimina una trascrizione
@login_required
def delete_affiliate_audit(request, affiliate_audit_id):
    affiliate_audit = get_object_or_404(AffiliateAudit, id=affiliate_audit_id)
    if request.method == 'POST':
        affiliate_audit.delete()
        return redirect('affiliate/affiliate_audit_list')
    return render(request, 'delete_affiliate_audit.html', {'affiliate_audit': affiliate_audit})
