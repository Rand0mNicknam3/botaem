from django.test import TestCase
from asgiref.sync import sync_to_async
from channels.testing import WebsocketCommunicator
from user.models import CustomUser
from myprofile.models import Profile
from chatapp.consumers import WSChatConsumer
from tests.test_chatapp.consumerdata import get_headers_and_scope, make_communicator_scope

# ATTENTION ! This test is so hardcored(check get_headers_and_scope) that I'm not even sure how it suppose to work
# I can't do it better now :(
# PS made it better 3 times already, still worst shit ever but alreast works now XD
class ChatConsumerTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        user = CustomUser.objects.create_user(username='testuser', email='testemail@example.com', password='testpassword')
        Profile.objects.create(user=user)
        user2 = CustomUser.objects.create_user(username='testuser2', email='testemail2@example.com', password='testpassword')
        Profile.objects.create(user=user2)
        
    async def test_consumer_connection(self):
        user = await sync_to_async(CustomUser.objects.get)(username='testuser')
        headers, scope = await get_headers_and_scope(self, user)
        communicator = WebsocketCommunicator(WSChatConsumer.as_asgi(), path="/ws/chatroom/based_chat", headers=headers)
        communicator = await make_communicator_scope(communicator, scope)
        connected, subprotocol = await communicator.connect()
        assert connected
        await communicator.disconnect()
    
    async def test_consumer_send_data(self):
        user = await sync_to_async(CustomUser.objects.get)(username='testuser')
        headers, scope = await get_headers_and_scope(self, user)
        communicator = WebsocketCommunicator(WSChatConsumer.as_asgi(), path="/ws/chatroom/based_chat", headers=headers)
        communicator = await make_communicator_scope(communicator, scope)
        await communicator.connect()
        response = await communicator.receive_json_from()
        self.assertTrue(response['type'] == 'online_users')
        await communicator.send_json_to({'type': 'chat_message', 'message': 'test_message'})
        response = await communicator.receive_json_from()
        self.assertTrue(response['type'] == 'message_to_show')
        self.assertIn('test_message', response['message'])
        await communicator.disconnect()
    
    async def test_consumer_remove_online_when_disconnect(self):
        user = await sync_to_async(CustomUser.objects.get)(username='testuser')
        user2 = await sync_to_async(CustomUser.objects.get)(username='testuser2')
        headers, scope = await get_headers_and_scope(self, user)
        headers2, scope2 = await get_headers_and_scope(self, user2)
        communicator = WebsocketCommunicator(WSChatConsumer.as_asgi(), path="/ws/chatroom/based_chat", headers=headers)
        communicator = await make_communicator_scope(communicator, scope)
        communicator2 = WebsocketCommunicator(WSChatConsumer.as_asgi(), path="/ws/chatroom/based_chat", headers=headers2)
        communicator2 = await make_communicator_scope(communicator2, scope2)
        await communicator.connect()
        await communicator2.connect()
        response = await communicator.receive_json_from()
        self.assertTrue(response['type'] == 'online_users')
        response2 = await communicator2.receive_json_from()
        self.assertTrue(response2['type'] == 'online_users')
        await communicator2.disconnect()
        await communicator.receive_json_from()
        response = await communicator.receive_json_from()
        self.assertNotIn(user2.username, response['users'])
        self.assertIn(user.username, response['users'])
        await communicator.disconnect()
    
