import datetime
import logging
from typing import List
from django.http import JsonResponse
from affiliate.models.affiliate_program import AffiliateProgram
from affiliate.api.serializers import AffiliateProgramSerializer 

# Set up a logger
logger = logging.getLogger(__name__)

class AffiliateProgramService():
    def __init__(self) -> None:
        pass

    def get_affiliate_programs(self) ->  List[AffiliateProgram]:
        try:
            affiliate_programs = AffiliateProgram.objects.all() 
            return affiliate_programs
        except AffiliateProgram.DoesNotExist:
            logger.warning(f"AffiliateProgram not found")
            raise ValueError("AffiliateProgram not found")
     
    def get_affiliate_program(self, pk) -> AffiliateProgram:
        try:
            affiliate_program = AffiliateProgram.objects.get(id=pk)
            return affiliate_program
        except AffiliateProgram.DoesNotExist:
            logger.warning(f"AffiliateProgram not found: {pk}")
            raise ValueError("AffiliateProgram not found")
     
    def create_affiliate_program(self, data) -> AffiliateProgram:
        try:
            affiliate_program = AffiliateProgram(
                name = data.get('name'),
                description = data.get('description'),
                commission_rate = data.get('commission_rate'),
                currency = data.get('currency'),
                min_payout_threshold = data.get('min_payout_threshold'),
                max_payout_limit = data.get('max_payout_limit'),
                date_created = data.get('date_created'),
                is_active = data.get('is_active'),
                duration = data.get('duration'),
                allowed_countries = data.get('allowed_countries'),
                target_industry = data.get('target_industry'))
            affiliate_program.save()
 
            logger.info(f"AffiliateProgram created: {affiliate_program}")
            return affiliate_program
        except Exception as e:
            logger.error(f"Error creating affiliate_program: {e}")
            raise e
 
    def update_affiliate_program(self, pk, data) -> AffiliateProgram:
        try:
            affiliate_program = self.get_affiliate_program(pk)
            for key, value in data.items():
                setattr(affiliate_program, key, value)
            affiliate_program.save()
            logger.info(f"AffiliateProgram updated: {affiliate_program}")
            return affiliate_program
        except Exception as e:
            logger.error(f"Error updating affiliate_program: {e}")
            raise e
    
    def delete_affiliate_program(self, pk) -> None:
        try:
            affiliate_program = self.get_affiliate_program(pk)
            affiliate_program.delete()
            logger.info(f"AffiliateProgram deleted: {affiliate_program}")
        except Exception as e:
            logger.error(f"Error deleting affiliate_program: {e}")
            raise e