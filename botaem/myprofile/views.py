from django.http import JsonResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from myprofile.factories import ProfileFactory
from myprofile.decorators import require_post_redirect
from referral.factories import ReferralCodeFactory
from myprofile.utils import full_ref_link
import logging

logger = logging.getLogger(__name__)


@login_required()
def myprofile_main(request):
    user_profile = ProfileFactory.get_profile(user=request.user)
    logger.info(
        'Got get request for main_page',
        extra={'user': request.user.username}
    )
    context = {
        'user': request.user,
        'profile': user_profile,
    }
    return render(request, 'myprofile/main_page.html', context=context)


@login_required
@require_post_redirect('myprofile:main_page')
def upload_avatar(request):
    logger.info('we got post request in upload_avatar')
    if 'image' not in request.FILES:
        logger.info('Request does not contain image', extra={'user': request.user.username})
        return JsonResponse(data={'status': 'fail', 'error': 'Image is required'})
    image = request.FILES['image']
    uploaded_image = ProfileFactory.add_image(user=request.user, image=image)
    if not uploaded_image:
        logger.info('Request with too big image', extra={'user': request.user.username})
        return JsonResponse(data={'status': 'fail', 'error': 'Image is too big'})
    logger.info('Image uploaded', extra={'user': request.user.username})
    return JsonResponse(data={'status': 'success'})

    
@login_required
@require_post_redirect('myprofile:main_page')
def upload_bio(request):
    logger.info('we got post request in upload_bio')
    if 'bio' not in request.POST:
        logger.info('Request does not contain bio', extra={'user': request.user.username})
        return JsonResponse(data={'status': 'fail', 'error': 'Bio is required'})
    bio = request.POST['bio']
    uploaded_bio = ProfileFactory.add_bio(user=request.user, bio=bio)
    if not uploaded_bio:
        logger.info('Too big bio', extra={'user': request.user.username})
        return JsonResponse(data={'status': 'fail', 'error': 'Bio is too big'})
    return JsonResponse(data={'status': 'success'})


@login_required
def get_refcode(request):
    logger.info('we got get request in get_refcode')
    refcode = ReferralCodeFactory.get_code_or_create(user=request.user)
    reflink = full_ref_link(request, refcode)
    logger.info('Responding with reflink', extra={'reflink': reflink})
    return JsonResponse(data={'status': 'success', 'refcode': reflink})
