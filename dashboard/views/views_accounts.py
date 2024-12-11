
from django.shortcuts import redirect
from django.views.generic import TemplateView 
from django.contrib.auth.views import LoginView, PasswordResetView, PasswordChangeView
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth import login, logout
from django.contrib.auth.views import LoginView, PasswordResetView, PasswordChangeView
from django.views import View
from django.views.generic import TemplateView
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy 
from django.utils.crypto import get_random_string 
from referral.models import *
from referral.forms import *
from referral.models.referral import Referral
from referral.models.referral_code import ReferralCode  
from dashboard.forms import * 


#####################
# Register & Login  #
#####################
class ReferralRedirectView(View):
    def get(self, request, *args, **kwargs):
        referral_code = kwargs.get('referral_code') #path('referral/<str:referral_code>/')
        #referral_code = request.GET.get('referral_code') #path('referral/')

        # Verifica che il codice referral esista
        try:
            referral = ReferralCode.objects.get(code=referral_code, status='active')
            # Redirect alla vista di registrazione, passando il codice referral come parte dell'URL
            return redirect(reverse('core_register_with_referral', args=[referral_code]))
        except ReferralCode.DoesNotExist:
            # Se il codice referral non è valido, reindirizza ad una pagina di errore o alla home
            return redirect('/')

class RegisterView(View):
    form_class = RegisterForm
    initial = {'key': 'value'}
    template_name = 'core/register.html'
    success_url = '/login/'  # Dopo il successo della registrazione, reindirizza alla pagina di login
 
    def dispatch(self, request, *args, **kwargs):
        # will redirect to the home page if a user tries to access the register page while logged in
        if request.user.is_authenticated:
            return redirect(to='/')

        # else process dispatch as it otherwise normally would
        return super(RegisterView, self).dispatch(request, *args, **kwargs)

    """def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {'form': form})"""

    def get(self, request, *args, **kwargs):
        referral_code_used = kwargs.get('referral_code')  # Codice referral da URL
        form = self.form_class(initial=self.initial)

        if referral_code_used:
            try:
                referral_code = ReferralCode.objects.get(code=referral_code_used, status="active")
                print(form.fields)
                #form.fields['username'].initial = referral_code.user.username
                #form.fields['referral_code'].initial = referral_code.code
            except ReferralCode.DoesNotExist:
                messages.warning(request, 'Il codice referral non è valido.')

        return render(request, self.template_name, {'form': form})
    
    def post(self, request, *args, **kwargs):        
        # Estrai referral_code direttamente dai kwargs, dato che è passato come parte dell'URL
        referral_code_used = kwargs.get('referral_code', None)  # Codice referral passato nel percorso URL
        print('Referral code from URL:', referral_code_used)

        form = self.form_class(request.POST)
        #referral_code_used = request.GET.get('referral_code')  # Codice referral passato come query param (se esiste)
        #print('referral_code_used',referral_code_used)
        
        if form.is_valid():
            user = form.save()
            referrer_code = None

            # Se il nuovo utente ha usato un codice referral
            if referral_code_used is not None:
                try:
                    # Recupera il codice referral del referrer
                    referrer_code = ReferralCode.objects.filter(code=referral_code_used, status="active").first()
                    if referrer_code:
                        print(f"Referral code found: {referrer_code.code}")
                    else:
                        print(f"No active referral code found for {referral_code_used}")

                    print(f"Referral code found: {referrer_code.code}")
                    referrer = referrer_code.user  # Assuming you have the referrer from the referral code.
                    
                    referral = None
                    if Referral.objects.filter(referrer=referrer).exists():
                        # If a referral record for this user already exists, you can handle it as needed.
                        # You could raise an error or return early, depending on your business logic.
                        print(f"Referral already exists for {referrer.username}")
                        referral = Referral.objects.filter(referrer=referrer).first()
                        referral.referred.add(user)
                    else:
                        # If no referral exists for this user, proceed to create a new referral.
                        referral = Referral.objects.create(
                            program=None,  # referrer_code.program,
                            referrer=referrer,
                            #referred=user,
                            reward_given=False
                        )
                        referral.referred.add(user)
                        # Add the referred users to the referral record
                        #if user not in referral.referred.all(): referral.referred.add(user)  # Solo se l'utente non è già referenziato # Add the referred user (assuming `user` is the referred user)
                        #print(f"Referral created for {referrer.username}")
                    
                    print("Referral created successfully")
                    # Aggiorna il conteggio degli utenti invitati
                    referrer_code.referred_user_count += 1
                    referrer_code.save()

                    messages.success(
                        request,
                        f"Registrazione completata! Sei stato invitato da {referrer_code.user.username}."
                    )

                except ReferralCode.DoesNotExist:
                    # Se il codice non è valido, mostra un messaggio di avvertimento
                    messages.warning(request, 'Il codice referral utilizzato non è valido. Registrazione completata senza referral.')
            else:
                # Messaggio di successo standard se nessun referral è stato usato
                messages.success(request, 'Registrazione completata! Benvenuto.')


            # Creazione del codice referral per il nuovo utente
            code = get_random_string(length=8).upper()
            campaign_source = request.POST.get('campaign_source')
            campaign_medium = request.POST.get('campaign_medium')

            # Ensure that 'campaign_source' is not None or empty
            if not campaign_source:
                campaign_source = 'default_campaign_source'  # You can use a default value or raise an error
            if not campaign_source:
                campaign_medium = 'default_campaign_medium'  # You can use a default value or raise an error

            referral_code = ReferralCode.objects.create(
                user=user,
                code=code,
                usage_count=0,
                status="active",
                referred_user_count=0,
                expiry_date=request.POST.get('expiry_date'),
                unique_url=request.build_absolute_uri("/referral-code/" + code + "/"), # request.get_host() + '/referral-code/' + code + '/'#,
                #campaign_source=campaign_source,  # Now we ensure it's not None
                #campaign_medium=campaign_medium
            )


            return redirect(to='core_login')

        return render(request, self.template_name, {'form': form})


