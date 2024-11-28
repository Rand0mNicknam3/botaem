from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.urls import reverse
from myprofile.models import Profile
from user.models import CustomUser


class TestMyprofileViewsMyprofileMain(TestCase):
    
    @classmethod
    def setUpTestData(cls):
        user = CustomUser.objects.create_user(username='testuser', email='testemail@example.com', password='testpassword')
        Profile.objects.create(user=user)
    
    def test_view_myprofile_success(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get('/myprofile/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'myprofile/main_page.html')
    
    def test_view_myprofile_not_logged_in(self):
        response = self.client.get('/myprofile/')
        redirected_url_full = f'{reverse("user:login")}?next={reverse("myprofile:main_page")}'
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, redirected_url_full)

class TestMyprofileViewsUploadAvatar(TestCase):

    @classmethod
    def setUpTestData(cls):
        user = CustomUser.objects.create_user(username='testuser', email='testemail@example.com', password='testpassword')
        Profile.objects.create(user=user)
    
    def test_view_upload_avatar_success(self):
        self.client.login(username='testuser', password='testpassword')
        image = SimpleUploadedFile("default_images/article_jaba.jpg", b"file_content")
        response = self.client.post(reverse('myprofile:upload_avatar'), {'image': image})
        self.assertEqual(response.status_code, 200)
        self.assertIn(response.content, b'{"status": "success"}')
    
    def test_view_upload_avatar_not_logged_in(self):
        image = SimpleUploadedFile("default_images/article_jaba.jpg", b"file_content")
        response = self.client.post(reverse('myprofile:upload_avatar'), {'image': image})
        redirected_url_full = f'{reverse("user:login")}?next={reverse("myprofile:upload_avatar")}'
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, redirected_url_full)
    
    def test_view_upload_avatar_fail_too_big_image(self):
        self.client.login(username='testuser', password='testpassword')
        with open("media/default_images/article_dog.jpg", "rb") as f:
            image = SimpleUploadedFile("default_images/article_dog.jpg", f.read())
        response = self.client.post(reverse('myprofile:upload_avatar'), {'image': image})
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'{"status": "fail", "error": "Image is too big"}', response.content)

    def test_view_upload_avatar_fail_no_image(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.post(reverse('myprofile:upload_avatar'), {})
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'{"status": "fail", "error": "Image is required"}', response.content)


class TestMyprofileViewsUploadBio(TestCase):

    @classmethod
    def setUpTestData(cls):
        user = CustomUser.objects.create_user(username='testuser', email='testemail@example.com', password='testpassword')
        Profile.objects.create(user=user)

    def test_view_upload_bio_not_logged_in(self):
        response = self.client.post(reverse('myprofile:upload_bio'), {'bio': 'testbio'})
        redirected_url_full = f'{reverse("user:login")}?next={reverse("myprofile:upload_bio")}'
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, redirected_url_full)


    def test_view_upload_bio_success(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.post(reverse('myprofile:upload_bio'), {'bio': 'testbio'})
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'{"status": "success"}', response.content)
    
    def test_view_upload_bio_fail_too_big(self):
        self.client.login(username='testuser', password='testpassword')
        bio = '1' * 255
        response = self.client.post(reverse('myprofile:upload_bio'), {'bio': bio})
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'{"status": "fail", "error": "Bio is too big"', response.content)
    
    def test_view_upload_bio_fail_no_bio(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.post(reverse('myprofile:upload_bio'), {})
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'{"status": "fail", "error": "Bio is required"}', response.content)

class TestMyprofileViewsGetRefCode(TestCase):

    @classmethod
    def setUpTestData(cls):
        user = CustomUser.objects.create_user(username='testuser', email='testemail@example.com', password='testpassword')
        Profile.objects.create(user=user)
    
    def test_view_get_ref_code_success(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('myprofile:get_refcode'))
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'{"status": "success"', response.content)
    
    def test_view_get_ref_code_not_logged_in(self):
        response = self.client.get(reverse('myprofile:get_refcode'))
        redirected_url_full = f'{reverse("user:login")}?next={reverse("myprofile:get_refcode")}'
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, redirected_url_full)
    
    def test_view_get_ref_code_post_method_success(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.post(reverse('myprofile:get_refcode'))
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'{"status": "success"', response.content)
