from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from subscriptions.models import *

class PurchaseTokensAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        tokens_to_buy = request.data.get('tokens')
        price_entry = TokenPrice.objects.filter(quantity=tokens_to_buy).first()

        if not price_entry:
            return Response({"error": "Quantità di token non valida"}, status=400)

        # Aggiorna i token disponibili
        subscription, created = Subscription.objects.get_or_create(user=request.user)
        subscription.tokens_available += tokens_to_buy
        subscription.save()

        return Response({
            "message": f"Aggiunti {tokens_to_buy} token al tuo account.",
            "tokens_available": subscription.tokens_available,
        })
