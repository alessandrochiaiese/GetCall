
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth import login, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, PasswordResetView, PasswordChangeView
from django.db.models import Sum
from django.db.models import Count  
from django.http import JsonResponse
from django.views import View
from django.views.generic import TemplateView, DetailView
from django.views.generic.edit import UpdateView 
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.utils import timezone
from django.utils.crypto import get_random_string
from django.utils.decorators import method_decorator 
from referral.models import *
from referral.forms import *
from core.forms import *
from getcall.settings import HOSTNAME
 

User = get_user_model()

class HomeView(TemplateView):
    template_name = 'core/home.html'


class LandingPageView(TemplateView):
    template_name = 'core/landing_page.html'
 
#####################
# Original Commented#
#####################
"""
class RegisterView(View):
    form_class = RegisterForm
    initial = {'key': 'value'}
    template_name = 'core/register.html'
    success_url = '/login/'  # Dopo il successo della registrazione, reindirizza alla pagina di login

    def dispatch(self, request, *args, **kwargs):
        # Redirect to home if user is already logged in
        if request.user.is_authenticated:
            return redirect(to='/')

        return super(RegisterView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        referral_code_used = request.GET.get('referral_code')  # Codice referral passato come query param (se esiste)

        if form.is_valid():
            user = form.save()

            # Creazione del codice referral per il nuovo utente
            referral_code = get_random_string(length=8).upper()
            ReferralCode.objects.create(
                user=user,
                code=referral_code,
                usage_count=0,
                status="active",
                referred_user_count=0,
                date_created=timezone.now()
            )

            # Se il nuovo utente ha usato un codice referral
            if referral_code_used:
                try:
                    # Recupera il codice referral del referrer
                    referrer_code = ReferralCode.objects.get(code=referral_code_used, status="active")

                    # Registra il referral nella tabella Referral
                    Referral.objects.create(
                        program=referrer_code.program,
                        referrer=referrer_code.user,
                        referred=user,
                        reward_given=False
                    )

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

            return redirect(to='core_login')

        return render(request, self.template_name, {'form': form})
"""

"""class ProfileView(UpdateView):
    model = get_user_model()  # Usa il modello User di default
    form_class = UpdateUserForm
    template_name = 'core/profile.html'
    success_url = reverse_lazy('core_profile')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile_form'] = UpdateProfileForm(instance=self.request.user.profile)
        return context

    def form_valid(self, form):
        # Gestisce la parte relativa al profilo separatamente
        profile_form = UpdateProfileForm(self.request.POST, self.request.FILES, instance=self.request.user.profile)
        if profile_form.is_valid():
            profile_form.save()
            messages.success(self.request, 'Your profile is updated successfully')

        return super().form_valid(form)
"""

"""
@method_decorator(login_required, name='dispatch')
class ProfileView(UpdateView):
    model = get_user_model()  # Usa il modello User di default
    form_class = UpdateUserForm
    template_name = 'core/profile.html'
    success_url = reverse_lazy('core_profile')

    def get_object(self, queryset=None):
        # Ritorna l'oggetto corrispondente all'utente autenticato
        return self.request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile_form'] = UpdateProfileForm(instance=self.request.user.profile)
        return context

    def form_valid(self, form):
        # Gestisce la parte relativa al profilo separatamente
        profile_form = UpdateProfileForm(self.request.POST, self.request.FILES, instance=self.request.user.profile)
        
        if not profile_form.is_valid():
            # Se il form del profilo non è valido, ritorna un errore
            messages.error(self.request, 'There was an error updating your profile.')
            return self.form_invalid(form)

        # Salva entrambi i form
        form.save()  # Salva i dati utente
        profile_form.save()  # Salva i dati del profilo

        # Messaggio di successo
        messages.success(self.request, 'Your profile and account information were updated successfully.')
        return super().form_valid(form)
"""


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
                unique_url=request.get_host() + '/referral-code/' + code + '/'#,
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

