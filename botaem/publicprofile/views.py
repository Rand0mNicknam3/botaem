import logging
from django.shortcuts import render, get_object_or_404
from myprofile.models import Profile
from follower.factories import FollowerFactory

logger = logging.getLogger(__name__)

def publicprofile_main(request, slug):
    logger.info(f'Got request for publicprofile_main', extra={'slug': slug})
    user_profile = get_object_or_404(Profile, slug=slug)
    followers = FollowerFactory.get_followers_count_by_slug(slug)
    is_authenticated = request.user.is_authenticated
    is_followed = False
    if is_authenticated:
        is_followed = user_profile.is_followed(request.user)
    context = {
        'profile': user_profile,
        'is_followed': is_followed,
        'followers': followers,
        'is_authenticated': is_authenticated
    }
    return render(request, 'publicprofile/main_page.html', context=context)