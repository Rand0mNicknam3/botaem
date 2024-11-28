from django.test import TestCase
from user.models import CustomUser
from follower.models import Follower
from follower.factories import FollowerFactory

class FollowerFactoryTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        CustomUser.objects.create_user(username='follower', email='testemail@example.com', password='testpassword')
        CustomUser.objects.create_user(username='followed', email='testemail2@example.com', password='testpassword')
    
    def test_create_follower_success(self):
        follower = CustomUser.objects.get(username='follower')
        followed = CustomUser.objects.get(username='followed')
        followpair = FollowerFactory.create(followed, follower)
        self.assertTrue(Follower.objects.filter(user=followed, follower=follower).exists())
        self.assertTrue(isinstance(followpair, Follower))

    def test_create_follower_fail_wrong_follower(self):
        followed = CustomUser.objects.get(username='followed')
        followpair = FollowerFactory.create(followed, 'wrong')
        self.assertEqual(followpair, None)
    
    def test_create_follower_fail_wrong_followed(self):
        follower = CustomUser.objects.get(username='follower')
        followpair = FollowerFactory.create('wrong', follower)
        self.assertEqual(followpair, None)
    
    def test_remove_follower_success(self):
        follower = CustomUser.objects.get(username='follower')
        followed = CustomUser.objects.get(username='followed')
        Follower.objects.create(user=followed, follower=follower)
        followpair = FollowerFactory.remove(followed, follower)
        self.assertNotEqual(followpair, None)
        self.assertFalse(Follower.objects.filter(user=followed, follower=follower).exists())
    
    def test_remove_follower_fail_wrong_follower(self):
        followed = CustomUser.objects.get(username='followed')
        followpair = FollowerFactory.remove(followed, 'wrong')
        self.assertEqual(followpair, None)
    
    def test_remove_follower_fail_wrong_followed(self):
        follower = CustomUser.objects.get(username='follower')
        followpair = FollowerFactory.remove('wrong', follower)
        self.assertEqual(followpair, None)
    
    def test_remove_follower_fail_wrong_data(self):
        followpair = FollowerFactory.remove('wrong', 'wrong')
        self.assertEqual(followpair, None)
    
    def test_get_followers_count_by_slug_success(self):
        follower = CustomUser.objects.get(username='follower')
        followed = CustomUser.objects.get(username='followed')
        Follower.objects.create(user=followed, follower=follower)
        count = FollowerFactory.get_followers_count_by_slug(followed.username)
        self.assertEqual(count, 1)

    def test_get_followers_count_by_slug_fail_wrong_slug(self):
        count = FollowerFactory.get_followers_count_by_slug('wrong')
        self.assertEqual(count, None)        