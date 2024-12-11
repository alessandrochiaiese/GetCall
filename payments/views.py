from accounts.models.user import User
import stripe
from django.conf import settings
from django.http.response import JsonResponse, HttpResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import DetailView, ListView
from django.views.generic.base import TemplateView


from .models import Price, Product


class HomePageView(TemplateView):
    template_name = 'payments/home.html'


@csrf_exempt
def stripe_config(request):
    if request.method == 'GET':
        stripe_config = {'publicKey': settings.STRIPE_PUBLISHABLE_KEY}
        return JsonResponse(stripe_config, safe=False)


@csrf_exempt
def create_checkout_session(request):
    if request.method == 'GET':
        domain_url = 'http://localhost:8000/'
        stripe.api_key = settings.STRIPE_SECRET_KEY
        try:
            # Create new Checkout Session for the order
            # Other optional params include:
            # [billing_address_collection] - to display billing address details on the page
            # [customer] - if you have an existing Stripe Customer ID
            # [payment_intent_data] - lets capture the payment later
            # [customer_email] - lets you prefill the email input in the form
            # For full details see https:#stripe.com/docs/api/checkout/sessions/create

            # ?session_id={CHECKOUT_SESSION_ID} means the redirect will have the session ID set as a query param

            # If we want to identify the user when using webhooks we can pass client_reference_id  to checkout
            # session constructor. We will then be able to fetch it and make changes to our Django models.
            #
            # If we offer a SaaS service it would also be good to allow only authenticated users to purchase
            # anything on our site.

            try:
                # Use Stripe's library to make requests...
                checkout_session = stripe.checkout.Session.create(
                    # client_reference_id=request.user.id if request.user.is_authenticated else None,
                    success_url=domain_url + 'success?session_id={CHECKOUT_SESSION_ID}',
                    cancel_url=domain_url + 'cancelled/',
                    payment_method_types=['card'],
                    mode='payment',
                    line_items=[
                        {
                            'name': 'T-shirt',
                            'quantity': 1,
                            'currency': 'usd',
                            'amount': '2000',
                        }
                    ]
                )
            except stripe.error.CardError as e:
                # Since it's a decline, stripe.error.CardError will be caught

                print('Status is: %s' % e.http_status)
                print('Code is: %s' % e.code)
                # param is '' in this case
                print('Param is: %s' % e.param)
                print('Message is: %s' % e.user_message)
            except stripe.error.RateLimitError as e:
                # Too many requests made to the API too quickly
                pass
            except stripe.error.InvalidRequestError as e:
                # Invalid parameters were supplied to Stripe's API
                pass
            except stripe.error.AuthenticationError as e:
                # Authentication with Stripe's API failed
                # (maybe you changed API keys recently)
                pass
            except stripe.error.APIConnectionError as e:
                # Network communication with Stripe failed
                pass
            except stripe.error.StripeError as e:
                # Display a very generic error to the user, and maybe send
                # yourself an email
                pass
            except Exception as e:
                # Something else happened, completely unrelated to Stripe
                pass
            return JsonResponse({'sessionId': checkout_session['id']})
        except Exception as e:
            return JsonResponse({'error': str(e)})


@csrf_exempt
def stripe_webhook(request):
    stripe.api_key = settings.STRIPE_SECRET_KEY
    endpoint_secret = settings.STRIPE_ENDPOINT_SECRET
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None

    # Stripe CLI setup + login
    # The easiest way to test our webhook is to download Stripe CLI (https://stripe.com/docs/stripe-cli)
    # After downloading it we need to login by running 'stripe login' in Terminal, this command will generate
    # a pairing code for us an open our web browser.
    #
    # ---------------------------------------------------------------
    # Your pairing code is: word1-word2-word3-word4
    # This pairing code verifies your authentication with Stripe.
    # Press Enter to open the browser (^C to quit)
    # ---------------------------------------------------------------
    #
    # By pressing enter CLI opens our browser and asks us if we want to allow Stripe CLI to access our account
    # information. We can allow it by clicking 'Allow access' button and confirming the action with our password.
    #
    # If everything goes well Stripe CLI will display the following message:
    #
    # ---------------------------------------------------------------
    # > Done! The Stripe CLI is configured for {ACCOUNT_NAME} with account id acct_{ACCOUNT_ID}
    # Please note: this key will expire after 90 days, at which point you'll need to re-authenticate.
    # ---------------------------------------------------------------
    #
    # Webhook setup
    # Once we successfully logged in we can start listening to Stripe events and forward them to our webhook using
    # the following command:
    #
    # stripe listen --forward-to localhost:8000/webhook/
    #
    # This will generate a webhook signing secret that we should save in our settings.py. After that we will
    # need to pass it when constructing a Webhook event.
    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except ValueError as e:
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return HttpResponse(status=400)

    # Handle the checkout.session.completed event
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']

        # This method will be called when user successfully purchases something.
        handle_checkout_session(session)

    return HttpResponse(status=200)


