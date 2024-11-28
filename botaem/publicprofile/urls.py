from django.urls import path
from publicprofile.views import publicprofile_main

app_name = 'publicprofile'

urlpatterns = [
    path('<slug:slug>', publicprofile_main, name='main_page'),
]