@method_decorator(login_required, name='dispatch')
class ProfileView(UpdateView):
    model = get_user_model()  # Usa il modello User di default
    form_class = UpdateUserForm
    template_name = 'core/profile.html'
    success_url = reverse_lazy('core_profile')

    def get_object(self, queryset=None):
        # Ritorna l'oggetto corrispondente all'utente autenticato
        return self.request.user

    """def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        profile = Profile.objects.filter(user=self.request.user).first()
        referral_code = ReferralCode.objects.filter(user=self.request.user).first()
        referral = Referral.objects.filter(referred=self.request.user).first()
        referrer = None
        try:
            referrer = ReferralCode.objects.filter(user=referral.referrer).first()
        except Exception:
            referrer = None
            
        if referrer:
            referrer_code = referrer.code
        else:
            referrer_code = None

        # Recupera il form del profilo
        context['profile_form'] = UpdateProfileForm(instance=profile)

        # Recupera il codice referral dell'utente
        try: 
            context['referral_code'] = referral_code.code
        except AttributeError:
            context['referral_code'] = None
        try: 
            context['referrer_code'] = referrer_code
        except AttributeError:
            context['referrer_code'] = None

        # Recupera gli utenti invitati dall'utente autenticato
        context['referrals'] = Referral.objects.filter(referrer=self.request.user)

        return context

    """
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Get the user 
        user=self.request.user#user = User.objects.filter(user=self.request.user).first()

        # Get the user's profile
        profile = Profile.objects.filter(user=user).first()

        # Get the referral code for the user
        referral_code = ReferralCode.objects.filter(user=user).first()
 
        # Get the user's referral information
        try:
            referral = Referral.objects.filter(referrer=user).first()
        except Exception:
            referrer = None

        referrer = None
        referrer_code = None
        # Get the referral code for the referrer
        try:
            referrer = ReferralCode.objects.filter(user=referral.referrer).first()
        except Exception:
            referrer = None

        # If the referrer exists, get the referrer code
        if referrer:
            referrer_code = referrer.code
        else:
            referrer_code = None

        # Add the profile form to the context
        context['profile_form'] = UpdateProfileForm(instance=profile)

        # Add the referral code to the context
        try: 
            context['referral_code'] = referral_code.code
        except AttributeError:
            context['referral_code'] = None
        
        # Add the referrer code to the context
        try: 
            context['referrer_code'] = referrer_code
        except AttributeError:
            context['referrer_code'] = None

        
        # Retrieve all referrals made by the logged-in user
        referred_users = []

        referral = None
        try:
            # Recupera tutti i Referral dell'utente autenticato
            referral = Referral.objects.filter(referrer=user).first() 
            print(referral)
            
        except Exception:
            referrer = None
        
        if referral != None:
            # Itera sui Referral e aggiungi gli utenti collegati alla lista
            for referred in referral.referred.all():
                referred_users.append(referred)  # Usa .all() per ottenere gli oggetti collegati

            # Debug: Stampa gli utenti invitati
            print("Final referred users list:", referred_users)
            # Debug: Print the final list of referred users
            print("Final Referred Users:", referred_users)

            # Pass the referred users to the context
            context['referred_users'] = referred_users

        referreds = []
        tree_referred = get_tree_referred(user, level=0)
        list_referred = tree_to_list(tree_referred, referreds)
        
        print(tree_referred)
        print(list_referred)
        context['referred_leveled_users'] = list_referred
        
        return context
    
    def form_valid(self, form):
        user=self.request.user
        profile = Profile.objects.filter(user=user).first()
        # Gestisce la parte relativa al profilo separatamente
        profile_form = UpdateProfileForm(self.request.POST, self.request.FILES, instance=profile)
        
        if not profile_form.is_valid():
            # Se il form del profilo non è valido, ritorna un errore
            messages.error(self.request, 'There was an error updating your profile.')
            return self.form_invalid(form)

        # Salva entrambi i form
        form.save()  # Salva i dati utente
        profile_form.save()  # Salva i dati del profilo

        # Messaggio di successo
        messages.success(self.request, 'Your profile and account information were updated successfully.')
        return super().form_valid(form)

