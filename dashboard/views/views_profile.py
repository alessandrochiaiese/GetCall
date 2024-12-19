
from django.http import JsonResponse 
from django.db.models import Sum
from django.shortcuts import redirect
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views import View 
from django.views.generic.edit import UpdateView 
from dashboard.utils import get_tree_referred, tree_to_list
from referral.models import *
from referral.forms import *
from referral.models.referral import Referral
from referral.models.referral_code import ReferralCode  
from dashboard.forms import * 

#####################
# Profile           #
#####################
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

        # Get the user
        user = self.request.user

        # Get the user's profile
        profile = Profile.objects.filter(user=user).first()

        # Get the referral code for the user
        referral_code = ReferralCode.objects.filter(user=user).first()

        # Get the referral where the user is referred
        referral = None
        try:
            referral = Referral.objects.filter(referred=user).first()
        except Exception as e:
            print(e)

        
        # Initialize referrer and referrer_code
        referrer = None
        referrer_code = None

        # Check if referral exists
        if referral:
            # If the user has been referred, get the referrer and their referral code
            referrer = referral.referrer  # This is the user who invited the current user
            referrer_code = ReferralCode.objects.filter(user=referrer).first()  # Get the referrer code

            # Debugging print to see the referrer and referred information
            print(f"Referrer: {referrer}, Referred: {referral.referred}")

        else:
            # If no referral is found, handle it gracefully
            print("No referral found for this user.")

        # Add the profile form to the context
        context['profile_form'] = UpdateProfileForm(instance=profile)

        # Add the profile form to the context
        context['profile_base_form'] = UpdateBaseProfileForm(instance=profile)

        # Add the referral code to the context
        context['referral_code'] = referral_code.code if referral_code else None

        # Add the referrer code to the context
        context['referrer_code'] = referrer_code.code if referrer_code else None


        
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
        user = self.request.user
        profile = Profile.objects.filter(user=user).first()
        
        if not profile:
            messages.error(self.request, 'Profile not found for the current user.')
            return self.form_invalid(form)

        # Gestisci separatamente il profilo
        profile_form = UpdateProfileForm(self.request.POST, self.request.FILES, instance=profile)
        profile_base_form = UpdateBaseProfileForm(self.request.POST, instance=profile)

        if not profile_form.is_valid():
            print("Profile Form Errors:", profile_form.errors)
            messages.error(self.request, 'There was an error updating your profile.')
            return self.form_invalid(form)

        if not profile_base_form.is_valid():
            print("Profile Base Form Errors:", profile_base_form.errors)
            messages.error(self.request, 'There was an error updating your profile.')
            return self.form_invalid(form)

        # Salvataggio dei form
        profile_form.save()  # Salva i dati del profilo
        profile_base_form.save()  # Salva i dati del profilo base
        form.save()  # Salva i dati utente

        # Aggiungi un messaggio di successo
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
    