def handle_checkout_session(session):
    # client_reference_id = user's id
    client_reference_id = session.get("client_reference_id")
    payment_intent = session.get("payment_intent")

    if client_reference_id is None:
        # Customer wasn't logged in when purchasing
        return

    # Customer was logged in we can now fetch the Django user and make changes to our models
    try:
        user = User.objects.get(id=client_reference_id)
        print(user.username, "just purchased something.")

        # TODO: make changes to our models.

    except User.DoesNotExist:
        pass


class SuccessView(TemplateView):
    template_name = 'payments/success.html'


class CancelledView(TemplateView):
    template_name = 'payments/cancelled.html'


@csrf_exempt
def stripe_webhook(request):
    stripe.api_key = settings.STRIPE_SECRET_KEY
    endpoint_secret = settings.STRIPE_ENDPOINT_SECRET
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except ValueError as e:
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return HttpResponse(status=400)

    # Handle the checkout.session.completed event
    if event['type'] == 'checkout.session.completed':
        print("Payment was successful.")
        # TODO: run some custom code here

    return HttpResponse(status=200)



#####################
# Product and Order #
#####################
 
"""
def create_product(request):
    if request.method == "POST":
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('product_list')  # Redirect to the product list page
    else:
        form = ProductForm()
    return render(request, 'commerce/create_product.html', {'form': form})



def create_order(request):
    if request.method == "POST":
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save()
            # Optionally, calculate the total price here
            order.calculate_total_price()
            return redirect('order_detail', order_id=order.id)
    else:
        form = OrderForm()
    return render(request, 'commerce/create_order.html', {'form': form})



def add_item_to_order(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    if request.method == "POST":
        form = OrderItemForm(request.POST)
        if form.is_valid():
            order_item = form.save(commit=False)
            order_item.order = order
            order_item.save()
            order.calculate_total_price()  # Recalculate the total price of the order
            return redirect('order_detail', order_id=order.id)
    else:
        form = OrderItemForm()
    return render(request, 'commerce/add_item_to_order.html', {'form': form, 'order': order})
"""

from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from .models import Product
from .forms import ProductForm
from django.views.generic import ListView, DetailView

class ProductListView(ListView):
    model = Product  # Modello associato alla vista
    template_name = 'commerce/list_product.html'
    context_object_name = 'products'  # Nome del contesto passato al template
    paginate_by = 10  # Opzionale, per aggiungere la paginazione

    def get_queryset(self):
        queryset = super().get_queryset()
        # Aggiungi filtri personalizzati, se necessario
        return queryset.order_by('-created_at')  # Esempio: ordina per data di creazione

class ProductDetailView(DetailView):
    template_name = 'commerce/detail_product.html'

class ProductUpdateView(CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'commerce/ipdate_product.html'
    success_url = reverse_lazy('product_list')  # Redirige alla lista dei prodotti dopo il salvataggio

class ProductCreateView(CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'commerce/create_product.html'
    success_url = reverse_lazy('product_list')  # Redirige alla lista dei prodotti dopo il salvataggio

    def form_valid(self, form):
        # Puoi aggiungere logica personalizzata prima di salvare il form, se necessario
        return super().form_valid(form)

from django.urls import reverse
from django.views.generic.edit import CreateView
from .models import Order
from .forms import OrderForm

class OrderCreateView(CreateView):
    model = Order
    form_class = OrderForm
    template_name = 'commerce/create_order.html'

    def form_valid(self, form):
        # Aggiungi logica per il calcolo del totale dell'ordine
        order = form.save()
        order.calculate_total_price()
        return redirect('order_detail', order_id=order.id)

    def get_success_url(self):
        # Puoi anche usare un redirect dinamico come in questo caso
        return reverse('order_detail', kwargs={'order_id': self.object.id})

from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.views.generic.edit import FormView
from .models import Order, OrderItem
from .forms import OrderItemForm

class AddItemToOrderView(FormView):
    form_class = OrderItemForm
    template_name = 'commerce/add_item_to_order.html'

    def dispatch(self, request, *args, **kwargs):
        self.order = get_object_or_404(Order, id=kwargs['order_id'])
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        order_item = form.save(commit=False)
        order_item.order = self.order
        order_item.save()
        
        # Ricalcola il prezzo totale dell'ordine
        self.order.calculate_total_price()

        return redirect('order_detail', order_id=self.order.id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['order'] = self.order
        return context


class ProductListView(ListView):
    model = Product
    context_object_name = "products"
    template_name = "payments/product_list.html"

class ProductDetailView(DetailView):
    model = Product
    context_object_name = "product"
    template_name = "payments/product_detail.html"

    def get_context_data(self, **kwargs):
        context = super(ProductDetailView, self).get_context_data()
        context["prices"] = Price.objects.filter(product=self.get_object())
        return context