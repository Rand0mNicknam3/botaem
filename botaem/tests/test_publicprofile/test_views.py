from django.test import TestCase
from django.urls import reverse
from user.models import CustomUser
from myprofile.models import Profile
from follower.models import Follower


class TestPublicProfileViews(TestCase):

    @classmethod
    def setUpTestData(cls):
        user = CustomUser.objects.create(username='testuser', email='testemail@example.com', password='testpassword')
        Profile.objects.create(user=user)
    
    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/profile/testuser')
        self.assertEqual(response.status_code, 200)
    
    def test_view_accessible_by_name(self):
        response = self.client.get(reverse('publicprofile:main_page', kwargs={'slug': 'testuser'}))
        self.assertEqual(response.status_code, 200)
    
    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('publicprofile:main_page', kwargs={'slug': 'testuser'}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'publicprofile/main_page.html')
    
    def test_view_logged_in_user(self):
        self.client.force_login(user=CustomUser.objects.get(username='testuser'))
        response = self.client.get(reverse('publicprofile:main_page', kwargs={'slug': 'testuser'}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'publicprofile/main_page.html')
        self.assertEqual(response.context['is_authenticated'], True)
    
    def test_view_logged_in_user_followcount(self):
        self.client.force_login(user=CustomUser.objects.get(username='testuser'))
        main_user = CustomUser.objects.get(username='testuser')
        follower = CustomUser.objects.create(username='follower', email='testemail2@example.com', password='testpassword')
        Follower.objects.create(user=main_user, follower=follower)
        response = self.client.get(reverse('publicprofile:main_page', kwargs={'slug': 'testuser'}))
        self.assertEqual(main_user.followers.count(), 1)
        self.assertEqual(response.status_code, 200)
    
    def test_view_logged_in_user_isfollowed_true(self):
        self.client.force_login(user=CustomUser.objects.get(username='testuser'))
        main_user_follower = CustomUser.objects.get(username='testuser')
        followed = CustomUser.objects.create(username='followed', email='testemail2@example.com', password='testpassword')
        Follower.objects.create(user=followed, follower=main_user_follower)
        Profile.objects.create(user=followed)
        response = self.client.get(reverse('publicprofile:main_page', kwargs={'slug': 'followed'}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['is_followed'], True)
    
    def test_view_profile_does_not_exist(self):
        self.client.force_login(user=CustomUser.objects.get(username='testuser'))
        response = self.client.get(reverse('publicprofile:main_page', kwargs={'slug': 'wrong'}))
        self.assertEqual(response.status_code, 404)
        