from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from accounts.models.user import User
from getcall.settings import STRIPE_SECRET_KEY, STRIPE_ENDPOINT_SECRET
import stripe

from subscriptions.utils import send_subscription_email
from subscriptions.models import *
from django.utils.timezone import now
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from django.http import JsonResponse

stripe.api_key = STRIPE_SECRET_KEY
  

class PurchaseTokensAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        package_id = request.data.get('package_id')  # L'ID del pacchetto scelto dall'utente
        user = request.user
        package = get_object_or_404(TokenPackage, id=package_id)

        try:
            # Crea una sessione di pagamento Stripe
            checkout_session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[{
                    'price_data': {
                        'currency': 'eur',
                        'product_data': {
                            'name': f'Acquisto {package.name} ({package.tokens} token)',
                        },
                        'unit_amount': package.price_in_cents,  # Prezzo del pacchetto in centesimi
                    },
                    'quantity': 1,
                }],
                mode='payment',
                success_url='https://your-site.com/success/',  # URL di successo
                cancel_url='https://your-site.com/cancel/',  # URL di cancellazione
                client_reference_id=user.id,  # Passiamo l'ID dell'utente
                metadata={'package_id': package.id},
            )

            return Response({
                "session_id": checkout_session.id
            })

        except stripe.error.StripeError as e:
            return Response({"error": str(e)}, status=400)


@csrf_exempt
def stripe_webhook_simple(request):
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    endpoint_secret = settings.STRIPE_ENDPOINT_SECRET  # Ottieni questa chiave da Stripe

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )

        # Gestisci il pagamento completato
        """if event['type'] == 'checkout.session.completed':
            session = event['data']['object']
            user_id = session['client_reference_id']
            plan_id = session['metadata']['plan_id']
            user = User.objects.get(id=user_id)
            plan = Plan.objects.get(id=plan_id)

            # Crea o aggiorna l'abbonamento
            subscription, created = Subscription.objects.get_or_create(user=user)
            subscription.plan = plan
            subscription.renew()

            return JsonResponse({'status': 'success'})"""
        
        if event['type'] == 'invoice.payment_succeeded':
            invoice = event['data']['object']
            user_id = invoice['customer']
            user = User.objects.get(stripe_customer_id=user_id)  # Usa l'ID cliente di Stripe
            plan_id = invoice['metadata']['plan_id']
            plan = Plan.objects.get(id=plan_id)

            # Trova o crea l'abbonamento
            subscription, created = Subscription.objects.get_or_create(user=user)
            subscription.plan = plan
            subscription.renew()

            # Invia un'email di rinnovo
            send_subscription_email(user, plan)
            return JsonResponse({'status': 'success'})
        
    except ValueError as e:
        # Event data is invalid
        return JsonResponse({'error': 'Invalid payload'}, status=400)
    except stripe.error.SignatureVerificationError as e:
        # Signature verification failed
        return JsonResponse({'error': 'Invalid signature'}, status=400)

    return JsonResponse({'status': 'success'})

@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    endpoint_secret = STRIPE_ENDPOINT_SECRET  # Ottieni questa chiave da Stripe

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )

        # Se l'evento riguarda un pagamento completato
        if event['type'] == 'checkout.session.completed':
            session = event['data']['object']
            user_id = session['client_reference_id']
            package_id = session['metadata']['package_id']
            user = User.objects.get(id=user_id)
            package = TokenPackage.objects.get(id=package_id)

            # Trova o crea il record dei token per l'utente
            token_record, created = Token.objects.get_or_create(user=user)
            token_record.add_tokens(package.tokens)

            return JsonResponse({'status': 'success'})

    except ValueError as e:
        return JsonResponse({'error': 'Invalid payload'}, status=400)
    except stripe.error.SignatureVerificationError as e:
        return JsonResponse({'error': 'Invalid signature'}, status=400)

    return JsonResponse({'status': 'success'})
