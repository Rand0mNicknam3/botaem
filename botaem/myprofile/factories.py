import logging
from user.models import CustomUser
from myprofile.models import Profile

logger = logging.getLogger(__name__)

class ProfileFactory:

    @staticmethod
    def create(user):
        return ProfileFactory._create_profile(user)
    
    @staticmethod
    def add_image(user, image):
        print(f' add_image func {user} {image}')
        return ProfileFactory._update_profile(user, image=image)
    
    @staticmethod
    def add_bio(user, bio):
        return ProfileFactory._update_profile(user, bio=bio)

    @staticmethod
    def add_location(user, location):
        return ProfileFactory._update_profile(user, location=location)

    @staticmethod
    def add_birth_date(user, birth_date):
        return ProfileFactory._update_profile(user, birth_date=birth_date)
    
    @staticmethod
    def get_profile(user):
        return ProfileFactory._get_profile({'user': user})
    
    def _get_profile(query):
        try:
            return Profile.objects.get(**query)
        except Exception as e:
            logger.error(f'{e} while getting profile in ProfileFactory')
            return None
    
    def _create_profile(user):
        if isinstance(user, CustomUser):
            return Profile.objects.create(user=user)
        else:
            return None
        
    def _update_profile(user, **kwargs):
        print(f' add_image func {user} {kwargs}')
        if isinstance(user, CustomUser):
            profile = Profile.objects.get(user=user)
            for key, value in kwargs.items():
                setattr(profile, key, value)
            try:
                profile.full_clean()
                profile.save()
                return profile
            except Exception as e:
                logger.error(f'{e} while updating profile in ProfileFactory')
                return None
        return None