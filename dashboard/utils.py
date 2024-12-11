 
from django.contrib.auth import get_user_model 
from referral.models.referral import Referral
from referral.models.referral_code import ReferralCode 
  
 
from django.contrib.auth import get_user_model 
from django.http import JsonResponse 
from django.utils import timezone 
from referral.models import *
from referral.forms import *
from dashboard.forms import * 
 

User = get_user_model()
 
  

#####################
# Hierarchy         #
#####################
def track_referral_code(referral_code, referred_user=None):
    try:
        referral = ReferralCode.objects.get(code=referral_code, status="active")

        # Creazione di una nuova conversione
        conversion = ReferralConversion.objects.create(
            referral_code=referral,
            referred_user=referred_user,
            conversion_date=timezone.now(),
            conversion_value=10,  # Valore arbitrario
            status="pending",
            reward_issued=False
        )

        # Aggiorna le statistiche del codice
        stats = ReferralStats.objects.get(referral_code=referral)
        stats.click_count += 1
        if referred_user:
            stats.conversion_count += 1
        stats.save()

        # Genera una reward se i criteri sono soddisfatti
        if stats.conversion_count >= referral.program.min_referral_count:
            ReferralReward.objects.create(
                referral_code=referral,
                referred_user=referred_user,
                reward_type=referral.program.reward_type,
                reward_value=referral.program.reward_value,
                date_awarded=timezone.now(),
                status="active"
            )

        return {"message": "Codice tracciato con successo.", "conversion_id": conversion.id}
    except ReferralCode.DoesNotExist:
        raise ValueError("Codice referral non trovato o non attivo.")
    except Exception as e:
        raise ValueError(f"Errore durante il tracking: {e}")
    
def get_referral_hierarchy(user, depth=0):
    referrals = Referral.objects.filter(referrer=user)
    hierarchy = []
    for referral in referrals:
        hierarchy.append({
            'user': referral.referred,
            'depth': depth,
            'children': get_referral_hierarchy(referral.referred, depth + 1)
        })
    return hierarchy

def calculate_user_level(user, depth=1, max_depth=5):
    """ Funzione ricorsiva per calcolare il livello di un utente. """
    if depth > max_depth:
        return 0  # Raggiunta la profondità massima

    referrals = Referral.objects.filter(referrer=user)  # Ottieni tutti i referrals per l'utente
    if not referrals.exists():
        return depth  # Se non ci sono altri referrals, siamo al livello massimo per questo ramo

    # Altrimenti, esplora i referrals in profondità
    max_level = 0
    for referral in referrals:
        for referred_user in referral.referred.all():
            current_level = calculate_user_level(referred_user, depth + 1, max_depth)
            max_level = max(max_level, current_level)  # Trova il livello massimo tra i referrals

    return max_level

def get_tree_referred(user, level=1):# -> dict: 
    tree = []

    # Interrompe la ricorsione se il livello supera 5
    if level > 5:
        return tree
    
    referral = None
    try:
        referral = Referral.objects.filter(referrer=user).first()
    except Exception as e:
        print(e)

    if referral is None:
        print(f"No referral found for user {user.username}")
        return tree

    for referred_user in referral.referred.all():
        print(f"Processing user: {referred_user.username}, Level: {level}")  # Debug
        user_to_add = {
            "first_name": referred_user.first_name,
            "last_name": referred_user.last_name,
            "username": referred_user.username,
            "date_joined": referred_user.date_joined,
            "level": level,
            "list_referred": get_tree_referred(referred_user, level+1)
        }
        tree.append(user_to_add)
     
    return tree

def tree_to_list(tree, _list=None):
    if _list is None:
        _list = []  # Inizializza una lista vuota se non è stata passata
    
    for leaf in tree:
        # Verifica che ogni 'leaf' sia un dizionario
        if isinstance(leaf, dict):
            user_to_add = {
                "first_name": leaf.get('first_name'),
                "last_name": leaf.get('last_name'),
                "username": leaf.get('username'),
                "date_joined": leaf.get('date_joined'),
                "level": leaf.get('level') +1 #max(1, leaf.get('level', 1))  # Valore minimo a 1
            }
            _list.append(user_to_add)

            # Se 'list_referred' esiste, continua ricorsivamente
            list_referred = leaf.get('list_referred', [])
            if list_referred:  # Verifica che ci siano utenti referiti
                tree_to_list(list_referred, _list)  # Chiamata ricorsiva per esplorare i livelli successivi
            #for referred in list_referred:
            #    tree_to_list(referred, _list)  # Chiamata ricorsiva per gli utenti successivi
        else:
            print(f"Warning: Expected a dict, but got {type(leaf)}")
    
    return _list

