
from django.conf.urls.static import static
from django.urls import include, path, re_path as url
 
from getcall import settings   
from dashboard.views import *

from django.contrib.auth import views as auth_views
from dashboard.views import *

from dashboard.forms import *
from django.urls import path
from .views import (
    HomeView,
    ChartJSView,
    DocumentationView,
    BasicElementsView,
    IconsView,
    Error400View,
    Error404View,
    LoginView,
    RegisterView,
    TableView,
    DropdownsView,
    TypographyView,
    WithdrawalView,
)

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('home/', HomeView.as_view(), name='home'),
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
    path('withdrawals/', WithdrawalView.as_view(), name='withdrawals'),
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