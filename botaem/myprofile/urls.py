from django.urls import path
from myprofile.views import myprofile_main, upload_avatar, upload_bio, get_refcode

app_name = 'myprofile'

urlpatterns = [
    path('', myprofile_main, name='main_page'),
    path('upload_avatar', upload_avatar, name='upload_avatar'),
    path('upload_bio', upload_bio, name='upload_bio'),
    path('get_refcode', get_refcode, name='get_refcode'),
    ]