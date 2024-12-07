from django.shortcuts import render, get_object_or_404, redirect
from affiliate.models import AffiliateSupportTicket  # Importiamo il modello AffiliateSupportTicket
from affiliate.forms import AffiliateSupportTicketForm
from django.contrib.auth.decorators import login_required

# LIST: Mostra tutte le trascrizioni
@login_required
def affiliate_support_ticket_list(request):
    affiliate_support_tickets = AffiliateSupportTicket.objects.all()
    return render(request, 'affiliate/affiliate_support_ticket_list.html', {'affiliate_support_tickets': affiliate_support_tickets})

# DETAIL: Mostra il dettaglio di una trascrizione
@login_required
def affiliate_support_ticket_detail(request, affiliate_support_ticket_id):
    affiliate_support_ticket = get_object_or_404(AffiliateSupportTicket, id=affiliate_support_ticket_id)
    return render(request, 'affiliate/affiliate_support_ticket_detail.html', {'affiliate_support_ticket': affiliate_support_ticket})

# CREATE: Crea una nuova trascrizione
@login_required
def create_affiliate_support_ticket(request):
    if request.method == 'POST':
        form = AffiliateSupportTicketForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('affiliate/affiliate_support_ticket_list')
    else:
        form = AffiliateSupportTicketForm()
    return render(request, 'affiliate/create_affiliate_support_ticket.html', {'form': form})

# UPDATE: Modifica una trascrizione
@login_required
def update_affiliate_support_ticket(request, affiliate_support_ticket_id):
    affiliate_support_ticket = get_object_or_404(AffiliateSupportTicket, id=affiliate_support_ticket_id)
    if request.method == 'POST':
        form = AffiliateSupportTicketForm(request.POST, instance=affiliate_support_ticket)
        if form.is_valid():
            form.save()
            return redirect('affiliate/affiliate_support_ticket_detail', affiliate_support_ticket_id=affiliate_support_ticket_id)
    else:
        form = AffiliateSupportTicketForm(instance=affiliate_support_ticket)
    return render(request, 'affiliate/update_affiliate_support_ticket.html', {'form': form})

# DELETE: Elimina una trascrizione
@login_required
def delete_affiliate_support_ticket(request, affiliate_support_ticket_id):
    affiliate_support_ticket = get_object_or_404(AffiliateSupportTicket, id=affiliate_support_ticket_id)
    if request.method == 'POST':
        affiliate_support_ticket.delete()
        return redirect('affiliate/affiliate_support_ticket_list')
    return render(request, 'delete_affiliate_support_ticket.html', {'affiliate_support_ticket': affiliate_support_ticket})
