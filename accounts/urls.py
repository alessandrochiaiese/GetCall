# accounts/urls.py
from django.urls import include, path

from accounts.views.views_account import role_detail_view, role_list_view, user_detail_view, user_list_view

from accounts.views.views_account import SignUpView


urlpatterns = [
    # APIs
    path('', include('accounts.api.urls')),

    # Entities
    #path('roles/', role_list_view, name='role_list'),
    #path('roles/<int:pk>/', role_detail_view, name='role_detail'),
    
    #path('users/', user_list_view, name='user_list'),
    #path('users/<int:pk>/', user_detail_view, name='user_detail'),
    
    # Signup
    #path("signup/", SignUpView.as_view(), name="signup"),
]