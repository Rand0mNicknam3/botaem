from user.factories import CustomUserFactory
from user.models import CustomUser
from myprofile.models import Profile
from django.test import TestCase


class TestCustomUserFactory(TestCase):

    @classmethod
    def setUpTestData(cls):
        user = CustomUser.objects.create_user(username='testuser', email='testemail@example.com', password='testpassword')
        Profile.objects.create(user=user)

    def test_factory_get_by_username(self):
        user = CustomUserFactory.get_by_username('testuser')
        self.assertEqual(user.username, 'testuser')

    def test_factory_get_by_username(self):
        user = CustomUserFactory.get_by_username('testuser')
        self.assertEqual(user.username, 'testuser')
    
    def test_factory_get_image_by_instance(self):
        user = CustomUserFactory.get_by_username('testuser')
        profile = Profile.objects.get(user=user)
        image = CustomUserFactory.get_image_by_instance(user)
        self.assertEqual(image, profile.image)