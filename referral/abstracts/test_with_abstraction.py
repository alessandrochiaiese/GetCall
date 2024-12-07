
from abc import ABC, abstractmethod
from datetime import datetime

class AbstractReferralAudit(ABC):
    @abstractmethod
    def log_action(self, action_taken, user, ip_address, device_info, location):
        pass


class AbstractReferralBonus(ABC):
    @abstractmethod
    def calculate_bonus(self, num_referrals):
        pass

    @abstractmethod
    def is_eligible(self, user):
        pass


class AbstractReferralCampaign(ABC):
    @abstractmethod
    def track_spending(self, amount):
        pass

    @abstractmethod
    def is_active(self):
        pass


class AbstractReferralCode(ABC):
    @abstractmethod
    def increment_usage(self):
        pass

    @abstractmethod
    def is_valid(self):
        pass


class AbstractReferralConversion(ABC):
    @abstractmethod
    def register_conversion(self, referred_user, conversion_value):
        pass

    @abstractmethod
    def issue_reward(self):
        pass


class AbstractReferralEngagement(ABC):
    @abstractmethod
    def log_interaction(self, action_type):
        pass


class AbstractReferralNotification(ABC):
    @abstractmethod
    def send_notification(self, message, priority):
        pass


class AbstractReferralProgramPartecipation(ABC):
    @abstractmethod
    def join_program(self, referral_code, program):
        pass


class AbstractReferralProgram(ABC):
    @abstractmethod
    def activate(self):
        pass

    @abstractmethod
    def deactivate(self):
        pass


class AbstractReferralReward(ABC):
    @abstractmethod
    def claim_reward(self):
        pass


class AbstractReferralSettings(ABC):
    @abstractmethod
    def update_preferences(self, notification_preference, auto_share_setting):
        pass


class AbstractReferralStats(ABC):
    @abstractmethod
    def calculate_stats(self):
        pass


class AbstractReferralTransaction(ABC):
    @abstractmethod
    def process_transaction(self, transaction_amount, currency):
        pass


class AbstractReferralUser(ABC):
    @abstractmethod
    def update_referral_count(self, is_active):
        pass

    @abstractmethod
    def calculate_loyalty_points(self):
        pass
#################################################
class ReferralCode(AbstractReferralCode):
    def __init__(self, code, expiry_date, usage_count=0):
        self.code = code
        self.expiry_date = expiry_date
        self.usage_count = usage_count

    def increment_usage(self):
        self.usage_count += 1

    def is_valid(self):
        return datetime.now() < self.expiry_date


class ReferralProgram(AbstractReferralProgram):
    def __init__(self, name, reward_type, reward_value, is_active=True):
        self.name = name
        self.reward_type = reward_type
        self.reward_value = reward_value
        self.is_active = is_active

    def activate(self):
        self.is_active = True

    def deactivate(self):
        self.is_active = False


class ReferralBonus(AbstractReferralBonus):
    def __init__(self, bonus_type, bonus_value, min_referrals_required):
        self.bonus_type = bonus_type
        self.bonus_value = bonus_value
        self.min_referrals_required = min_referrals_required

    def calculate_bonus(self, num_referrals):
        if num_referrals >= self.min_referrals_required:
            return self.bonus_value
        return 0

    def is_eligible(self, user):
        # Assume user has an attribute `total_referrals`
        return user.total_referrals >= self.min_referrals_required

########################################
def test():
    from datetime import timedelta

    # Creazione di un programma di referral
    program = ReferralProgram(name="Spring Promo", reward_type="cash", reward_value=50)

    # Creazione di un referral code
    referral_code = ReferralCode(code="SPRING2024", expiry_date=datetime.now() + timedelta(days=30))

    # Creazione di un bonus di referral
    bonus = ReferralBonus(bonus_type="cash", bonus_value=10, min_referrals_required=5)

    # Simulazione di utilizzo del codice
    if referral_code.is_valid():
        referral_code.increment_usage()
        print(f"Code {referral_code.code} has been used {referral_code.usage_count} times.")

    # Calcolo di un bonus
    user_referrals = 7
    bonus_earned = bonus.calculate_bonus(user_referrals)
    print(f"Bonus earned for {user_referrals} referrals: {bonus_earned}")

    # Attivazione e disattivazione del programma
    program.deactivate()
    print(f"Program active: {program.is_active}")
