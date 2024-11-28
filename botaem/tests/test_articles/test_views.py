from django.contrib.messages.test import MessagesTestMixin
from django.test import TestCase
from django.urls import reverse
from articles.models import Article, Topic, Article_Params, Article_likes
from user.models import CustomUser


class TestArticlesViewsArticles(TestCase):

    @classmethod
    def setUpTestData(cls):
        author = CustomUser.objects.create_user(username='testuser', email='testemail@example.com', password='testpassword')
        Article.objects.create(author = author, tittle='testtitle', content='testcontent')

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/articles/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('articles:articles'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('articles:articles'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'articles/main_page.html')


class TestArticlesViewsCreateArticle(TestCase, MessagesTestMixin):

    @classmethod
    def setUpTestData(cls):
        CustomUser.objects.create_user(username='testuser', email='testemail@example.com', password='testpassword')
        Topic.objects.create(name='testtopic')

    def test_view_url_exists_at_desired_location(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get('/articles/create/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('articles:create_article'))
        self.assertEqual(response.status_code, 200)
    
    def test_view_uses_correct_template(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('articles:create_article'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'articles/create.html')
    
    def test_view_create_article_success(self):
        self.client.login(username='testuser', password='testpassword')
        topic = Topic.objects.get(name='testtopic')
        response = self.client.post(reverse('articles:create_article'), {'tittle': 'testtitle2', 'content': 'testcontent2', 'topic': topic.id, 'complexity': 1})
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Article.objects.filter(tittle='testtitle2').exists())
        self.assertEqual(response.content, b'{"message": "Article created successfully", "slug": "testtitle2"}')

    def test_view_create_article_content_too_long(self):
        self.client.login(username='testuser', password='testpassword')
        topic = Topic.objects.get(name='testtopic')
        content = '1' * 4001
        response = self.client.post(reverse('articles:create_article'), {'tittle': 'testtitle2', 'content': content, 'topic': topic.id, 'complexity': 1})
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Article.objects.filter(tittle='testtitle2').exists())
        self.assertIn(b'Ensure this value has at most 4000 characters', response.content)
    
    def test_view_create_article_content_too_short(self):
        self.client.login(username='testuser', password='testpassword')
        topic = Topic.objects.get(name='testtopic')
        content = '1'
        response = self.client.post(reverse('articles:create_article'), {'tittle': 'testtitle2', 'content': content, 'topic': topic.id, 'complexity': 1})
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Article.objects.filter(tittle='testtitle2').exists())
        self.assertIn(b'Ensure this value has at least 5 characters', response.content)

    def test_view_create_article_tittle_taken(self):
        self.client.login(username='testuser', password='testpassword')
        topic = Topic.objects.get(name='testtopic')
        Article.objects.create(author = CustomUser.objects.get(username='testuser'), tittle='testtitle', content='testcontent')
        response = self.client.post(reverse('articles:create_article'), {'tittle': 'testtitle', 'content': 'testcontent', 'topic': topic.id, 'complexity': 1})
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Article with this Title already exists', response.content)

    def test_view_create_article_topic_does_not_exist(self):
        self.client.login(username='testuser', password='testpassword')
        topic = Topic.objects.get(name='testtopic')
        response = self.client.post(reverse('articles:create_article'), {'tittle': 'testtitle2', 'content': 'testcontent2', 'topic': topic.id + 1, 'complexity': 1})
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Select a valid choice. That choice is not one of the available choices.", response.content)

    def test_view_create_article_complexity_does_not_exist(self):
        self.client.login(username='testuser', password='testpassword')
        topic = Topic.objects.get(name='testtopic')
        response = self.client.post(reverse('articles:create_article'), {'tittle': 'testtitle2', 'content': 'testcontent2', 'topic': topic.id, 'complexity': 50})
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Select a valid choice. 50 is not one of the available choices.", response.content)

    def test_view_create_article_complexity_does_not_exist_str(self):
        self.client.login(username='testuser', password='testpassword')
        topic = Topic.objects.get(name='testtopic')
        response = self.client.post(reverse('articles:create_article'), {'tittle': 'testtitle2', 'content': 'testcontent2', 'topic': topic.id, 'complexity': 'complexity'})
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Select a valid choice. complexity is not one of the available choices.", response.content)
     
    def test_view_create_article_topic_is_empty(self):
        self.client.login(username='testuser', password='testpassword')
        topic = Topic.objects.get(name='testtopic')
        response = self.client.post(reverse('articles:create_article'), {'tittle': 'testtitle2', 'content': 'testcontent2', 'topic': '', 'complexity': 1})
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Select a valid choice. That choice is not one of the available choices.", response.content)

    def test_view_create_article_tittle_too_short(self):
        self.client.login(username='testuser', password='testpassword')
        topic = Topic.objects.get(name='testtopic')
        tittle = '1'
        response = self.client.post(reverse('articles:create_article'), {'tittle': tittle, 'content': 'testcontent2', 'topic': topic.id, 'complexity': 1})
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Article.objects.filter(tittle=tittle).exists())
        self.assertIn(b'Ensure this value has at least 5 characters', response.content)


class TestArticlesViewsArticle(TestCase):

    @classmethod
    def setUpTestData(self):
        author = CustomUser.objects.create_user(username='testuser', email='testemail@example.com', password='testpassword')
        topic = Topic.objects.create(name='testtopic')
        article = Article.objects.create(author=author, tittle='testtitle', content='testcontent')
        Article_Params.objects.create(article=article, topic=topic, complexity=1)
    
    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/article/testtitle')
        self.assertEqual(response.status_code, 200)
    
    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('article:article', kwargs={'slug': 'testtitle'}))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('article:article', kwargs={'slug': 'testtitle'}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'articles/article.html')
    
    def test_view_article_success(self):
        response = self.client.get(reverse('article:article', kwargs={'slug': 'testtitle'}))
        self.assertEqual(response.status_code, 200)
    
    def test_view_article_does_not_exist(self):
        response = self.client.get(reverse('article:article', kwargs={'slug': 'testtitle2'}))
        self.assertEqual(response.status_code, 404)


class TestArticleViewsLikeArticle(TestCase):

    @classmethod
    def setUpTestData(self):
        author = CustomUser.objects.create_user(username='testuser', email='testemail@example.com', password='testpassword')
        topic = Topic.objects.create(name='testtopic')
        article = Article.objects.create(author=author, tittle='testtitle', content='testcontent')
        Article_Params.objects.create(article=article, topic=topic, complexity=1)
    
    def test_view_like_article_success(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('articles:article_like', kwargs={'slug': 'testtitle'}))
        self.assertEqual(b'{"status": "success", "message": "Article liked"}', response.content)
        self.assertEqual(response.status_code, 200)
    
    def test_view_like_article_does_not_exist(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('articles:article_like', kwargs={'slug': 'testtitle2'}))
        self.assertEqual(response.status_code, 404)
    
    def test_view_like_article_not_logged_in(self):
        response = self.client.get(reverse('articles:article_like', kwargs={'slug': 'testtitle'}))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/auth/login?next=/articles/article_like/testtitle')
    
    def test_view_unlike_article_success(self):
        self.client.login(username='testuser', password='testpassword')
        Article_likes.objects.create(article=Article.objects.get(tittle='testtitle'), user=CustomUser.objects.get(username='testuser'))
        response = self.client.get(reverse('articles:article_like', kwargs={'slug': 'testtitle'}))
        self.assertEqual(b'{"status": "success", "message": "Article unliked"}', response.content)