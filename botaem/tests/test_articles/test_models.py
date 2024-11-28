from django.test import TestCase
from articles.models import Article, Article_Params, Article_read_later, Topic
from user.models import CustomUser


class ArticleModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        author = CustomUser.objects.create_user(username='testuser', email='testemail@example.com', password='testpassword')
        topic = Topic.objects.create(name='testtopic')
        article = Article.objects.create(author=author, tittle='testtitle', content='testcontent')
        Article_Params.objects.create(article=article, topic=topic)

    def test_tittle_verbose_name(self):
        article = Article.objects.get(tittle='testtitle')
        self.assertEqual(article._meta.get_field('tittle').verbose_name, 'Title')
    
    def test_tittle_slug_field_verbose_name(self):
        article = Article.objects.get(tittle='testtitle')
        self.assertEqual(article._meta.get_field('slug').verbose_name, 'URL')
    
    def test_article_string_method(self):
        article = Article.objects.get(tittle='testtitle')
        self.assertEqual(str(article), 'testtitle')


class ArticleParamsModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        author = CustomUser.objects.create_user(username='testuser', email='testemail@example.com', password='testpassword')
        topic = Topic.objects.create(name='testtopic')
        article = Article.objects.create(author=author, tittle='testtitle', content='testcontent')
        Article_Params.objects.create(article=article, topic=topic, complexity=1)
    
    def test_article_related_name(self):
        article = Article.objects.get(tittle='testtitle')
        article_params = Article_Params.objects.get(article=article)
        self.assertEqual(article_params._meta.get_field('article')._related_name, 'params')
    
    def test_topic_related_name(self):
        article = Article.objects.get(tittle='testtitle')
        article_params = Article_Params.objects.get(article=article)
        self.assertEqual(article_params._meta.get_field('topic')._related_name, 'articles')
    
    def test_complexity_default_value(self):
        article = Article.objects.get(tittle='testtitle')
        article_params = Article_Params.objects.get(article=article)
        self.assertEqual(article_params.complexity, 1)
    
    def test_complexity_choices(self):
        article = Article.objects.get(tittle='testtitle')
        article_params = Article_Params.objects.get(article=article)
        self.assertEqual(article_params._meta.get_field('complexity').choices, [(1, 'Easy'), (2, 'Medium'), (3, 'Hard')])

    def test_views_default_value(self):
        article = Article.objects.get(tittle='testtitle')
        article_params = Article_Params.objects.get(article=article)
        self.assertEqual(article_params.views, 0)

class ArticleReadLaterModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        author = CustomUser.objects.create_user(username='testuser', email='testemail@example.com', password='testpassword')
        topic = Topic.objects.create(name='testtopic')
        article = Article.objects.create(author=author, tittle='testtitle', content='testcontent')
        article_read_later = Article_read_later.objects.create(article=article, user=author)
    
    def test_article_related_name(self):
        article_read_later = Article_read_later.objects.get(user=CustomUser.objects.get(username='testuser'))
        self.assertEqual(article_read_later._meta.get_field('article')._related_name, 'read_later')
    
    def test_user_related_name(self):
        article_read_later = Article_read_later.objects.get(user=CustomUser.objects.get(username='testuser'))
        self.assertEqual(article_read_later._meta.get_field('user')._related_name, 'read_later_articles')

