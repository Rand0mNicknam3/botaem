from django.apps import AppConfig
from django.apps import apps
from django.dispatch import receiver
from django.db.models.signals import post_migrate
import logging

logger = logging.getLogger(__name__)


@receiver(post_migrate, sender=AppConfig)
def create_start_data(sender, **kwargs):
    from initial_data import start_user, start_topic, start_articles, start_articles_params

    CustomUser = apps.get_model('user', 'CustomUser')
    if not CustomUser.objects.filter(username='helloworld').exists():
        user = CustomUser.objects.create(**start_user)
        logger.info("User created", extra={'username': user.username})
    else:
        user = CustomUser.objects.get(username='helloworld')
        logger.info(f"{user.username} already exists")

    Article = apps.get_model('articles', 'Article')
    Topic = apps.get_model('articles', 'Topic')
    Article_params = apps.get_model('articles', 'Article_Params')
    Profile = apps.get_model('myprofile', 'Profile')

    if not Topic.objects.filter(name='Python').exists():
        topic = Topic.objects.create(**start_topic)
        logger.info("Topic created", extra={'topic': start_topic['name']})
    else:
        topic = Topic.objects.get(name='Python')
        logger.info("Topic already exists")

    if not Article.objects.filter(tittle='Hello, World!').exists():
        start_articles['author'] = user
        article = Article.objects.create(**start_articles)
        Article_params.objects.create(article=article, topic=topic, complexity=1)
        logger.info("Article created", extra={'article': start_articles['tittle']})
    else:
        article = Article.objects.get(tittle='Hello, World!')
        logger.info("Article already exists")

    if not Article_params.objects.filter(article=article).exists():
        start_articles_params['article'] = article
        start_articles_params['topic'] = topic
        Article_params.objects.create(**start_articles_params)
        logger.info("Article_params created", extra={'article_params': article.tittle})
    else:
        logger.info("Article_params already exists")

    if not Profile.objects.filter(user=user).exists():
        Profile.objects.create(user=user)
        logger.info("Profile created", extra={'user': user.username})
    else:
        logger.info("Profile already exists")


class ArticlesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'articles'
    
    def ready(self):
        post_migrate.connect(create_start_data, sender=self)