# Class based view that extends from the built in login view to add a remember me functionality
class CustomLoginView(LoginView):
    form_class = LoginForm
    template_name = 'core/login.html'

    def form_valid(self, form):
        remember_me = form.cleaned_data.get('remember_me')

        if not remember_me:
            # set session expiry to 0 seconds. So it will automatically close the session after the browser is closed.
            self.request.session.set_expiry(0)

            # Set session as modified to force data updates/cookie to be saved.
            self.request.session.modified = True

        # login() is needed to ensure the session is saved
        login(self.request, form.get_user())
        
        # else browser session will be as long as the session cookie time "SESSION_COOKIE_AGE" defined in settings.py
        return super(CustomLoginView, self).form_valid(form)


class ResetPasswordView(SuccessMessageMixin, PasswordResetView):
    template_name = 'core/password_reset.html'
    email_template_name = 'core/password_reset_email.html'
    subject_template_name = 'core/password_reset_subject.html'
    success_message = "We've emailed you instructions for setting your password, " \
                      "if an account exists with the email you entered. You should receive them shortly." \
                      " If you don't receive an email, " \
                      "please make sure you've entered the address you registered with, and check your spam folder."
    success_url = reverse_lazy('core_home')


class ChangePasswordView(SuccessMessageMixin, PasswordChangeView):
    template_name = 'core/change_password.html'
    success_message = "Successfully Changed Your Password"
    success_url = reverse_lazy('core_home')



class LandingPageView(TemplateView):
    template_name = 'core/landing_page.html'
    

    
def custom_logout(request):
    logout(request)  # Invalidiamo la sessione dell'utente
    return redirect('core_home')  # Redirigi alla home (o a qualsiasi altra pagina)
