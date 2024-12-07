from django.shortcuts import render, get_object_or_404, redirect
from referral.models import ReferralProgram  # Importiamo il modello ReferralProgram
from referral.forms import ReferralProgramForm
from django.contrib.auth.decorators import login_required

# LIST: Mostra tutte le trascrizioni
@login_required
def referral_program_list(request):
    referral_programs = ReferralProgram.objects.all()
    return render(request, 'referral/referral_program_list.html', {'referral_programs': referral_programs})

# DETAIL: Mostra il dettaglio di una trascrizione
@login_required
def referral_program_detail(request, referral_program_id):
    referral_program = get_object_or_404(ReferralProgram, id=referral_program_id)
    return render(request, 'referral/referral_program_detail.html', {'referral_program': referral_program})

# CREATE: Crea una nuova trascrizione
@login_required
def create_referral_program(request):
    if request.method == 'POST':
        form = ReferralProgramForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('referral/referral_program_list')
    else:
        form = ReferralProgramForm()
    return render(request, 'referral/create_referral_program.html', {'form': form})

# UPDATE: Modifica una trascrizione
@login_required
def update_referral_program(request, referral_program_id):
    referral_program = get_object_or_404(ReferralProgram, id=referral_program_id)
    if request.method == 'POST':
        form = ReferralProgramForm(request.POST, instance=referral_program)
        if form.is_valid():
            form.save()
            return redirect('referral/referral_program_detail', referral_program_id=referral_program_id)
    else:
        form = ReferralProgramForm(instance=referral_program)
    return render(request, 'referral/update_referral_program.html', {'form': form})

# DELETE: Elimina una trascrizione
@login_required
def delete_referral_program(request, referral_program_id):
    referral_program = get_object_or_404(ReferralProgram, id=referral_program_id)
    if request.method == 'POST':
        referral_program.delete()
        return redirect('referral/referral_program_list')
    return render(request, 'delete_referral_program.html', {'referral_program': referral_program})
