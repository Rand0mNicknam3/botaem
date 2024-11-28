import logging
from django.shortcuts import redirect
from django.urls import reverse
from referral.factories import ReferralCodeFactory

logger = logging.getLogger(__name__)


def get_referred(request, referral_code):
    user = ReferralCodeFactory.get_user_by_code(referral_code)
    if user:
        request.session['referred_by'] = user.username
    else:
        logger.error('Tried to get user by code, but code does not exists', extra={'referral_code': referral_code})
    return redirect(reverse('user:register'))


