from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from myprofile.factories import ProfileFactory
from myprofile.models import Profile
from user.models import CustomUser


class ProfileFactoryTest(TestCase):
    
    @classmethod
    def setUpTestData(cls):
        user = CustomUser.objects.create_user(username='testuser', email='testemail@example.com', password='testpassword')
    
    def test_create_profile_success(self):
        user = CustomUser.objects.get(username='testuser')
        profile = ProfileFactory.create(user=user)
        self.assertIsInstance(profile, Profile)
        self.assertTrue(Profile.objects.filter(user=user).exists())
    
    def test_create_profile_fail_wrong_user(self):
        profile = ProfileFactory.create(user='wrong_user')
        self.assertIsNone(profile)
    
    def test_get_profile_success(self):
        user = CustomUser.objects.get(username='testuser')
        profile = ProfileFactory.create(user=user)
        profile = ProfileFactory.get_profile(user=user)
        self.assertIsInstance(profile, Profile)
        self.assertEqual(profile.slug, 'testuser')
    
    def test_add_profile_image_success(self):
        user = CustomUser.objects.get(username='testuser')
        profile = ProfileFactory.create(user=user)
        image = 'default_images/article_jaba.jpg'
        profile = ProfileFactory.add_image(user=user, image=image)
        self.assertEqual(profile.image, image)
    
    def test_add_profile_image_fail_too_big(self):
        user = CustomUser.objects.get(username='testuser')
        profile = ProfileFactory.create(user=user)
        with open("media/default_images/article_dog.jpg", "rb") as f:
            image = SimpleUploadedFile("default_images/article_dog.jpg", f.read())
        profile = ProfileFactory.add_image(user=user, image=image)
        self.assertIsNone(profile)
    
    def test_add_profile_bio_success(self):
        user = CustomUser.objects.get(username='testuser')
        profile = ProfileFactory.create(user=user)
        bio = 'test bio'
        profile = ProfileFactory.add_bio(user=user, bio=bio)
        self.assertEqual(profile.bio, bio)

    def test_add_profile_bio_fail_too_big(self):
        user = CustomUser.objects.get(username='testuser')
        profile = ProfileFactory.create(user=user)
        bio = '1' * 255
        profile = ProfileFactory.add_bio(user=user, bio=bio)
        self.assertIsNone(profile)