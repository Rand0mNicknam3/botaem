import logging
from user.models import CustomUser
from django.contrib.auth.hashers import make_password

logger = logging.getLogger(__name__)


class CustomUserFactory:

    @staticmethod
    def create(username, email, password):
        return CustomUserFactory._create_user({
            'username': username,
            'email': email,
            'password': password
        })
    
    @staticmethod
    def get_by_username(username):
        return CustomUserFactory._get_user({'username': username})
    
    @staticmethod
    def get_image_by_instance(user):
        profile = user.profile
        return profile.image
    
    def _get_user(query):
        try:
            return CustomUser.objects.get(**query)
        except CustomUser.DoesNotExist:
            return None
        except ValueError:
            return None
        except Exception as e:
            logger.error(f'Untracked error while getting user in CustomUserFactory: {e}')
            return None
    
    def _create_user(query):
        try:
            user = CustomUser(**query)
            user.password = make_password(user.password)
            user.full_clean()
            user.save()
            return user
        except Exception as e:
            logger.error(f'Untracked error while creating user in CustomUserFactory: {e}')
            return None