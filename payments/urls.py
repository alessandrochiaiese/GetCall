from django.urls import path

from dashboard.utils import track_referral_code

from . import views

from .views import (
    AddItemToOrderView,
    CancelledView,
    HomePageView,
    OrderCreateView,
    ProductCreateView,
    ProductDetailView,
    ProductListView,
    ProductUpdateView,
    SuccessView,
    create_checkout_session,
    stripe_config,
)

urlpatterns = [
    path('config/', stripe_config),
    path('create-checkout-session/', create_checkout_session),
    
    path('marketplace/', HomePageView.as_view(), name='marketplace'),
    path('success/', SuccessView.as_view()),
    path('cancelled/', CancelledView.as_view()),

    #path("", ProductListView.as_view(), name="product-list"),
    #path("<int:pk>/", ProductDetailView.as_view(), name="product-detail"),

    path('product/list/', ProductListView.as_view(), name='product_list'),
    path('product/create/', ProductCreateView.as_view(), name='create_product'),
    path('product/<int:order_id>/update/', ProductUpdateView.as_view(), name='create_product'),
    path('product/<int:order_id>/', ProductDetailView.as_view(), name='product_detail'),
    
    path('order/create/', OrderCreateView.as_view(), name='create_order'),
    path('order/<int:order_id>/add_item/', AddItemToOrderView.as_view(), name='add_item_to_order'),
    
    #path("order/<int:pk>/", OrderView.as_view(), name="order_detail"),

    path('track/<int:referral_code>/', track_referral_code, name=''),
     
    path('webhook/stripe/', views.stripe_webhook),
]
