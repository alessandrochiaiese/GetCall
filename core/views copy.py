from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView, PasswordResetView, PasswordChangeView
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.decorators import login_required
from django.views import View
from django.http import JsonResponse
from django.db.models import Sum
from referral.models import Referral, ReferralCode, ReferralBonus, ReferralAudit, ReferralStats, ReferralTransaction
from referral.models import *
from .forms import RegisterForm, LoginForm, UpdateUserForm, UpdateProfileForm


def home(request):
    return render(request, 'core/home.html')

def landing_page(request):
    return render(request, 'core/landing_page.html')


class RegisterView(View):
    form_class = RegisterForm
    initial = {'key': 'value'}
    template_name = 'core/register.html'

    def dispatch(self, request, *args, **kwargs):
        # will redirect to the home page if a user tries to access the register page while logged in
        if request.user.is_authenticated:
            return redirect(to='/')

        # else process dispatch as it otherwise normally would
        return super(RegisterView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)

        if form.is_valid():
            form.save()

            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}')

            return redirect(to='core_login')

        return render(request, self.template_name, {'form': form})


# Class based view that extends from the built in login view to add a remember me functionality
class CustomLoginView(LoginView):
    form_class = LoginForm

    def form_valid(self, form):
        remember_me = form.cleaned_data.get('remember_me')

        if not remember_me:
            # set session expiry to 0 seconds. So it will automatically close the session after the browser is closed.
            self.request.session.set_expiry(0)

            # Set session as modified to force data updates/cookie to be saved.
            self.request.session.modified = True

        # else browser session will be as long as the session cookie time "SESSION_COOKIE_AGE" defined in settings.py
        return super(CustomLoginView, self).form_valid(form)


class ResetPasswordView(SuccessMessageMixin, PasswordResetView):
    template_name = 'core/password_reset.html'
    email_template_name = 'core/password_reset_email.html'
    subject_template_name = 'core/password_reset_subject'
    success_message = "We've emailed you instructions for setting your password, " \
                      "if an account exists with the email you entered. You should receive them shortly." \
                      " If you don't receive an email, " \
                      "please make sure you've entered the address you registered with, and check your spam folder."
    success_url = reverse_lazy('core-home')


class ChangePasswordView(SuccessMessageMixin, PasswordChangeView):
    template_name = 'core/change_password.html'
    success_message = "Successfully Changed Your Password"
    success_url = reverse_lazy('core-home')


@login_required
def profile(request):
    if request.method == 'POST':
        user_form = UpdateUserForm(request.POST, instance=request.user)
        profile_form = UpdateProfileForm(request.POST, request.FILES, instance=request.user.profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile is updated successfully')
            return redirect(to='core_profile')
    else:
        user_form = UpdateUserForm(instance=request.user)
        profile_form = UpdateProfileForm(instance=request.user.profile)

    return render(request, 'core/profile.html', {'user_form': user_form, 'profile_form': profile_form})


"""
@login_required
def user_profile_data(request):
    user = request.user
    referral_data = {
        'total_commission': Referral.objects.filter(user=user).aggregate(Sum('commission'))['commission__sum'] or 0,
        'active_referrals': Referral.objects.filter(user=user, status='active').count(),
        'total_rewards': ReferralBonus.objects.filter(user=user).aggregate(Sum('reward_value'))['reward_value__sum'] or 0,
        'referral_codes': ReferralCode.objects.filter(user=user).values('code', 'usage_count'),
        'recent_audits': list(ReferralAudit.objects.filter(user=user).values('date', 'type', 'details', 'amount')),
        'referral_stats': list(ReferralStats.objects.filter(referral_code__user=user).values('click_count', 'conversion_count', 'total_rewards')),
        'referral_transactions': list(ReferralTransaction.objects.filter(referral_code__user=user).values('transaction_date', 'order_id', 'transaction_amount')),
    }
    return JsonResponse(referral_data)
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Referral, ReferralCode, ReferralBonus, ReferralActivity, ReferralCampaign

@login_required
def user_profile_data(request):
    user = request.user

    # Dati per i programmi di referral
    referral_codes = ReferralCode.objects.filter(user=user).values('code', 'usage_count')

    # Dati per le campagne attive
    active_campaigns = ReferralCampaign.objects.filter(is_active=True).values('id', 'name', 'start_date', 'end_date')

    # Attività recenti
    recent_activities = ReferralActivity.objects.filter(user=user).values('date', 'type', 'details', 'amount')

    # Ottieni il codice referral unico dell'utente
    referral_code = ReferralCode.objects.filter(user=user).first()

    data = {
        'referral_codes': list(referral_codes),
        'referral_campaigns': list(active_campaigns),
        'recent_activities': list(recent_activities),
        'referral_code': referral_code.code if referral_code else ''
    }

    return JsonResponse(data)
"""
  

@login_required
def user_profile_data(request):
    user = request.user

    # Dati generali di referral
    referral_data = {
        'total_commission': Referral.objects.filter(user=user).aggregate(Sum('commission'))['commission__sum'] or 0,
        'active_referrals': Referral.objects.filter(user=user, status='active').count(),
        'total_rewards': ReferralBonus.objects.filter(user=user).aggregate(Sum('reward_value'))['reward_value__sum'] or 0,
    }

    # Dati per i codici referral
    referral_codes = ReferralCode.objects.filter(user=user).values('code', 'usage_count')

    # Dati per le campagne attive
    active_campaigns = ReferralCampaign.objects.filter(is_active=True).values('id', 'name', 'start_date', 'end_date')

    # Attività recenti
    #recent_activities = ReferralActivity.objects.filter(user=user).values('date', 'type', 'details', 'amount')

    # Statistiche dei referral
    referral_stats = list(ReferralStats.objects.filter(referral_code__user=user).values('click_count', 'conversion_count', 'total_rewards'))

    # Transazioni dei referral
    referral_transactions = list(ReferralTransaction.objects.filter(referral_code__user=user).values('transaction_date', 'order_id', 'transaction_amount'))

    # Audit dei referral
    recent_audits = list(ReferralAudit.objects.filter(user=user).values('date', 'type', 'details', 'amount'))

    # Codice referral unico dell'utente
    referral_code = ReferralCode.objects.filter(user=user).first()

    data = {
        'referral_data': referral_data,
        'referral_codes': list(referral_codes),
        'referral_campaigns': list(active_campaigns),
        #'recent_activities': list(recent_activities),
        'referral_stats': referral_stats,
        'referral_transactions': referral_transactions,
        'recent_audits': recent_audits,
        'referral_code': referral_code.code if referral_code else ''
    }

    return JsonResponse(data)

@login_required
def participate_campaign(request):
    if request.method == 'POST':
        campaign_id = request.POST.get('campaign_id')
        campaign = ReferralCampaign.objects.get(id=campaign_id)

        # Logica per associare l'utente alla campagna, per esempio creando una partecipazione
        # Implementa la logica in base ai tuoi modelli (potresti voler creare un record di partecipazione)

        # Risposta di successo
        return JsonResponse({'success': True})

    return JsonResponse({'success': False}, status=400)
