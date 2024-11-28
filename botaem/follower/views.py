from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from myprofile.decorators import require_post_redirect
from follower.factories import FollowerFactory
from user.factories import CustomUserFactory
import logging

logger = logging.getLogger(__name__)

# View to follow a user
@require_post_redirect('myprofile:main_page')
def follow_user(request):
    if request.method == 'POST':
        validate = _check_post_contains_follower_and_followed(request)
        if not validate:
            return _render_errors(request)
        follower, followed = _check_follower_and_followed_valid(**validate)
        if follower is None or followed is None:
            return _render_errors(request)
        FollowerFactory.create(followed, follower)
        logger.info('Followed user', extra={'follower': follower.username, 'followed': followed.username})
        return JsonResponse({'status': 'success', 'redirectUrl' : reverse('publicprofile:main_page', args=[followed.username])})


# View to unfollow a user
@require_post_redirect('myprofile:main_page')
def unfollow_user(request):
    if request.method == 'POST':
        logger.info('got request for unfollowing')
        validate = _check_post_contains_unfollower_and_unfollowed(request)
        if not validate:
            return _render_errors(request)
        unfollower, unfollowed = _check_follower_and_followed_valid(**validate)
        if unfollower is None or unfollowed is None:
            return _render_errors(request)
        FollowerFactory.remove(unfollowed, unfollower)
        logger.info('Unfollowed user', extra={'unfollower': unfollower.username, 'unfollowed': unfollowed.username})
        return JsonResponse({'status': 'success', 'redirectUrl': reverse('publicprofile:main_page', args=[unfollowed.username])})


# View to show error page (User can probably get it only using url/postman request to other views)
def error_page(request, messages=None):
    return render(request, 'follower/errors.html', {'messages': messages})

# Methods for following/unfollowing (2 of them are universal)
def _check_post_contains_follower_and_followed(request):
    follower = request.POST.get('follower')
    followed = request.POST.get('followed')
    if follower is None or followed is None:
        return None
    return {
        'follower': follower,
        'followed': followed
    }

def _check_post_contains_unfollower_and_unfollowed(request):
    follower = request.POST.get('unfollower')
    followed = request.POST.get('unfollowed')
    if follower is None or followed is None:
        return None
    return {
        'follower': follower,
        'followed': followed
    }

def _check_follower_and_followed_valid(follower, followed):
    validate_follower = CustomUserFactory.get_by_username(follower)
    validate_followed = CustomUserFactory.get_by_username(followed)
    if validate_followed and validate_follower:
        return validate_follower, validate_followed
    return None, None

def _render_errors(request):
        logger.info('Not valid data for following/unfollowing')
        return JsonResponse({'status': 'fail', 'redirectUrl' : reverse('follower:errors')})