@method_decorator(login_required, name='dispatch')
class UserProfileDataView(View):
    def get(self, request, *args, **kwargs):
        user = self.request.user
 
        
        # Dati generali di referral
        referral_data = {
            # Totale delle commissioni: supponendo che siano in ReferralTransaction o ReferralReward
            'total_commission': ReferralTransaction.objects.filter(referral_codes__user=user).aggregate(Sum('conversion_value'))['conversion_value__sum'] or 0,
            
            # Totale delle ricompense (bonus e premi)
            #'total_rewards': (ReferralBonus.objects.filter(user=user).aggregate(Sum('bonus_value'))['bonus_value__sum'] or 0) + 
            #                (ReferralReward.objects.filter(referred_user=user).aggregate(Sum('reward_value'))['reward_value__sum'] or 0),
            
            # Numero di referral attivi
            'active_referrals': Referral.objects.filter(referrer=user).count(),
            
            # Conversioni totali da ReferralConversion
            'total_conversions': ReferralConversion.objects.filter(referral_codes__user=user).count(),

            # Totale delle transazioni da ReferralTransaction
            'total_transactions': ReferralTransaction.objects.filter(referral_codes__user=user).aggregate(Sum('transaction_amount'))['transaction_amount__sum'] or 0,
        }


        # Dati per i codici referral
        referral_codes = ReferralCode.objects.filter(user=user).values('code', 'usage_count')

        # Dati per le campagne attive
        #active_campaigns = ReferralCampaign.objects.filter(is_active=True).values('id', 'campaign_name', 'start_date', 'end_date', 'goal', 'budget', 'spending_to_date', 'target_audience')

        # Statistiche dei referral
        referral_stats = list(ReferralStats.objects.filter(referral_codes__user=user).values('period', 'click_count', 'conversion_count', 'total_rewards', 'average_conversion_value', 'highest_referral_earning'))

        # Transazioni dei referral
        #referral_transactions = list(ReferralTransaction.objects.filter(referral_codes__in__referral_codes=referral_codes).values('referred_user', 'transaction_date', 'order_id', 'transaction_amount', 'currency', 'status', 'conversion_value', 'discount_value', 'coupon_code_used', 'channel'))

        # Audit dei referral
        recent_audits = list(ReferralAudit.objects.filter(user=user).values('referral_codes', 'action_taken', 'action_date', 'user', 'ip_address', 'device_info', 'location'))

        # Codice referral unico dell'utente
        referral_code = ReferralCode.objects.filter(user=user).first()

        data = {
            'referral_data': referral_data,
            'referral_codes': list(referral_codes),
            #'referral_campaigns': list(active_campaigns),
            'referral_stats': referral_stats,
            #'referral_transactions': referral_transactions, 
            'recent_audits': recent_audits,
            'referral_code': referral_code.code if referral_code else ''
        }

        return JsonResponse(data, status=200)
    

#####################
# Campaign          #
#####################
class ParticipateCampaignView(View):
    def post(self, request, *args, **kwargs):
        campaign_id = request.POST.get('campaign_id')
        try:
            campaign = ReferralCampaign.objects.get(id=campaign_id)

            # Logica per associare l'utente alla campagna (da implementare secondo le esigenze)
            # Ad esempio, associamo l'utente alla campagna

            return JsonResponse({'success': True})
        except ReferralCampaign.DoesNotExist:
            return JsonResponse({'success': False}, status=400)

#####################
# Hierarchy         #
#####################
def track_referral_code(referral_code, referred_user=None):
    try:
        referral = ReferralCode.objects.get(code=referral_code, status="active")

        # Creazione di una nuova conversione
        conversion = ReferralConversion.objects.create(
            referral_code=referral,
            referred_user=referred_user,
            conversion_date=timezone.now(),
            conversion_value=10,  # Valore arbitrario
            status="pending",
            reward_issued=False
        )

        # Aggiorna le statistiche del codice
        stats = ReferralStats.objects.get(referral_code=referral)
        stats.click_count += 1
        if referred_user:
            stats.conversion_count += 1
        stats.save()

        # Genera una reward se i criteri sono soddisfatti
        if stats.conversion_count >= referral.program.min_referral_count:
            ReferralReward.objects.create(
                referral_code=referral,
                referred_user=referred_user,
                reward_type=referral.program.reward_type,
                reward_value=referral.program.reward_value,
                date_awarded=timezone.now(),
                status="active"
            )

        return {"message": "Codice tracciato con successo.", "conversion_id": conversion.id}
    except ReferralCode.DoesNotExist:
        raise ValueError("Codice referral non trovato o non attivo.")
    except Exception as e:
        raise ValueError(f"Errore durante il tracking: {e}")
    
