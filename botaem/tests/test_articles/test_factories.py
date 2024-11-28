from django.test import TestCase
from articles.factories import ArticleLikeFactory, ArticleParamsFactory, ArticleReadLaterFactory, TopicFactory, ArticleFactory
from articles.models import Article_likes, Article_read_later, Topic, Article, Article_Params
from user.models import CustomUser

class TestTopicFactory(TestCase):

    @classmethod
    def setUpTestData(cls):
        topic = Topic.objects.create(name='testtopic', description='testdescription')
        author = CustomUser.objects.create_user(username='testuser', email='testemail@example.com', password='testpassword')
        article = Article.objects.create(author=author, tittle='testtitle', content='testcontent')
        Article_Params.objects.create(article=article, topic=topic)

    def test_get_by_id_success(self):
        topic_id = Topic.objects.get(name='testtopic').id
        topic = TopicFactory.get_by_id(topic_id)
        self.assertEqual(topic.name, 'testtopic')

    def test_get_by_id_fail(self):
        topic_id = 999
        topic = TopicFactory.get_by_id(topic_id)
        self.assertEqual(topic, None)
    
    def test_get_by_id_fail_string(self):
        topic_id = 'zxc'
        topic = TopicFactory.get_by_id(topic_id)
        self.assertEqual(topic, None)

    def test_get_by_name_success(self):
        topic = TopicFactory.get_by_name('testtopic')
        self.assertEqual(topic.name, 'testtopic')
    
    def test_get_by_name_fail(self):
        topic = TopicFactory.get_by_name('testtopic1')
        self.assertEqual(topic, None)
    
    def test_get_by_name_fail_integer(self):
        topic = TopicFactory.get_by_name(999)
        self.assertEqual(topic, None)
    
    def test_get_articles_success(self):
        topic = TopicFactory.get_by_name('testtopic')
        articles = TopicFactory.get_articles('testtopic')
        self.assertEqual(articles.count(), 1)

    def test_get_articles_fail(self):
        topic = TopicFactory.get_by_name('testtopic')
        articles = TopicFactory.get_articles('testtopic1')
        self.assertEqual(articles, None)


class TestArticleFactory(TestCase):

    @classmethod
    def setUpTestData(cls):
        topic = Topic.objects.create(name='testtopic', description='testdescription')
        author = CustomUser.objects.create_user(username='testuser', email='testemail@example.com', password='testpassword')
        article = Article.objects.create(author=author, tittle='testtitle', content='testcontent')
        Article_Params.objects.create(article=article, topic=topic)
    
    def test_create_article_success(self):
        author = CustomUser.objects.get(username='testuser')
        ArticleFactory.create(author=author, tittle='testtitle2zxczxc', content='testcontent')
        self.assertTrue(Article.objects.filter(tittle='testtitle2zxczxc').exists())

    def test_create_article_fail_tittle_too_long(self):
        author = CustomUser.objects.get(username='testuser')
        tittle = '1' * 55
        article = ArticleFactory.create(author=author, tittle=tittle, content='someuniquecontent')
        self.assertEqual(article, None)

    def test_create_article_fail_tittle_too_short(self):
        author = CustomUser.objects.get(username='testuser')
        tittle = '1'
        article = ArticleFactory.create(author=author, tittle=tittle, content='helloworld')
        self.assertEqual(article, None)

    def test_create_article_fail_two_with_same_tittle(self):
        author = CustomUser.objects.get(username='testuser')
        article = ArticleFactory.create(author=author, tittle='testtitle', content='helloworld')
        self.assertEqual(article, None)
    
    def test_create_article_with_image_success(self):
        author = CustomUser.objects.get(username='testuser')
        ArticleFactory.create(author=author, tittle='testtitle2', content='helloworld', image='default_images/article_jaba.jpg')
        self.assertTrue(Article.objects.filter(tittle='testtitle2').exists())

    def test_create_article_with_image_fail_too_big(self):
        author = CustomUser.objects.get(username='testuser')
        ArticleFactory.create(author=author, tittle='testtitle2', content='helloworld', image='default_images/article_dog.jpg')
        self.assertFalse(Article.objects.filter(tittle='testtitle2').exists())
    
    def test_create_article_fail_content_too_long(self):
        author = CustomUser.objects.get(username='testuser')
        content = '1' * 4001
        article = ArticleFactory.create(author=author, tittle='testtitle2', content=content)
        self.assertEqual(article, None)
    
    def test_create_article_fail_content_too_short(self):
        author = CustomUser.objects.get(username='testuser')
        article = ArticleFactory.create(author=author, tittle='testtitle2', content='1')
        self.assertEqual(article, None)

