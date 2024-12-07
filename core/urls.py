
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from django.urls import include, path, re_path as url
from core.views import CustomLoginView, ResetPasswordView, ChangePasswordView, ProfileView, UserProfileDataView, RegisterView
from core.forms import LoginForm
from getref import settings  

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
from .views import (
    AddItemToOrderView,
    HomeView,
    LandingPageView,
    OrderCreateView,
    #OrderView,
    ProductCreateView,
    ProductDetailView,
    ProductListView,
    ProductUpdateView,
    ReferralRedirectView,
    RegisterView,
    CustomLoginView,
    ResetPasswordView,
    ChangePasswordView,
    ProfileView,
    UserProfileDataView,
    ParticipateCampaignView,
    UserReferredLevelView,
    get_user_table,
    track_referral_code,
)
from django.contrib.auth.views import LogoutView

urlpatterns = [
    # Pagina principale
    path('', HomeView.as_view(), name='core_home'),

    # get users referred with level
    #path('get-level-users/', UserReferredLevelView.as_view(), name='get_user_table'), #get_user_table, name='get_user_table'),

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

    # Profilo utente
    path('profile/', ProfileView.as_view(), name='core_profile'),
    
    # Dati profilo utente (API JSON)
    path('profile/data/', UserProfileDataView.as_view(), name='core_profile_data'),
    
    # Partecipazione a campagne di referral
    path('campaign/participate/', ParticipateCampaignView.as_view(), name='core_participate_campaign'),
    
    path('product/list/', ProductListView.as_view(), name='product_list'),
    path('product/create/', ProductCreateView.as_view(), name='create_product'),
    path('product//<int:order_id>/update/', ProductUpdateView.as_view(), name='create_product'),
    path('product/<int:order_id>/', ProductDetailView.as_view(), name='product_detail'),
    
    path('order/create/', OrderCreateView.as_view(), name='create_order'),
    path('order/<int:order_id>/add_item/', AddItemToOrderView.as_view(), name='add_item_to_order'),
    
    #path("order/<int:pk>/", OrderView.as_view(), name="order_detail"),

    path('track/<int:referral_code>/', track_referral_code, name=''),
    
    path('api/v0/', include('core.api.urls'), name='api_profile'),

    url(r'^oauth/', include('social_django.urls', namespace='social')),

] + static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)
