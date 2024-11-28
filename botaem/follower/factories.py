import logging
from django.forms import ValidationError
from user.models import CustomUser
from follower.models import Follower
from user.factories import CustomUserFactory

logger = logging.getLogger(__name__)

class FollowerFactory:

    @staticmethod
    def create(followed, follower):
        return FollowerFactory._create_follower({'user': followed, 'follower': follower})
    
    @staticmethod
    def remove(followed, follower):
        return FollowerFactory._remove_follower({'user': followed, 'follower': follower})
    
    
    @staticmethod
    def get_followers_count_by_slug(slug):
        try:
            user = CustomUserFactory.get_by_username(slug)
            return user.followers.count()
        except CustomUser.DoesNotExist:
            logger.error('Tried to get user followers, but user does not exists')
            return None
        except Exception as e:
            logger.critical(f'{e} while getting user followers in FollowerFactory')
            return None
    
    def _remove_follower(query):
        try:
            return Follower.objects.filter(**query).delete()
        except ValueError as e:
            logger.error(f'ValueError while removing follower in FollowerFactory')
        except Exception as e:
            logger.error(f'{e} while removing follower in FollowerFactory')
            return None

    def _create_follower(query):
        try:
            follow_pair = Follower(**query)
            follow_pair.full_clean()
            follow_pair.save()
            return follow_pair
        except ValidationError as e:
            logger.error('ValidationError while creating follower in FollowerFactory', extra={'errors': e.messages})
            return None
        except Exception as e:
            logger.error(f'{e} while creating follower in FollowerFactory')
            return None