def get_referral_hierarchy(user, depth=0):
    referrals = Referral.objects.filter(referrer=user)
    hierarchy = []
    for referral in referrals:
        hierarchy.append({
            'user': referral.referred,
            'depth': depth,
            'children': get_referral_hierarchy(referral.referred, depth + 1)
        })
    return hierarchy

def get_user_table(request):
    #user = User.objects.get(user=request.user)
    referral = Referral.objects.filter(user=request.user).first()

    # Otteniamo tutti gli utenti
    users = User.objects.all()
    
    user_data = []
    for user in users:
        # Calcoliamo il livello dell'utente ricorsivamente
        level = calculate_user_level(user)

        user_data.append({
            "first_name": user.first_name,
            "last_name": user.last_name,
            "username": user.username,
            "level": level,
        })
    print(user_data)
    return JsonResponse(user_data, safe=False)

def calculate_user_level(user, depth=1, max_depth=5):
    """ Funzione ricorsiva per calcolare il livello di un utente. """
    if depth > max_depth:
        return 0  # Raggiunta la profondità massima

    referrals = Referral.objects.filter(referrer=user)  # Ottieni tutti i referrals per l'utente
    if not referrals.exists():
        return depth  # Se non ci sono altri referrals, siamo al livello massimo per questo ramo

    # Altrimenti, esplora i referrals in profondità
    max_level = 0
    for referral in referrals:
        for referred_user in referral.referred.all():
            current_level = calculate_user_level(referred_user, depth + 1, max_depth)
            max_level = max(max_level, current_level)  # Trova il livello massimo tra i referrals

    return max_level

class UserReferredLevelView(View):
    def get(self, request, *args, **kwargs):
        user=self.request.user

        # Ottieni il primo referral dell'utente
        if user.is_authenticated:
            referral = Referral.objects.filter(referrer=user).first()
        else: 
            referral = None

        if not referral:
            return JsonResponse({'error': 'No referrals found for this user'}, status=400)

        try:
            user_data = []

            # Itera su tutti gli utenti che sono stati referenziati direttamente da te
            for user in referral.referred.all():
                # Calcola il livello di ogni utente ricorsivamente
                level = calculate_user_level(user)

                user_to_add = {
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                    "username": user.username,
                    "level": level,
                }
                print(user_to_add)
                user_data.append(user_to_add)

            # Restituisci i dati dei tuoi invitati con il loro livello calcolato
            return JsonResponse(user_data, safe=False)

        except Referral.DoesNotExist:
            return JsonResponse({'error': 'Referral record not found'}, status=400)

def get_tree_referred(user, level=1):# -> dict: 
    tree = []

    # Interrompe la ricorsione se il livello supera 5
    if level > 5:
        return tree
    
    referral = None
    try:
        referral = Referral.objects.filter(referrer=user).first()
    except Exception as e:
        print(e)

    if referral is None:
        print(f"No referral found for user {user.username}")
        return tree

    for referred_user in referral.referred.all():
        print(f"Processing user: {referred_user.username}, Level: {level}")  # Debug
        user_to_add = {
            "first_name": referred_user.first_name,
            "last_name": referred_user.last_name,
            "username": referred_user.username,
            "date_joined": referred_user.date_joined,
            "level": level,
            "list_referred": get_tree_referred(referred_user, level+1)
        }
        tree.append(user_to_add)
     
    return tree

