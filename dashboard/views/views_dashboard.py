
from django.http import JsonResponse
from django.views import View
from django.views.generic import TemplateView 
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from dashboard.models.profile import Profile  
from dashboard.utils import calculate_user_level, get_tree_referred, tree_to_list
from referral.models.referral import Referral
from referral.models.referral_code import ReferralCode 
  
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required 
from django.views.generic import TemplateView 
from django.utils.decorators import method_decorator 
from referral.models import *
from referral.forms import *
from dashboard.forms import * 
 

User = get_user_model()

@method_decorator(login_required, name='dispatch')
class HomeView(TemplateView):
    model = get_user_model()  # Usa il modello User di default
    template_name = 'dashboard/index.html'

    def get_object(self, queryset=None):
        # Ritorna l'oggetto corrispondente all'utente autenticato
        return self.request.user
    
    
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
    
@method_decorator(login_required, name='dispatch')
class MasterAccountsView(TemplateView):
    model = get_user_model()  # Usa il modello User di default
    template_name = 'dashboard/referred_accounts/master_accounts.html'

    def get_object(self, queryset=None):
        # Ritorna l'oggetto corrispondente all'utente autenticato
        return self.request.user
    
    
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
    
@method_decorator(login_required, name='dispatch')
class InvestorAccountsView(TemplateView):
    model = get_user_model()  # Usa il modello User di default
    template_name = 'dashboard/referred_accounts/investor_accounts.html'

    def get_object(self, queryset=None):
        # Ritorna l'oggetto corrispondente all'utente autenticato
        return self.request.user
    
    
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
        
        investor_accounts = []
        for referred_item in list_referred:
            referred_id = referred_item.get('id')
            referred_user = User.objects.filter(user=referred_id).first()
            referred = Profile.objects.filter(user=referred_user).first()
            profile = None
            transactions = ReferralTransaction.objects.filter(referred_user=referred)
            if len(transactions)>0:
                investor_accounts.append(referred_item)
        print(tree_referred)
        print(list_referred)
        print(investor_accounts)
        context['investor_accounts'] = investor_accounts
        
        return context
    
@method_decorator(login_required, name='dispatch')
class IncompleteRegistrationsView(TemplateView):
    model = get_user_model()  # Usa il modello User di default
    template_name = 'dashboard/referred_accounts/incomplete_registrations.html'

    def get_object(self, queryset=None):
        # Ritorna l'oggetto corrispondente all'utente autenticato
        return self.request.user
    
    
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
        
        incomplete_registrations = []
        for referred_item in list_referred:
            referred_id = referred_item.get('id')
            referred_user = User.objects.filter(user=referred_id).first()
            referred = Profile.objects.filter(user=referred_user).first()
            profile = None
            profile = Profile.objects.filter(user=referred).first()
            if not profile or \
                profile.birth_date == None or \
                profile.city == None or \
                profile.street == None or \
                profile.CAP == None or \
                profile.phone_number == None or \
                profile.is_business == False or \
                profile.is_buyer == False:
                incomplete_registrations.append(referred_item)
        print(tree_referred)
        print(list_referred)
        print(incomplete_registrations)
        context['incomplete_registrations'] = incomplete_registrations
        
        return context
    
@method_decorator(login_required, name='dispatch')
class MyIBsView(TemplateView):
    model = get_user_model()  # Usa il modello User di default
    template_name = 'dashboard/my_ibs.html'

    def get_object(self, queryset=None):
        # Ritorna l'oggetto corrispondente all'utente autenticato
        return self.request.user
    
    
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
        
        investor_accounts = []
        for referred_item in list_referred:
            referred_id = referred_item.get('id')
            referred_user = User.objects.filter(user=referred_id).first()
            referred = Profile.objects.filter(user=referred_user).first()
            profile = None
            transactions = ReferralTransaction.objects.filter(referred_user=referred)
            if len(transactions)>0:
                investor_accounts.append(referred_item)
        print(tree_referred)
        print(list_referred)
        print(investor_accounts)
        context['my_ibs'] = list(set([*investor_accounts, *referreds]))
        
        return context
    
class WithdrawalView(TemplateView):
    template_name = 'dashboard/withdrawals.html'


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
