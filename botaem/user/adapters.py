from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from myprofile.factories import ProfileFactory

class CustomAccountAdapter(DefaultSocialAccountAdapter):
    
    def save_user(self, request, sociallogin, form=None):
        super().save_user(request, sociallogin, form)
        user = sociallogin.user
        ProfileFactory.create(user=user)
        return user