# referral_system/services.py

from referral.models import ReferralProgram, Referral, ReferralReward
from django.contrib.auth import get_user_model

User = get_user_model()

class ReferralService:
    @staticmethod
    def create_referral_program(name, reward_amount, active=True):
        program = ReferralProgram.objects.create(name=name, reward_amount=reward_amount, active=active)
        return program

    @staticmethod
    def create_referral(program_id, referrer_id, referred_id):
        program = ReferralProgram.objects.get(id=program_id)
        referrer = User.objects.get(id=referrer_id)
        referred = User.objects.get(id=referred_id)
        referral = Referral.objects.create(program=program, referrer=referrer, referred=referred)
        return referral

    @staticmethod
    def reward_referral(referral_id, amount):
        referral = Referral.objects.get(id=referral_id)
        reward = ReferralReward.objects.create(referral=referral, amount=amount)
        referral.reward_given = True
        referral.save()
        return reward
