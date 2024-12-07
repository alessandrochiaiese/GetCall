from django.utils.deprecation import MiddlewareMixin
from datetime import datetime
from referral.models import Referral, ReferralAudit

class ReferralAuditMiddleware(MiddlewareMixin):
    def process_request(self, request):
        # Ottieni i cookie
        user = request.user
        user_id = request.COOKIES.get('user_id') 

        # Verifica se l'utente è presente nei cookie
        if user_id:
            try:
                user = Referral.objects.get(referred=user_id)
            except Referral.DoesNotExist:
                user = None
        else:
            user = None

        # Controlla se l'endpoint richiesto inizia con 'api/v0/referral'
        if request.path.startswith('/api/v0/referral/'):
            # Se c'è un referral_id e program_id, procedi a creare un'istanza di ReferralAudit
            try:
                # Crea una nuova istanza di ReferralAudit
                ReferralAudit.objects.create(
                    action_taken=request.path,  # Usa l'endpoint come descrizione dell'azione
                    action_date=datetime.now(),
                    user=user,
                    ip_address=request.META.get('REMOTE_ADDR'),  # Ottieni l'indirizzo IP
                    device_info=request.META.get('HTTP_USER_AGENT'),  # Ottieni le informazioni sul dispositivo
                    location=request.META.get('HTTP_X_FORWARDED_FOR', request.META.get('REMOTE_ADDR'))  # Indirizzo IP del client
                )
            except Referral.DoesNotExist:
                pass  # Se non trova il referral, ignora la creazione dell'audit

        return None
