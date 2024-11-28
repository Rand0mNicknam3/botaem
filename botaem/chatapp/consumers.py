import json
import logging
from asgiref.sync import sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from datetime import datetime
from chatapp.factories import GroupMessageFactory
from chatapp.models import ChatGroup
from user.factories import CustomUserFactory
from django.core import serializers
from chatapp.utils import get_html_for_online_users

logger = logging.getLogger(__name__)

# TODO Refactor this shit one day
class WSChatConsumer(AsyncWebsocketConsumer):
    
    async def connect(self):
        self.user = self.scope['user']
        logger.info('connection called for user', extra={'user': self.user})
        self.chatroom_name = self.scope["url_route"]["kwargs"]["chatroom_name"]
        self.room_group_name = f"chat_{self.chatroom_name}"
        self.chatroom = await sync_to_async(get_object_or_404)(ChatGroup, groupchat_name=self.chatroom_name)
        await self.channel_layer.group_add(
            self.room_group_name, self.channel_name
        )
        if await sync_to_async(self.chatroom.users_online.all)() != self.user:
            await sync_to_async(self.chatroom.users_online.add)(self.user)
            await self.update_online_users()
        await self.accept()

    async def disconnect(self, close_code):
        logger.info("disconnect called", extra={'user': self.user})
        await self.channel_layer.group_discard(
            self.room_group_name, self.channel_name
        )
        if await sync_to_async(self.chatroom.users_online.all)() != self.user:
            await sync_to_async(self.chatroom.users_online.remove)(self.user)
            await self.update_online_users()

    async def update_online_users(self):
        online_users = await sync_to_async(self.chatroom.users_online.all)()
        html = await get_html_for_online_users(online_users)
        event = {
            'online_users': html,
            'type': 'get_connected_clients'
        }
        await self.channel_layer.group_send(
            self.room_group_name, event
        )
        
    async def receive(self, text_data):
        logger.info('receive called', extra={'user': self.user})
        text_data_json = json.loads(text_data)
        if text_data_json['type'] == 'chat_message':
            message = text_data_json["message"]
            logger.info('recieved message', extra={'message_text': message, 'user': self.user})
            await sync_to_async(GroupMessageFactory.create)(
                author=self.user,
                group=self.chatroom,
                body=message)
            image = await sync_to_async(CustomUserFactory.get_image_by_instance)(self.user)
            context = {
                'message': message,
                'username': self.user,
                'chat_group': self.chatroom,
                'time': f'{datetime.now().strftime("%H:%M")}',
                'image': image
            }
            html = await sync_to_async(render_to_string)("chatapp/message_gen.html", context=context)
            await self.channel_layer.group_send(
                self.room_group_name, {"type": "chat_message", "message": html}
            )
        if text_data_json['type'] == 'online_users':
            online_users = await sync_to_async(self.chatroom.users_online.all)()
            html = await get_html_for_online_users(online_users)
            logger.info('online_users called', extra={'user': self.user})
            await self.channel_layer.group_send(
                self.room_group_name, {"type": "get_connected_clients", "online_users": html}
            )

    async def chat_message(self, event):
        logger.info('chat_message called (event)')
        message = event["message"]
        await self.send(text_data=json.dumps({
            'type': 'message_to_show',
            'message': message,
        }))


    async def get_connected_clients(self, event):
        logger.info('get_connected_clients called (event)')
        online_users = event['online_users']
        await self.send(text_data=json.dumps({
            'type': 'online_users',
            'users': online_users,
        }))