def tree_to_list(tree, _list=None):
    if _list is None:
        _list = []  # Inizializza una lista vuota se non è stata passata
    
    for leaf in tree:
        # Verifica che ogni 'leaf' sia un dizionario
        if isinstance(leaf, dict):
            user_to_add = {
                "first_name": leaf.get('first_name'),
                "last_name": leaf.get('last_name'),
                "username": leaf.get('username'),
                "date_joined": leaf.get('date_joined'),
                "level": leaf.get('level') +1 #max(1, leaf.get('level', 1))  # Valore minimo a 1
            }
            _list.append(user_to_add)

            # Se 'list_referred' esiste, continua ricorsivamente
            list_referred = leaf.get('list_referred', [])
            if list_referred:  # Verifica che ci siano utenti referiti
                tree_to_list(list_referred, _list)  # Chiamata ricorsiva per esplorare i livelli successivi
            #for referred in list_referred:
            #    tree_to_list(referred, _list)  # Chiamata ricorsiva per gli utenti successivi
        else:
            print(f"Warning: Expected a dict, but got {type(leaf)}")
    
    return _list



#####################
# Product and Order #
#####################
 
"""
def create_product(request):
    if request.method == "POST":
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('product_list')  # Redirect to the product list page
    else:
        form = ProductForm()
    return render(request, 'commerce/create_product.html', {'form': form})



def create_order(request):
    if request.method == "POST":
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save()
            # Optionally, calculate the total price here
            order.calculate_total_price()
            return redirect('order_detail', order_id=order.id)
    else:
        form = OrderForm()
    return render(request, 'commerce/create_order.html', {'form': form})



def add_item_to_order(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    if request.method == "POST":
        form = OrderItemForm(request.POST)
        if form.is_valid():
            order_item = form.save(commit=False)
            order_item.order = order
            order_item.save()
            order.calculate_total_price()  # Recalculate the total price of the order
            return redirect('order_detail', order_id=order.id)
    else:
        form = OrderItemForm()
    return render(request, 'commerce/add_item_to_order.html', {'form': form, 'order': order})
"""

from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from .models import Product
from .forms import ProductForm
from django.views.generic import ListView, DetailView

class ProductListView(ListView):
    model = Product  # Modello associato alla vista
    template_name = 'commerce/list_product.html'
    context_object_name = 'products'  # Nome del contesto passato al template
    paginate_by = 10  # Opzionale, per aggiungere la paginazione

    def get_queryset(self):
        queryset = super().get_queryset()
        # Aggiungi filtri personalizzati, se necessario
        return queryset.order_by('-created_at')  # Esempio: ordina per data di creazione

class ProductDetailView(DetailView):
    template_name = 'commerce/detail_product.html'

class ProductUpdateView(CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'commerce/ipdate_product.html'
    success_url = reverse_lazy('product_list')  # Redirige alla lista dei prodotti dopo il salvataggio

class ProductCreateView(CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'commerce/create_product.html'
    success_url = reverse_lazy('product_list')  # Redirige alla lista dei prodotti dopo il salvataggio

    def form_valid(self, form):
        # Puoi aggiungere logica personalizzata prima di salvare il form, se necessario
        return super().form_valid(form)

from django.urls import reverse
from django.views.generic.edit import CreateView
from .models import Order
from .forms import OrderForm

class OrderCreateView(CreateView):
    model = Order
    form_class = OrderForm
    template_name = 'commerce/create_order.html'

    def form_valid(self, form):
        # Aggiungi logica per il calcolo del totale dell'ordine
        order = form.save()
        order.calculate_total_price()
        return redirect('order_detail', order_id=order.id)

    def get_success_url(self):
        # Puoi anche usare un redirect dinamico come in questo caso
        return reverse('order_detail', kwargs={'order_id': self.object.id})

from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views.generic.edit import FormView
from .models import Order, OrderItem
from .forms import OrderItemForm

class AddItemToOrderView(FormView):
    form_class = OrderItemForm
    template_name = 'commerce/add_item_to_order.html'

    def dispatch(self, request, *args, **kwargs):
        self.order = get_object_or_404(Order, id=kwargs['order_id'])
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        order_item = form.save(commit=False)
        order_item.order = self.order
        order_item.save()
        
        # Ricalcola il prezzo totale dell'ordine
        self.order.calculate_total_price()

        return redirect('order_detail', order_id=self.order.id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['order'] = self.order
        return context


from django.shortcuts import redirect
from django.contrib.auth import logout

def custom_logout(request):
    logout(request)  # Invalidiamo la sessione dell'utente
    return redirect('core_home')  # Redirigi alla home (o a qualsiasi altra pagina)
