from django.contrib.messages.test import MessagesTestMixin
from django.test import TestCase
from django.urls import reverse
from user.models import CustomUser
from django.contrib.messages.storage.base import Message


class TestUserViewsLogin(MessagesTestMixin, TestCase):
    
    @classmethod
    def setUpTestData(cls):
        CustomUser.objects.create_user(username='testuser', email='testemail@example.com', password='testpassword')

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/auth/login')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('user:login'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('user:login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'user/login.html')

    def test_view_login_user_success(self):
        self.client.post(reverse('user:login'), {'username': 'testuser', 'password': 'testpassword'})
        self.assertTrue('_auth_user_id' in self.client.session)
        self.assertEqual(self.client.session['_auth_user_id'], str(CustomUser.objects.get(username='testuser').id))
    
    def test_view_login_user_wrong_password(self):
        response = self.client.post(reverse('user:login'), {'username': 'testuser', 'password': 'wrongpassword'})
        self.assertFalse('_auth_user_id' in self.client.session)
        self.assertMessages(response, [Message(level=20, message='Username or password is incorrect')])

    def test_view_login_user_wrong_username(self):
        response = self.client.post(reverse('user:login'), {'username': 'wronguser', 'password': 'testpassword'})
        self.assertFalse('_auth_user_id' in self.client.session)
        self.assertMessages(response, [Message(level=20, message='Username or password is incorrect')])


class TestUserViewsRegister(MessagesTestMixin, TestCase):

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/auth/register')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('user:register'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('user:register'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'user/register.html')
    
    def test_view_register_user_success(self):
        self.client.post(reverse('user:register'), {'username': 'testuser', 'email': 'testemail@example.com', 'password1': 'testpassword', 'password2': 'testpassword'})
        self.assertTrue(CustomUser.objects.filter(username='testuser').exists())

    def test_view_register_user_wrong_second_password(self):
        response = self.client.post(reverse('user:register'), {'username': 'testuser', 'email': 'testemail@example.com', 'password1': 'testpassword', 'password2': 'wrongpassword'})
        self.assertFalse(CustomUser.objects.filter(username='testuser').exists())
        self.assertFormError(response.context['form'], 'password2', 'The two password fields didn’t match.')


    def test_view_register_user_wrong_email(self):
        CustomUser.objects.create(username='testuser2', email='testemail@example.com', password='testpassword')
        response = self.client.post(reverse('user:register'), {'username': 'testuser', 'email': 'testemail@example.com', 'password1': 'testpassword', 'password2': 'testpassword'})
        self.assertFalse(CustomUser.objects.filter(username='testuser').exists())
        self.assertFormError(response.context['form'], 'email', 'User with this Email address already exists.')
    