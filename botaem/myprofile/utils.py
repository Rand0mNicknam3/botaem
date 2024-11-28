from django.urls import reverse


def profile_image_path(instance, filename):
    return f'profile_images/{instance.user.username}/{instance.id}/{filename}'

def full_ref_link(request, code):
    refurl = reverse('referral:get_referred', kwargs={'referral_code': code})
    absolute_url = request.build_absolute_uri(refurl)
    return absolute_url