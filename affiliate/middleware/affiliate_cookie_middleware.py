
from django.utils.deprecation import MiddlewareMixin
from datetime import datetime, timedelta
from affiliate.models import Affiliate, AffiliateIncentive  # Importa il modello per gestire gli incentivi

class AffiliateCookieMiddleware(MiddlewareMixin):
    def process_request(self, request):
        # Controlla se il cookie di affiliazione è presente
        affiliate_id = request.COOKIES.get('affiliate_id')
        program_id = request.COOKIES.get('program_id')

        if affiliate_id and program_id:
            # Controlla se l'affiliato esiste
            try:
                affiliate = Affiliate.objects.get(id=affiliate_id)
                program = affiliate.programs.get(id=program_id)
                
                # Logica per gestire l'incentivo (es. crea un record di tracciamento, segna la visita, ecc.)
                AffiliateIncentive.objects.create(
                    affiliate=affiliate,
                    program=program,
                    date=datetime.now(),
                    is_incentive_active=True
                )

            except Affiliate.DoesNotExist:
                pass  # Affiliate non trovato, ignora il cookie

        return None