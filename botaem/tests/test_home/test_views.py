from django.test import TestCase
from django.urls import reverse


class TestHomeViews(TestCase):

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
    
    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('home:main'))
        self.assertEqual(response.status_code, 200)
    
    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('home:main'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home/main_page.html')