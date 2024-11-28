from django.test import TestCase
from user.models import CustomUser
from myprofile.models import Profile


class ProfileModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        user = CustomUser.objects.create_user(username='testuser', email='testemail@example.com', password='testpassword')
        Profile.objects.create(user=user)
    
    def test_image_default(self):
        user = CustomUser.objects.get(username='testuser')
        profile = Profile.objects.get(user=user)
        field_default = profile._meta.get_field('image').default
        self.assertEqual(field_default, 'default_images/profile.jpg')
    
    def test_bio_max_length(self):
        user = CustomUser.objects.get(username='testuser')
        profile = Profile.objects.get(user=user)
        max_length = profile._meta.get_field('bio').max_length
        self.assertEqual(max_length, 250)
    
    def test_slug_generation(self):
        user = CustomUser.objects.get(username='testuser')
        profile = Profile.objects.get(user=user)
        self.assertEqual(profile.slug, 'testuser')