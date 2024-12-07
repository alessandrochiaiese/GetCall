
from django.shortcuts import render
from django.urls import path 
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views.generic import CreateView


class SignUpView(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy("login")
    template_name = "accounts/registration/signup.html"
    
# View per visualizzare la lista di ruoli
def role_list_view(request):
    return render(request, 'accounts/role_list.html')

# View per visualizzare la lista di ruoli
def role_list_view(request):
    return render(request, 'accounts/role_list.html')

# View per visualizzare i dettagli di un ruolo specifico
def role_detail_view(request, pk):
    return render(request, 'accounts/role_detail.html', {'role_id': pk})


# View per visualizzare la lista dei utenti
def user_list_view(request):
    return render(request, 'accounts/user_list.html')

# View per visualizzare i dettagli di un utente specifico
def user_detail_view(request, pk):
    return render(request, 'accounts/user_detail.html', {'user_id': pk})
 