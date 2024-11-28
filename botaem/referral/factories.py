import logging
import uuid
from referral.models import ReferralCode, ReferralRelationship

logger = logging.getLogger(__name__)

class ReferralRelationshipFactory:
    
    @staticmethod
    def create(inviter, invitee):
        return ReferralRelationshipFactory._create_relationship({'inviter': inviter, 'invitee': invitee})
    
    def _create_relationship(query):
        try:
            relationship = ReferralRelationship(**query)
            relationship.full_clean()
            relationship.save()
            return relationship
        except Exception as e:
            logger.error(f'{e} while creating relationship in ReferralRelationshipFactory')
            return None


class ReferralCodeFactory:

    @staticmethod
    def get_code_or_create(user):
        if ReferralCode.objects.filter(user=user).exists():
            return ReferralCode.objects.get(user=user).token
        return ReferralCodeFactory.create(user).token
    
    @staticmethod
    def get_user_by_code(code):
        try:
            return ReferralCode.objects.get(token=code).user
        except ReferralCode.DoesNotExist:
            logger.error('Tried to get user by code, but code does not exists')
            return None
        except Exception as e:
            logger.critical(f'{e} while getting user by code in ReferralCodeFactory')
            return None

    @staticmethod
    def create(user):
        return ReferralCodeFactory._create_code({'user': user})
    
    def _create_code(query):
        try:
            code = ReferralCode(**query)
            code.token = str(uuid.uuid4())[:15]
            code.full_clean()
            code.save()
            return code
        except Exception as e:
            logger.error(f'{e} while creating code in ReferralCodeFactory')
            return None
    
    