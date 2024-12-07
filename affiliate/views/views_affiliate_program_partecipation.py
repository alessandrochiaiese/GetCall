from django.shortcuts import render, get_object_or_404, redirect
from affiliate.models import AffiliateProgramPartecipation  # Importiamo il modello AffiliateProgramPartecipation
from affiliate.forms import AffiliateProgramPartecipationForm
from django.contrib.auth.decorators import login_required

# LIST: Mostra tutte le trascrizioni
@login_required
def affiliate_program_partecipation_list(request):
    affiliate_program_partecipations = AffiliateProgramPartecipation.objects.all()
    return render(request, 'affiliate/affiliate_program_partecipation_list.html', {'affiliate_program_partecipations': affiliate_program_partecipations})

# DETAIL: Mostra il dettaglio di una trascrizione
@login_required
def affiliate_program_partecipation_detail(request, affiliate_program_partecipation_id):
    affiliate_program_partecipation = get_object_or_404(AffiliateProgramPartecipation, id=affiliate_program_partecipation_id)
    return render(request, 'affiliate/affiliate_program_partecipation_detail.html', {'affiliate_program_partecipation': affiliate_program_partecipation})

# CREATE: Crea una nuova trascrizione
@login_required
def create_affiliate_program_partecipation(request):
    if request.method == 'POST':
        form = AffiliateProgramPartecipationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('affiliate/affiliate_program_partecipation_list')
    else:
        form = AffiliateProgramPartecipationForm()
    return render(request, 'affiliate/create_affiliate_program_partecipation.html', {'form': form})

# UPDATE: Modifica una trascrizione
@login_required
def update_affiliate_program_partecipation(request, affiliate_program_partecipation_id):
    affiliate_program_partecipation = get_object_or_404(AffiliateProgramPartecipation, id=affiliate_program_partecipation_id)
    if request.method == 'POST':
        form = AffiliateProgramPartecipationForm(request.POST, instance=affiliate_program_partecipation)
        if form.is_valid():
            form.save()
            return redirect('affiliate/affiliate_program_partecipation_detail', affiliate_program_partecipation_id=affiliate_program_partecipation_id)
    else:
        form = AffiliateProgramPartecipationForm(instance=affiliate_program_partecipation)
    return render(request, 'affiliate/update_affiliate_program_partecipation.html', {'form': form})

# DELETE: Elimina una trascrizione
@login_required
def delete_affiliate_program_partecipation(request, affiliate_program_partecipation_id):
    affiliate_program_partecipation = get_object_or_404(AffiliateProgramPartecipation, id=affiliate_program_partecipation_id)
    if request.method == 'POST':
        affiliate_program_partecipation.delete()
        return redirect('affiliate/affiliate_program_partecipation_list')
    return render(request, 'delete_affiliate_program_partecipation.html', {'affiliate_program_partecipation': affiliate_program_partecipation})
