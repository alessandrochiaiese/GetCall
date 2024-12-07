"""Per implementare un sistema di tracciamento tramite cookie per gli incentivi del sistema Affiliate, dovrai gestire i cookie a livello sia di front-end (per impostare e leggere i cookie sul browser dell'utente) che di back-end (per verificare e gestire gli incentivi).

Ecco i passaggi e dove implementare ciascun componente:

1. Impostazione dei Cookie nel Front-End
Per il front-end, JavaScript può impostare un cookie alla prima visita dell’utente tramite un link di affiliazione. Questo cookie deve includere informazioni necessarie per l’affiliazione, come l’ID dell’affiliato e il programma a cui si riferisce. Impostiamolo in modo che duri per 15-30 giorni, secondo i requisiti.

Ecco un esempio di codice JavaScript per impostare un cookie:

javascript"""

function setAffiliateCookie(name, value, days) {
    const date = new Date();
    date.setTime(date.getTime() + (days * 24 * 60 * 60 * 1000));
    const expires = "expires=" + date.toUTCString();
    document.cookie = name + "=" + value + ";" + expires + ";path=/";
}

// Verifica se il parametro di affiliazione è presente nell'URL
const urlParams = new URLSearchParams(window.location.search);
const affiliateId = urlParams.get('affiliate_id');
const programId = urlParams.get('program_id');

if (affiliateId && programId) {
    setAffiliateCookie('affiliate_id', affiliateId, 30); // Cookie valido per 30 giorni
    setAffiliateCookie('program_id', programId, 30);
}
"""2. Verifica dei Cookie nel Back-End (Django)
Nel backend Django, verifica i cookie per registrare un incentivo solo se i cookie sono presenti e validi (e non scaduti). Puoi implementare questa verifica nel tuo Affiliate view o middleware per automatizzare il processo ogni volta che viene effettuata una richiesta al sito web.

Esempio di Middleware Django per Verificare il Cookie di Affiliazione
In questo caso, il middleware controlla la presenza di cookie di affiliazione e gestisce l’incentivo se il cookie è valido.

Crea un middleware chiamato AffiliateCookieMiddleware:
python"""

# middleware/affiliate_cookie_middleware.py

from django.utils.deprecation import MiddlewareMixin
from datetime import datetime, timedelta
from .models import Affiliate, AffiliateIncentive  # Importa il modello per gestire gli incentivi

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
"""Aggiungi il middleware in settings.py per attivarlo:
python"""

MIDDLEWARE = [
    # ... altri middleware ...
    'myapp.middleware.affiliate_cookie_middleware.AffiliateCookieMiddleware',
]
"""3. Utilizzo del Cookie di Affiliazione
A seconda della logica del programma di affiliazione, potresti voler aggiornare o verificare questi cookie in momenti specifici, come durante un acquisto. Per esempio:

python"""

# views.py

from django.http import JsonResponse
from .models import Affiliate, AffiliateIncentive

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
"""4. Eliminazione dei Cookie
Assicurati di rimuovere i cookie quando l'incentivo è applicato, come mostrato sopra, o alla scadenza. Puoi configurare questo comportamento nel middleware o nella logica di gestione degli incentivi.

Riepilogo
Frontend: JavaScript imposta i cookie con l’affiliate_id e program_id dai parametri URL e li mantiene attivi per 15-30 giorni.
Backend Middleware: Controlla i cookie di affiliazione e registra un incentivo se presenti.
Gestione del Cookie: Assicurati di rimuovere o invalidare i cookie al termine dell’utilizzo per evitare riapplicazioni non volute."""