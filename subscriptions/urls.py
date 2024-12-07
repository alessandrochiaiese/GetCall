
from django.conf.urls.static import static
from django.urls import include, path, re_path as url

from getref import settings 
from .views import stripe_webhook
from .views import PurchaseTokensAPIView, stripe_webhook

urlpatterns = [
    path('purchase-tokens/', PurchaseTokensAPIView.as_view(), name='purchase-tokens'),
    path('stripe/webhook/', stripe_webhook, name='stripe-webhook'),
    path('api/v0/', include('subscriptions.api.urls'), name='subscriptions'),
] 