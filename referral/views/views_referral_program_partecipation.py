from django.shortcuts import render, get_object_or_404, redirect
from referral.models import ReferralProgramPartecipation  # Importiamo il modello ReferralProgramPartecipation
from referral.forms import ReferralProgramPartecipationForm
from django.contrib.auth.decorators import login_required

# LIST: Mostra tutte le trascrizioni
@login_required
def referral_program_partecipation_list(request):
    referral_program_partecipations = ReferralProgramPartecipation.objects.all()
    return render(request, 'referral/referral_program_partecipation_list.html', {'referral_program_partecipations': referral_program_partecipations})

# DETAIL: Mostra il dettaglio di una trascrizione
@login_required
def referral_program_partecipation_detail(request, referral_program_partecipation_id):
    referral_program_partecipation = get_object_or_404(ReferralProgramPartecipation, id=referral_program_partecipation_id)
    return render(request, 'referral/referral_program_partecipation_detail.html', {'referral_program_partecipation': referral_program_partecipation})

# CREATE: Crea una nuova trascrizione
@login_required
def create_referral_program_partecipation(request):
    if request.method == 'POST':
        form = ReferralProgramPartecipationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('referral/referral_program_partecipation_list')
    else:
        form = ReferralProgramPartecipationForm()
    return render(request, 'referral/create_referral_program_partecipation.html', {'form': form})

# UPDATE: Modifica una trascrizione
@login_required
def update_referral_program_partecipation(request, referral_program_partecipation_id):
    referral_program_partecipation = get_object_or_404(ReferralProgramPartecipation, id=referral_program_partecipation_id)
    if request.method == 'POST':
        form = ReferralProgramPartecipationForm(request.POST, instance=referral_program_partecipation)
        if form.is_valid():
            form.save()
            return redirect('referral/referral_program_partecipation_detail', referral_program_partecipation_id=referral_program_partecipation_id)
    else:
        form = ReferralProgramPartecipationForm(instance=referral_program_partecipation)
    return render(request, 'referral/update_referral_program_partecipation.html', {'form': form})

# DELETE: Elimina una trascrizione
@login_required
def delete_referral_program_partecipation(request, referral_program_partecipation_id):
    referral_program_partecipation = get_object_or_404(ReferralProgramPartecipation, id=referral_program_partecipation_id)
    if request.method == 'POST':
        referral_program_partecipation.delete()
        return redirect('referral/referral_program_partecipation_list')
    return render(request, 'delete_referral_program_partecipation.html', {'referral_program_partecipation': referral_program_partecipation})
