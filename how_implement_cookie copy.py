"""Per implementare i cookie per gestire l'incentivo nell’app Affiliate, dovrai impostare un cookie che identifichi la fonte di riferimento ogni volta che un utente arriva tramite un link di affiliazione. Questo cookie verrà utilizzato per tracciare le azioni dell’utente nei giorni successivi e assicurare che l'incentivo venga attribuito all’affiliato corretto.

Step 1: Impostazione del Cookie nel Backend (Django View)
Quando un utente arriva tramite un link di affiliazione, supponiamo che l’URL contenga un parametro, come ?affiliate_id=123. Creiamo o modifichiamo una view in Django per impostare il cookie con questo affiliate_id.

Ad esempio, possiamo creare una view chiamata set_affiliate_cookie:

python
"""
from django.http import HttpResponse
from datetime import timedelta
from django.utils import timezone

def set_affiliate_cookie(request):
    affiliate_id = request.GET.get('affiliate_id')
    response = HttpResponse("Cookie impostato per l'affiliato!")
    
    # Se c'è un affiliate_id, imposta il cookie
    if affiliate_id:
        # Imposta il cookie per 30 giorni
        expiration = timezone.now() + timedelta(days=30)
        response.set_cookie('affiliate_id', affiliate_id, expires=expiration)
    
    return response
"""Step 2: Aggiornamento dell'URL di Ingresso per Tracciare i Riferimenti
Configura una URL che punti a questa view in urls.py:

python
"""
from django.urls import path
from . import views

urlpatterns = [
    path('track-affiliate/', views.set_affiliate_cookie, name='track_affiliate'),
]
"""Ora, ogni volta che un utente arriva tramite un link di affiliazione (es. https://yourdomain.com/track-affiliate/?affiliate_id=123), verrà impostato un cookie affiliate_id valido per 30 giorni.

Step 3: Utilizzo del Cookie nelle View
Quando vuoi verificare se l'utente ha un cookie di affiliazione attivo, ad esempio per assegnare incentivi, puoi controllare la presenza del cookie in qualsiasi view di Django. Se l’utente ha un cookie valido, puoi tracciare o assegnare la transazione all’affiliato specificato.

Ecco un esempio in una view che assegna l’incentivo:

python"""

from django.http import JsonResponse
from .models import Affiliate, AffiliateCommission

def check_affiliate_incentive(request):
    affiliate_id = request.COOKIES.get('affiliate_id')
    
    if affiliate_id:
        # Logica per assegnare l’incentivo (ad esempio, una commissione)
        try:
            affiliate = Affiliate.objects.get(id=affiliate_id)
            # Esempio di aggiunta di una commissione
            AffiliateCommission.objects.create(
                affiliate=affiliate,
                amount=10,  # Esempio di incentivo
                status="pending"
            )
            return JsonResponse({'message': 'Incentivo assegnato all’affiliato!'})
        except Affiliate.DoesNotExist:
            return JsonResponse({'error': 'Affiliato non trovato'}, status=404)
    
    return JsonResponse({'message': 'Nessun cookie di affiliazione presente'})
"""Step 4: JavaScript per Gestione Client-side (Opzionale)
Se desideri accedere ai cookie tramite JavaScript per verificare l’esistenza del affiliate_id lato client, puoi utilizzare un semplice script:

javascript"""

function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
}

const affiliateId = getCookie('affiliate_id');
if (affiliateId) {
    console.log(`Affiliate ID from cookie: ${affiliateId}`);
    // Potresti fare ulteriori richieste o aggiornamenti lato client
}
"""Step 5: Controllo di Scadenza e Rinnovo del Cookie
Se vuoi estendere o aggiornare il cookie ogni volta che l’utente accede al sito tramite il link di affiliazione, basta impostare di nuovo il cookie quando viene rilevato affiliate_id nell’URL, usando la stessa view set_affiliate_cookie.

Questa configurazione completa il processo di tracciamento degli utenti per 15-30 giorni tramite cookie. In questo modo, si garantisce che gli affiliati ricevano il credito per le azioni compiute dagli utenti che hanno portato al sito."""