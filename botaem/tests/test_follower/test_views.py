from django.test import TestCase
from django.urls import reverse
from user.models import CustomUser
from myprofile.models import Profile
from follower.models import Follower


class TestFollowerViewsFollow(TestCase):

    @classmethod
    def setUpTestData(cls):
        follower = CustomUser.objects.create(username='follower', email='testemail@example.com', password='testpassword')
        followed = CustomUser.objects.create(username='followed', email='testemail2@example.com', password='testpassword')
        Profile.objects.create(user=followed)
    
    def test_view_follow_fail_get_method_logged_in(self):
        self.client.login(username='followed', password='testpassword')
        response = self.client.get(reverse('follower:follow_user'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('myprofile:main_page'), fetch_redirect_response=False)

    def test_view_follow_fail_get_method_not_logged_in(self):
        response = self.client.get('/follower/follow/', follow=True)
        self.assertEqual(response.status_code, 200)
        redirected_url_full = f'{reverse("user:login")}?next={reverse("myprofile:main_page")}'
        self.assertTemplateUsed(response, 'user/login.html')
        self.assertRedirects(response, redirected_url_full)
    
    def test_view_follow_success(self):
        self.client.login(username='follower', password='testpassword')
        follower = CustomUser.objects.get(username='follower')
        followed = CustomUser.objects.get(username='followed')
        response = self.client.post(reverse('follower:follow_user'), data={'follower': follower.username, 'followed': followed.username})
        self.assertEqual(response.status_code, 200)
    
    def test_view_follow_fail_wrong_follower(self):
        self.client.login(username='follower', password='testpassword')
        follower = CustomUser.objects.get(username='follower')
        followed = CustomUser.objects.get(username='followed')
        response = self.client.post(reverse('follower:follow_user'), data={'follower': 'wrong', 'followed': followed.username})
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'{"status": "fail", "redirectUrl": "/follower/errors/"}', response.content)

    def test_view_follow_fail_wrong_followed(self):
        self.client.login(username='follower', password='testpassword')
        follower = CustomUser.objects.get(username='follower')
        followed = CustomUser.objects.get(username='followed')
        response = self.client.post(reverse('follower:follow_user'), data={'follower': follower.username, 'followed': 'wrong'})
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'{"status": "fail", "redirectUrl": "/follower/errors/"}', response.content)
    
    def test_view_follow_fail_wrong_data(self):
        self.client.login(username='follower', password='testpassword')
        follower = CustomUser.objects.get(username='follower')
        followed = CustomUser.objects.get(username='followed')
        response = self.client.post(reverse('follower:follow_user'), data={'follower': 'wrong', 'followed': 'wrong'})
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'{"status": "fail", "redirectUrl": "/follower/errors/"}', response.content)


class TestFollowerViewsUnfollow(TestCase):

    @classmethod
    def setUpTestData(cls):
        follower = CustomUser.objects.create(username='follower', email='testemail@example.com', password='testpassword')
        followed = CustomUser.objects.create(username='followed', email='testemail2@example.com', password='testpassword')
        Profile.objects.create(user=followed)
        Follower.objects.create(user=followed, follower=follower)
    
    def test_view_unfollow_fail_get_method_logged_in(self):
        self.client.login(username='followed', password='testpassword')
        response = self.client.get(reverse('follower:unfollow_user'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('myprofile:main_page'), fetch_redirect_response=False)

    def test_view_unfollow_fail_get_method_not_logged_in(self):
        response = self.client.get('/follower/unfollow/', follow=True)
        self.assertEqual(response.status_code, 200)
        redirected_url_full = f'{reverse("user:login")}?next={reverse("myprofile:main_page")}'
        self.assertTemplateUsed(response, 'user/login.html')
        self.assertRedirects(response, redirected_url_full)
    
    def test_view_unfollow_success(self):
        self.client.login(username='follower', password='testpassword')
        follower = CustomUser.objects.get(username='follower')
        followed = CustomUser.objects.get(username='followed')
        response = self.client.post(reverse('follower:unfollow_user'), data={'follower': follower.username, 'followed': followed.username})
        self.assertEqual(response.status_code, 200)
    
    def test_view_unfollow_fail_wrong_follower(self):
        self.client.login(username='follower', password='testpassword')
        CustomUser.objects.get(username='follower')
        followed = CustomUser.objects.get(username='followed')
        response = self.client.post(reverse('follower:unfollow_user'), data={'follower': 'wrong', 'followed': followed.username})
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'{"status": "fail", "redirectUrl": "/follower/errors/"}', response.content)

    def test_view_unfollow_fail_wrong_followed(self):
        self.client.login(username='follower', password='testpassword')
        follower = CustomUser.objects.get(username='follower')
        CustomUser.objects.get(username='followed')
        response = self.client.post(reverse('follower:unfollow_user'), data={'follower': follower.username, 'followed': 'wrong'})
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'{"status": "fail", "redirectUrl": "/follower/errors/"}', response.content)
    
    def test_view_unfollow_fail_wrong_data(self):
        self.client.login(username='follower', password='testpassword')
        CustomUser.objects.get(username='follower')
        CustomUser.objects.get(username='followed')
        response = self.client.post(reverse('follower:unfollow_user'), data={'follower': 'wrong', 'followed': 'wrong'})
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'{"status": "fail", "redirectUrl": "/follower/errors/"}', response.content)

class TestFollowerViewsErrors(TestCase):
    
    def test_view_errors_existing(self):
        response = self.client.get('/follower/errors/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'follower/errors.html')


    def test_view_errors_existing_reverse(self):
        response = self.client.get(reverse('follower:errors'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'follower/errors.html')