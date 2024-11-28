from django.urls import path
from referral.views import get_referred

app_name = 'referral'

urlpatterns = [
    path('<referral_code>', get_referred, name='get_referred'),
]
