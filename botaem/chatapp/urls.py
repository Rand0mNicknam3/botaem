from django.urls import path
from chatapp.views import chat_view

app_name = 'chatapp'

urlpatterns = [
    path('', chat_view, name='chat'),
]