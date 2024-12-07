from django.shortcuts import render, get_object_or_404, redirect
from affiliate.models import AffiliateProgram  # Importiamo il modello AffiliateProgram
from affiliate.forms import AffiliateProgramForm
from django.contrib.auth.decorators import login_required

# LIST: Mostra tutte le trascrizioni
@login_required
def affiliate_program_list(request):
    affiliate_programs = AffiliateProgram.objects.all()
    return render(request, 'affiliate/affiliate_program_list.html', {'affiliate_programs': affiliate_programs})

# DETAIL: Mostra il dettaglio di una trascrizione
@login_required
def affiliate_program_detail(request, affiliate_program_id):
    affiliate_program = get_object_or_404(AffiliateProgram, id=affiliate_program_id)
    return render(request, 'affiliate/affiliate_program_detail.html', {'affiliate_program': affiliate_program})

# CREATE: Crea una nuova trascrizione
@login_required
def create_affiliate_program(request):
    if request.method == 'POST':
        form = AffiliateProgramForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('affiliate/affiliate_program_list')
    else:
        form = AffiliateProgramForm()
    return render(request, 'affiliate/create_affiliate_program.html', {'form': form})

# UPDATE: Modifica una trascrizione
@login_required
def update_affiliate_program(request, affiliate_program_id):
    affiliate_program = get_object_or_404(AffiliateProgram, id=affiliate_program_id)
    if request.method == 'POST':
        form = AffiliateProgramForm(request.POST, instance=affiliate_program)
        if form.is_valid():
            form.save()
            return redirect('affiliate/affiliate_program_detail', affiliate_program_id=affiliate_program_id)
    else:
        form = AffiliateProgramForm(instance=affiliate_program)
    return render(request, 'affiliate/update_affiliate_program.html', {'form': form})

# DELETE: Elimina una trascrizione
@login_required
def delete_affiliate_program(request, affiliate_program_id):
    affiliate_program = get_object_or_404(AffiliateProgram, id=affiliate_program_id)
    if request.method == 'POST':
        affiliate_program.delete()
        return redirect('affiliate/affiliate_program_list')
    return render(request, 'delete_affiliate_program.html', {'affiliate_program': affiliate_program})