class TestArticleParamsFactory(TestCase):

    @classmethod
    def setUpTestData(cls):
        Topic.objects.create(name='testtopic', description='testdescription')
        author = CustomUser.objects.create_user(username='testuser', email='testemail@example.com', password='testpassword')
        Article.objects.create(author=author, tittle='testtitle', content='testcontent')
    
    def test_create_article_params_success(self):
        topic = Topic.objects.get(name='testtopic')
        article = Article.objects.get(tittle='testtitle')
        ArticleParamsFactory.create(article=article, topic=topic, complexity=1)
        self.assertTrue(Article_Params.objects.filter(article=article, topic=topic, complexity=1).exists())
    
    def test_create_article_params_fail_article_not_exist(self):
        topic = Topic.objects.get(name='testtopic')
        params = ArticleParamsFactory.create(article='article_not_exist', topic=topic, complexity=1)
        self.assertEqual(params, None)

    def test_create_article_params_fail_topic_not_exist(self):
        article = Article.objects.get(tittle='testtitle')
        params = ArticleParamsFactory.create(article=article, topic=33, complexity=1)
        self.assertEqual(params, None)
    
    def test_create_article_params_fail_complexity_not_exist(self):
        article = Article.objects.get(tittle='testtitle')
        topic = Topic.objects.get(name='testtopic')
        params = ArticleParamsFactory.create(article=article, topic=topic, complexity=10)
        self.assertEqual(params, None)

    
class TestArticleLikeFactory(TestCase):
    @classmethod
    def setUpTestData(cls):
        author = CustomUser.objects.create_user(username='testuser', email='testemail@example.com', password='testpassword')
        topic = Topic.objects.create(name='testtopic')
        article = Article.objects.create(author=author, tittle='testtitle', content='testcontent')
        Article_Params.objects.create(article=article, topic=topic, complexity=1)
    
    def test_create_article_like_success(self):
        article = Article.objects.get(tittle='testtitle')
        user = CustomUser.objects.get(username='testuser')
        ArticleLikeFactory.create(article=article, user=user)
        self.assertTrue(Article_likes.objects.filter(article=article, user=user).exists())
    
    def test_create_article_fail_article_not_exist(self):
        user = CustomUser.objects.get(username='testuser')
        like = ArticleLikeFactory.create(article='article_not_exist', user=user)
        self.assertEqual(like, None)
    
    def test_create_article_fail_user_not_exist(self):
        article = Article.objects.get(tittle='testtitle')
        like = ArticleLikeFactory.create(article=article, user='user_not_exist')
        self.assertEqual(like, None)
    
    def test_remove_article_success(self):
        article = Article.objects.get(tittle='testtitle')
        user = CustomUser.objects.get(username='testuser')
        Article_likes.objects.create(article=article, user=user)
        removed = ArticleLikeFactory.remove(article=article, user=user)
        self.assertEqual(removed, True)
        self.assertFalse(Article_likes.objects.filter(article=article, user=user).exists())
    
    def test_remove_article_fail_article_not_exist(self):
        user = CustomUser.objects.get(username='testuser')
        article = Article.objects.get(tittle='testtitle')
        Article_likes.objects.create(article=article, user=user)
        removed = ArticleLikeFactory.remove(article='article_not_exist', user=user)
        self.assertEqual(removed, None)

class TestArticleReadLaterFactory(TestCase):
    @classmethod
    def setUpTestData(cls):
        author = CustomUser.objects.create_user(username='testuser', email='testemail@example.com', password='testpassword')
        topic = Topic.objects.create(name='testtopic')
        article = Article.objects.create(author=author, tittle='testtitle', content='testcontent')
        Article_Params.objects.create(article=article, topic=topic, complexity=1)
    
    def test_create_article_read_later_success(self):
        article = Article.objects.get(tittle='testtitle')
        user = CustomUser.objects.get(username='testuser')
        ArticleReadLaterFactory.create(article=article, user=user)
        self.assertTrue(Article_read_later.objects.filter(article=article, user=user).exists())
    
    def test_create_article_read_later_fail_article_not_exist(self):
        user = CustomUser.objects.get(username='testuser')
        read_later = ArticleReadLaterFactory.create(article='article_not_exist', user=user)
        self.assertEqual(read_later, None)
