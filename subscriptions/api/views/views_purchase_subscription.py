from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from subscriptions.models import Plan, Subscription

class PurchaseSubscriptionAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        plan_id = request.data.get('plan_id')
        plan = Plan.objects.filter(id=plan_id).first()

        if not plan:
            return Response({"error": "Piano non valido"}, status=400)

        # Crea o aggiorna l'abbonamento
        subscription, created = Subscription.objects.get_or_create(user=request.user)
        subscription.plan = plan
        subscription.renew()

        return Response({
            "message": f"Abbonamento {plan.name} attivato con successo!",
            "expires_at": subscription.expires_at,
            "tokens_available": subscription.tokens_available,
        })
