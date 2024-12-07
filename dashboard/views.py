from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView 
from django.contrib.auth.views import LoginView, PasswordResetView, PasswordChangeView
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.views import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator 
  
@method_decorator(login_required, name='dispatch')
class HomeView(TemplateView):
    template_name = 'dashboard/index.html'

class ChartJSView(TemplateView):
    template_name = 'dashboard/pages/charts/chartjs.html'

class DocumentationView(TemplateView):
    template_name = 'dashboard/pages/documentation/documentation.html'

class BasicElementsView(TemplateView):
    template_name = 'dashboard/pages/forms/basic_elements.html'

class IconsView(TemplateView):
    template_name = 'dashboard/pages/icons/mdi.html'

class Error400View(TemplateView):
    template_name = 'dashboard/pages/samples/error-400.html'

class Error404View(TemplateView):
    template_name = 'dashboard/pages/samples/error-404.html'

class LoginView(TemplateView):
    template_name = 'dashboard/pages/samples/login.html'

class RegisterView(TemplateView):
    template_name = 'dashboard/pages/samples/register.html'

class TableView(TemplateView):
    template_name = 'dashboard/pages/tables/basic-table.html'

class ButtonsView(TemplateView):
    template_name = 'dashboard/pages/ui-features/buttons.html'

class DropdownsView(TemplateView):
    template_name = 'dashboard/pages/ui-features/dropdowns.html'

class TypographyView(TemplateView):
    template_name = 'dashboard/pages/ui-features/typography.html'

class WithdrawalView(TemplateView):
    template_name = 'dashboard/withdrawals.html'

"""

def home(request):
    return render(request, 'dashboard/index.html')

def charts_chartjs(request):
    return render(request, 'dashboard/pages/charts/chartjs.html')

def documentation(request):
    return render(request, 'dashboard/pages/documentation/documentation.html')

def forms_basic_elements(request):
    return render(request, 'dashboard/pages/forms/basic_elements.html')

def icons_mdi(request):
    return render(request, 'dashboard/pages/icons/mdi.html')

def error_404(request):
    return render(request, 'dashboard/pages/samples/error-404.html')

def error_500(request):
    return render(request, 'dashboard/pages/samples/error-404.html')

def login(request):
    return render(request, 'dashboard/pages/samples/login.html')

def register(request):
    return render(request, 'dashboard/pages/samples/register.html')

def tables_basic_table(request):
    return render(request, 'dashboard/pages/tables/basic-table.html')

def ui_features_buttons(request):
    return render(request, 'dashboard/pages/ui-features/buttons.html')

def ui_dropdowns(request):
    return render(request, 'dashboard/pages/ui-features/dropdowns.html')

def ui_features_typography(request):
    return render(request, 'dashboard/pages/ui-features/typography.html')

"""