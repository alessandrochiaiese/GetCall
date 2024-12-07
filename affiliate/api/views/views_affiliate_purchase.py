
from django.http import JsonResponse
from affiliate.models import Affiliate, AffiliateIncentive

def affiliate_purchase_view(request):
    # Verifica l'esistenza dei cookie di affiliazione
    affiliate_id = request.COOKIES.get('affiliate_id')
    program_id = request.COOKIES.get('program_id')

    if affiliate_id and program_id:
        # Logica per processare l'incentivo in base alla transazione
        try:
            affiliate = Affiliate.objects.get(id=affiliate_id)
            incentive = AffiliateIncentive.objects.get(affiliate=affiliate, program_id=program_id)

            # Applica l'incentivo per l'acquisto e segna il cookie come utilizzato
            incentive.apply_incentive()  # Funzione di esempio per calcolare l'incentivo
            response = JsonResponse({"message": "Incentivo applicato con successo."})

            # Imposta il cookie come scaduto o rimuovilo
            response.delete_cookie('affiliate_id')
            response.delete_cookie('program_id')

            return response
        except (Affiliate.DoesNotExist, AffiliateIncentive.DoesNotExist):
            return JsonResponse({"error": "Affiliato o incentivo non trovato."}, status=404)

    return JsonResponse({"error": "Cookie di affiliazione non trovato."}, status=400)