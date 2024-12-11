
from django.conf.urls.static import static
from django.urls import include, path, re_path as url
 
from getref import settings   
from dashboard.utils import *
    
from django.contrib.auth import views as auth_views 
from dashboard.forms import * 
from dashboard.views.views_accounts import (
    LandingPageView,
    LoginView,
    CustomLoginView,
    ReferralRedirectView, ResetPasswordView, ChangePasswordView, RegisterView
)
from dashboard.views.views_profile import (

    ProfileView, UserProfileDataView,
)
from dashboard.views.views_dashboard import (
    HomeView,
    IncompleteRegistrationsView,
    InvestorAccountsView,
    MasterAccountsView,
    MyIBsView,
    ParticipateCampaignView,
    WithdrawalView,
)
from dashboard.views.views_kit_template import (
    ChartJSView,
    DocumentationView,
    BasicElementsView,
    IconsView,
    Error400View,
    Error404View,
    TableView,
    DropdownsView,
    TypographyView,
)

"""urlpatterns = [
    #path('', home, name='core-home'),
    path('profile/', ProfileView.as_view(), name='core_profile'),
    path('user_profile_data/', UserProfileDataView.as_view(), name='core_user_profile_data'),
    
    path('register/', RegisterView.as_view(), name='core_register'),
    path('login/', CustomLoginView.as_view(redirect_authenticated_user=True, template_name='core/login.html',
                                           authentication_form=LoginForm), name='core_login'),

    path('logout/', auth_views.LogoutView.as_view(template_name='core/logout.html'), name='logout'),

    path('password-reset/', ResetPasswordView.as_view(), name='core_password_reset'),

    path('password-reset-confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name='core/password_reset_confirm.html'),
         name='password_reset_confirm'),

    path('password-reset-complete/',
         auth_views.PasswordResetCompleteView.as_view(template_name='core/core_password_reset_complete.html'),
         name='core_password_reset_complete'),

    path('password-change/', ChangePasswordView.as_view(), name='core_password_change'),

    url(r'^oauth/', include('social_django.urls', namespace='social')),

] + static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)"""


from django.urls import path 
from django.contrib.auth.views import LogoutView

urlpatterns = [
    ## dashboard
    path('', HomeView.as_view(), name='core_home'),
    path('dashboard/', HomeView.as_view(), name='dashboard'),
    path('accounts/master/', MasterAccountsView.as_view(), name='master_accounts'),
    path('accounts/investor/', InvestorAccountsView.as_view(), name='investor_accounts'),
    path('accounts/incomplete/', IncompleteRegistrationsView.as_view(), name='incomplete_registrations'),
    path('my-ibs/', MyIBsView.as_view(), name='my_ibs'),

    # get users referred with level
    #path('get-level-users/', UserReferredLevelView.as_view(), name='get_user_table'), #get_user_table, name='get_user_table'),

    ## accounts
    # Pagina di atterraggio
    path('landing/', LandingPageView.as_view(), name='core_landing_page'),
    
    # Registrazione
    path('register/', RegisterView.as_view(), name='core_register'),    
    path('referral-code/<str:referral_code>/', ReferralRedirectView.as_view(), name='referral_redirect'),
    path('register/<str:referral_code>/', RegisterView.as_view(), name='core_register_with_referral'),
    #path('referral-code/', ReferralRedirectView.as_view(), name='referral_redirect'),
    
    # Login e Logout
    path('login/', CustomLoginView.as_view(), name='core_login'),
    path('accounts/logout/', LogoutView.as_view(next_page='core_home'), name='core_logout'),
    
    # Reset della password
    path('password-reset/', ResetPasswordView.as_view(), name='core_password_reset'),
    
    # Cambio della password
    path('password-change/', ChangePasswordView.as_view(), name='core_change_password'),
    
    path('password-reset-confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name='core/password_reset_confirm.html'),
         name='core_password_reset_confirm'),

    path('password-reset-complete/',
         auth_views.PasswordResetCompleteView.as_view(template_name='core/core_password_reset_complete.html'),
         name='core_password_reset_complete'),

    ## profile
    path('profile/', ProfileView.as_view(), name='core_profile'),
    
    # Dati profilo utente (API JSON)
    path('profile/data/', UserProfileDataView.as_view(), name='core_profile_data'),
    
    # Partecipazione a campagne di referral
    path('campaign/participate/', ParticipateCampaignView.as_view(), name='core_participate_campaign'),
    
    path('withdrawals/', WithdrawalView.as_view(), name='withdrawals'),

    ## kit_template visible only for admin
    path('charts/chartjs/', ChartJSView.as_view(), name='charts'),
    path('documentation/', DocumentationView.as_view(), name='documentation'),
    path('forms/basic_elements/', BasicElementsView.as_view(), name='forms_basic_elements'),
    path('icons/', IconsView.as_view(), name='icons_mdi'),
    path('error/404/', Error400View.as_view(), name='error-404'),
    path('error/500/', Error404View.as_view(), name='error-500'),
    path('login/', LoginView.as_view(), name='login'),
    path('register/', RegisterView.as_view(), name='register'),
    path('tables/basic-table/', TableView.as_view(), name='basic_table'),
    path('ui-features/buttons/', DropdownsView.as_view(), name='ui_features_buttons'),
    path('ui-features/dropdowns/', DropdownsView.as_view(), name='ui_features_dropdowns'),
    path('ui-features/typography/', TypographyView.as_view(), name='ui_features_typography'),
    
    ## api
    path('api/v0/', include('dashboard.api.urls'), name='api_profile'),

    ## social django
    url(r'^oauth/', include('social_django.urls', namespace='social')),

]+ static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)

"""urlpatterns = [
    path('', HomeView.as_view(), name='core_home'),
    
    path('', home, name='home'), 
    path('home/', home, name='home'), 
    path('pages/charts/chartjs/', charts_chartjs, name='charts'), 
    path('documentation/', documentation, name='documentation'), 
    path('pages/forms/basic_elements/', forms_basic_elements, name='forms_basic_elements'), 
    path('icons_mdi/', icons_mdi, name='icons_mdi'), 
    path('error_404/', error_404, name='error-404'), 
    path('error_500/', error_500, name='error-500'), 
    #path('login/', login, name='login'), 
    #path('register/', register, name='register'), 
    path('tables_basic_table/', tables_basic_table, name='basic_table'), 
    path('pages/ui-features/buttons/', ui_features_buttons, name='ui_features_buttons'), 
    path('pages/ui-features/dropdowns/', ui_dropdowns, name='ui_features_dropdowns'), 
    path('pages/ui-features/typography/', ui_features_typography, name='ui_features_typography'), 

] + static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)
"""