from django.urls import path
from user.views import register_user, login_user, logout_user

app_name = 'user'

urlpatterns = [
    path('register', register_user, name='register'),
    path('login', login_user, name='login'),
    path('logout', logout_user, name='logout'),
]