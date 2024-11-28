from django.urls import path
from follower.views import follow_user, unfollow_user, error_page

app_name = 'follower'

urlpatterns = [
    path('follow/', follow_user, name='follow_user'),
    path('unfollow/', unfollow_user, name='unfollow_user'),
    path('errors/', error_page, name='errors'),
]