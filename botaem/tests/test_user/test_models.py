from django.test import TestCase
from user.models import CustomUser

class CustomUserTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        CustomUser.objects.create(username='testuser', email='testemail@example.com', password='testpassword')

    def test_email_label(self):
        user = CustomUser.objects.get(username='testuser')
        field_label = user._meta.get_field('email').verbose_name
        self.assertEqual(field_label, 'Email address')
    
    def test_grade_label(self):
        user = CustomUser.objects.get(username='testuser')
        field_label = user._meta.get_field('grade').verbose_name
        self.assertEqual(field_label, 'User grade')

    def test_grade_default_value(self):
        user = CustomUser.objects.get(username='testuser')
        field_default = user._meta.get_field('grade').default
        self.assertEqual(field_default, 'Begginer')

    def test_str_magic_method(self):
        user = CustomUser.objects.get(username='testuser')
        self.assertEqual(str(user), 'testuser')