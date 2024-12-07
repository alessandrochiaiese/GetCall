
# pip install stripe
from developer.settings import STRIPE_SECRET_KEY
import stripe
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import redirect

stripe.api_key = STRIPE_SECRET_KEY

class CreateCheckoutSessionAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        # Ottieni il piano scelto dall'utente (ID del piano di Stripe)
        plan_id = request.data.get('plan_id')  # Assicurati che il piano corrisponda a quelli definiti su Stripe
        user = request.user

        try:
            # Crea la sessione di pagamento
            checkout_session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[{
                    'price_data': {
                        'currency': 'eur',
                        'product_data': {
                            'name': f'Abbonamento {plan_id}',
                        },
                        'unit_amount': 1000,  # Sostituisci con il prezzo del piano in centesimi
                    },
                    'quantity': 1,
                }],
                mode='subscription',  # Utilizza 'payment' per pagamento una tantum, 'subscription' per abbonamenti ricorrenti
                success_url='https://your-site.com/success/',
                cancel_url='https://your-site.com/cancel/',
            )

            return Response({
                "session_id": checkout_session.id
            })

        except stripe.error.StripeError as e:
            return Response({"error": str(e)}, status=400)
