
from datetime import datetime, timedelta

class User:
    def __init__(self, user_id, name, email):
        self.user_id = user_id
        self.name = name
        self.email = email
        self.total_referrals = 0
        self.active_referrals = 0
        self.total_rewards_earned = 0

    def add_referral(self):
        self.total_referrals += 1
        self.active_referrals += 1

    def update_rewards(self, reward_value):
        self.total_rewards_earned += reward_value

class ReferralProgram:
    def __init__(self, program_id, name, reward_type, reward_value, is_active=True):
        self.program_id = program_id
        self.name = name
        self.reward_type = reward_type
        self.reward_value = reward_value
        self.is_active = is_active

    def deactivate(self):
        self.is_active = False

class ReferralCode:
    def __init__(self, code_id, code, user, program, expiry_date):
        self.code_id = code_id
        self.code = code
        self.user = user
        self.program = program
        self.usage_count = 0
        self.referred_user_count = 0
        self.expiry_date = expiry_date

    def increment_usage(self):
        self.usage_count += 1

    def add_referred_user(self):
        self.referred_user_count += 1

    def is_valid(self):
        return datetime.now() < self.expiry_date

class ReferralConversion:
    def __init__(self, conversion_id, referral_code, referred_user, conversion_date, conversion_value):
        self.conversion_id = conversion_id
        self.referral_code = referral_code
        self.referred_user = referred_user
        self.conversion_date = conversion_date
        self.conversion_value = conversion_value
        self.reward_issued = False

    def issue_reward(self):
        self.reward_issued = True

class ReferralBonus:
    def __init__(self, bonus_id, program, min_referrals_required, bonus_value):
        self.bonus_id = bonus_id
        self.program = program
        self.min_referrals_required = min_referrals_required
        self.bonus_value = bonus_value

    def is_eligible(self, referrals_count):
        return referrals_count >= self.min_referrals_required

class ReferralReward:
    def __init__(self, reward_id, referral_code, referred_user, reward_type, reward_value, expiry_date):
        self.reward_id = reward_id
        self.referral_code = referral_code
        self.referred_user = referred_user
        self.reward_type = reward_type
        self.reward_value = reward_value
        self.expiry_date = expiry_date
        self.claimed = False

    def claim(self):
        self.claimed = True

def test():
    ###########################################
    #Scenario Completo con Esempio
    #1. Creazione di un Utente, Programma, e Codice

    # Creazione di un utente
    user1 = User(user_id=1, name="Alice", email="alice@example.com")

    # Creazione di un programma
    program1 = ReferralProgram(program_id=101, name="Spring Promo", reward_type="cash", reward_value=20)

    # Generazione di un codice referral per l'utente
    referral_code1 = ReferralCode(
        code_id=1001,
        code="SPRING2024",
        user=user1,
        program=program1,
        expiry_date=datetime.now() + timedelta(days=30)
    )
    #2. Utilizzo del Codice e Registrazione Conversioni

    # Simula che un nuovo utente usa il codice
    if referral_code1.is_valid():
        referral_code1.increment_usage()
        referral_code1.add_referred_user()

        # Creazione di un nuovo utente referenziato
        referred_user = User(user_id=2, name="Bob", email="bob@example.com")

        # Registrazione della conversione
        conversion = ReferralConversion(
            conversion_id=2001,
            referral_code=referral_code1,
            referred_user=referred_user,
            conversion_date=datetime.now(),
            conversion_value=50
        )
        conversion.issue_reward()

        # Aggiunge i referral all'utente originale
        user1.add_referral()
        user1.update_rewards(program1.reward_value)

    print(f"User {user1.name} now has {user1.total_referrals} referrals.")
    #3. Calcolo dei Bonus

    # Definiamo un bonus
    bonus = ReferralBonus(bonus_id=3001, program=program1, min_referrals_required=5, bonus_value=10)

    # Verifica se l'utente è idoneo per il bonus
    if bonus.is_eligible(user1.total_referrals):
        print(f"User {user1.name} is eligible for a bonus of {bonus.bonus_value}")
    else:
        print(f"User {user1.name} is not yet eligible for the bonus.")
    #4. Emissione di un Premio

    reward = ReferralReward(
        reward_id=4001,
        referral_code=referral_code1,
        referred_user=referred_user,
        reward_type="cash",
        reward_value=program1.reward_value,
        expiry_date=datetime.now() + timedelta(days=90)
    )

    # L'utente riscuote il premio
    reward.claim()

    print(f"Reward claimed: {reward.claimed}")



#test()