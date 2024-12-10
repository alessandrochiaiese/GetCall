from django.urls import path 
from dashboard.api.views.views_profile import ProfileAPIView
 
urlpatterns = [  
    path('profiles/', ProfileAPIView.as_view(), name='profiles'),
    path('profiles/<int:profile_id>/', ProfileAPIView.as_view(), name='profile'),
 
]
