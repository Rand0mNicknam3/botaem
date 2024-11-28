from django.urls import path
from chatapp.consumers import WSChatConsumer

ws_urlpatterns = [
    path('ws/chatroom/<chatroom_name>', WSChatConsumer.as_asgi()),
]