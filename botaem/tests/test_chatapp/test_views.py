import logging
from django.test import TestCase
from django.urls import reverse
from chatapp.models import GroupMessage, ChatGroup
from user.models import CustomUser

logger = logging.getLogger(__name__)

class TestChatappViewsChatView(TestCase):

    @classmethod
    def setUpTestData(cls):
        user = CustomUser.objects.create_user(username='testuser', email='testemail@example.com', password='testpassword')
        chat_group, created = ChatGroup.objects.get_or_create(group_name='base', groupchat_name='based_chat')
        GroupMessage.objects.create(author=user, body='test_message', group=chat_group)
        if created:
            logger.info('Chat was created !')
        else:
            logger.info('Chat was already created by initial_data.py, appreciate it ! :)')
    
    def test_view_not_logged_in(self):
        response = self.client.get('/chat/')
        self.assertEqual(response.status_code, 302)\
    
    def test_view_logged_in_success(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get('/chat/')
        self.assertEqual(response.status_code, 200)
    
    def test_view_uses_correct_template(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get('/chat/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'chatapp/main_page.html')

    def test_view_accessible_by_name(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('chatapp:chat'))
        self.assertEqual(response.status_code, 200)
    
    def test_view_message_is_avaliable(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('chatapp:chat'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['chat_messages'].count(), 1)