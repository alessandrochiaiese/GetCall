from typing import List
from django.shortcuts import get_object_or_404
from affiliate.models.affiliate import Affiliate
from affiliate.models.affiliate_program import AffiliateProgram
from affiliate.models.affiliate_program_partecipation import AffiliateProgramPartecipation
from affiliate.api.serializers import AffiliateProgramPartecipationSerializer 

import logging
logger = logging.getLogger(__name__)

class AffiliateProgramPartecipationService():
    def __init__(self) -> None:
        pass

    def get_affiliate_program_partecipations(self) -> List[AffiliateProgramPartecipation]:
        try:
            affiliate_program_partecipations = AffiliateProgramPartecipation.objects.all()
            return affiliate_program_partecipations
        except Exception as e:
            logger.warning(f"Error fetching affiliate_program_partecipations: {e}")
            raise e

    def get_affiliate_program_partecipation(self, pk) -> AffiliateProgramPartecipation:
        try:
            affiliate_program_partecipation = get_object_or_404(AffiliateProgramPartecipation, id=pk)
            return affiliate_program_partecipation
        except AffiliateProgramPartecipation.DoesNotExist as e:
            logger.warning(f"AffiliateProgramPartecipation not found: {pk}")
            raise e
        except Exception as e:
            logger.error(f"Error fetching affiliate_program_partecipation: {e}")
            raise e

    # Le altre funzioni rimangono invariate.

    def create_affiliate_program_partecipation(self, data) -> AffiliateProgramPartecipation:
        try:
            affiliate_program_partecipation = AffiliateProgramPartecipation(
                affiliate = data.get('affiliate'),
                program = data.get('program'),
                date_joined = data.get('date_joined'),
                commission_earned = data.get('commission_earned'),
                status = data.get('status'))
            affiliate_program_partecipation.save()
 
            logger.info(f"AffiliateProgramPartecipation created: {affiliate_program_partecipation}")
            return affiliate_program_partecipation
        except Exception as e:
            logger.error(f"Error creating affiliate_program_partecipation: {e}")
            raise e
 
    def update_affiliate_program_partecipation(self, pk, data) -> AffiliateProgramPartecipation:
        try:
            affiliate_program_partecipation = self.get_affiliate_program_partecipation(pk)
            for key, value in data.items():
                setattr(affiliate_program_partecipation, key, value)
            affiliate_program_partecipation.save()
            logger.info(f"AffiliateProgramPartecipation updated: {affiliate_program_partecipation}")
            return affiliate_program_partecipation
        except Exception as e:
            logger.error(f"Error updating affiliate_program_partecipation: {e}")
            raise e
    
    def delete_affiliate_program_partecipation(self, pk) -> None:
        try:
            affiliate_program_partecipation = self.get_affiliate_program_partecipation(pk)
            affiliate_program_partecipation.delete()
            logger.info(f"AffiliateProgramPartecipation deleted: {affiliate_program_partecipation}")
        except Exception as e:
            logger.error(f"Error deleting affiliate_program_partecipation: {e}")
            raise e