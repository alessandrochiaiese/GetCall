from django.shortcuts import render, get_object_or_404, redirect
from affiliate.models import AffiliateLink  # Importiamo il modello AffiliateLink
from affiliate.forms import AffiliateLinkForm
from django.contrib.auth.decorators import login_required

# LIST: Mostra tutte le trascrizioni
@login_required
def affiliate_link_list(request):
    affiliate_links = AffiliateLink.objects.all()
    return render(request, 'affiliate/affiliate_link_list.html', {'affiliate_links': affiliate_links})

# DETAIL: Mostra il dettaglio di una trascrizione
@login_required
def affiliate_link_detail(request, affiliate_link_id):
    affiliate_link = get_object_or_404(AffiliateLink, id=affiliate_link_id)
    return render(request, 'affiliate/affiliate_link_detail.html', {'affiliate_link': affiliate_link})

# CREATE: Crea una nuova trascrizione
@login_required
def create_affiliate_link(request):
    if request.method == 'POST':
        form = AffiliateLinkForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('affiliate/affiliate_link_list')
    else:
        form = AffiliateLinkForm()
    return render(request, 'affiliate/create_affiliate_link.html', {'form': form})

# UPDATE: Modifica una trascrizione
@login_required
def update_affiliate_link(request, affiliate_link_id):
    affiliate_link = get_object_or_404(AffiliateLink, id=affiliate_link_id)
    if request.method == 'POST':
        form = AffiliateLinkForm(request.POST, instance=affiliate_link)
        if form.is_valid():
            form.save()
            return redirect('affiliate/affiliate_link_detail', affiliate_link_id=affiliate_link_id)
    else:
        form = AffiliateLinkForm(instance=affiliate_link)
    return render(request, 'affiliate/update_affiliate_link.html', {'form': form})

# DELETE: Elimina una trascrizione
@login_required
def delete_affiliate_link(request, affiliate_link_id):
    affiliate_link = get_object_or_404(AffiliateLink, id=affiliate_link_id)
    if request.method == 'POST':
        affiliate_link.delete()
        return redirect('affiliate/affiliate_link_list')
    return render(request, 'delete_affiliate_link.html', {'affiliate_link': affiliate_link})
