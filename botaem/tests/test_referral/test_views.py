from django.test import TestCase
from django.urls import reverse

from user.models import CustomUser
from referral.models import ReferralCode, ReferralRelationship


class TestReferralGetReffered(TestCase):

    @classmethod
    def setUpTestData(cls):
        user = CustomUser.objects.create_user(username='testuser', email='testemail@example.com', password='testpassword')
        ReferralCode.objects.create(user=user, token='testtoken')
    
    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/rf/testtoken')
        self.assertRedirects(response, reverse('user:register'))
    
    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('referral:get_referred', kwargs={'referral_code': 'testtoken'}))
        self.assertRedirects(response, reverse('user:register'))
        
    def test_view_get_referred_success(self):
        response = self.client.get(reverse('referral:get_referred', kwargs={'referral_code': 'testtoken'}), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'user/register.html')
        self.assertIn('referred_by', self.client.session)
        self.assertEqual(self.client.session['referred_by'], 'testuser')
    
    def test_view_get_referred_fail_wrong_code(self):
        response = self.client.get(reverse('referral:get_referred', kwargs={'referral_code': 'wrongtoken'}), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'user/register.html')
        self.assertNotIn('referred_by', self.client.session)

