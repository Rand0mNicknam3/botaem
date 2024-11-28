from django.test import TestCase
from referral.factories import ReferralRelationshipFactory, ReferralCodeFactory
from referral.models import ReferralCode, ReferralRelationship
from user.models import CustomUser


class TestReferralRelationshipFactory(TestCase):
    @classmethod
    def setUpTestData(cls):
        CustomUser.objects.create_user(username='testuser', email='testemail@example.com', password='testpassword')
        CustomUser.objects.create_user(username='testuser2', email='testemail2@example.com', password='testpassword')

    def test_relationship_create_success(self):
        inviter = CustomUser.objects.get(username='testuser')
        invitee = CustomUser.objects.get(username='testuser2')
        ReferralRelationshipFactory.create(inviter=inviter, invitee=invitee)
        self.assertTrue(ReferralRelationship.objects.filter(inviter=inviter).exists())
    
    def test_relationship_create_fail(self):
        inviter = CustomUser.objects.get(username='testuser')
        invitee = None
        ReferralRelationshipFactory.create(inviter=inviter, invitee=invitee)
        self.assertFalse(ReferralRelationship.objects.filter(inviter=inviter).exists())


class TestReferralCodeFactory(TestCase):
    @classmethod
    def setUpTestData(cls):
        CustomUser.objects.create_user(username='testuser', email='testemail@example.com', password='testpassword')
        CustomUser.objects.create_user(username='testuser2', email='testemail2@example.com', password='testpassword')

    def test_code_create_success(self):
        user = CustomUser.objects.get(username='testuser')
        ReferralCodeFactory.create(user=user)
        self.assertTrue(ReferralCode.objects.filter(user=user).exists())
    
    def test_get_user_by_code_success(self):
        ReferralCode.objects.create(user=CustomUser.objects.get(username='testuser'), token='testtoken')
        user = ReferralCodeFactory.get_user_by_code('testtoken')
        self.assertEqual(user.username, 'testuser')
    
    def test_get_user_by_code_fail_not_exists(self):
        user = ReferralCodeFactory.get_user_by_code('testtoken')
        self.assertEqual(user, None)
    
    def test_create_code_success(self):
        user = CustomUser.objects.get(username='testuser')
        ReferralCodeFactory._create_code({'user': user})
        self.assertTrue(ReferralCode.objects.filter(user=user).exists())
    
    def test_create_code_fail(self):
        user = None
        ReferralCodeFactory._create_code({'user': user})
        self.assertFalse(ReferralCode.objects.filter(user=user).exists())