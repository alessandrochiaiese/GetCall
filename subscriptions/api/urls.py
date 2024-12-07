from django.urls import path
from subscriptions.api.views.views_purchase_subscription import PurchaseSubscriptionAPIView
from subscriptions.api.views.views_purchase_token import PurchaseTokensAPIView


urlpatterns = [
    path('purchase-subscription/', PurchaseSubscriptionAPIView.as_view(), name='purchase_subscription'),
    path('purchase-tokens/', PurchaseTokensAPIView.as_view(), name='purchase_tokens'),
]