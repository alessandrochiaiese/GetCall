# affiliate_system/services.py

from affiliate.models import Affiliate, AffiliateLink, AffiliateReward
from django.utils.crypto import get_random_string
from django.contrib.auth import get_user_model

User = get_user_model()

class AffiliateService:
    @staticmethod
    def create_affiliate(user):
        affiliate, created = Affiliate.objects.get_or_create(user=user)
        if created:
            affiliate.code = get_random_string(10)
            affiliate.save()
        return affiliate

    @staticmethod
    def generate_affiliate_link(affiliate_id, url):
        affiliate = Affiliate.objects.get(id=affiliate_id)
        link = AffiliateLink.objects.create(affiliate=affiliate, url=url)
        return link

    @staticmethod
    def add_click(link_id):
        try:
            link = AffiliateLink.objects.get(id=link_id)
            link.clicks += 1
            link.save()
            return link
        except AffiliateLink.DoesNotExist:
            return None

    @staticmethod
    def add_reward(affiliate_id, amount):
        affiliate = Affiliate.objects.get(id=affiliate_id)
        reward = AffiliateReward.objects.create(affiliate=affiliate, amount=amount)
        affiliate.total_rewards += amount
        affiliate.save()
        return reward
