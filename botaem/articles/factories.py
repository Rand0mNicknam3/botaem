import logging
from django.utils.text import slugify
from django.forms import ValidationError
from articles.models import Article, Article_Params, Article_read_later, Topic, Article_likes

logger = logging.getLogger(__name__)


class TopicFactory:

    @staticmethod
    def get_by_name(name):
        return TopicFactory._get_topic({'name': name})
    
    @staticmethod
    def get_by_id(id):
        return TopicFactory._get_topic({'id': id})
    
    @staticmethod
    def create(name, description):
        return TopicFactory._create_topic({'name': name, 'description': description})
    
    @staticmethod
    def get_articles(name):
        topic = TopicFactory._get_topic({'name': name})
        if topic is None:
            return None
        return topic.articles
    
    def _create_topic(query):
        try:
            topic = Topic(**query)
            topic.full_clean()
            topic.save()
            return topic
        except ValidationError as e:
            logger.error(f'ValidationError while creating topic in TopicFactory: {e.messages}')
            return None

    def _get_topic(query):
        try:
            return Topic.objects.get(**query)
        except Exception as e:
            logger.critical(f'{e} while getting topic in TopicFactory')
            return None


class ArticleParamsFactory:
        
    @staticmethod
    def create(article, topic, complexity):
        return ArticleParamsFactory._create_article_params({'article': article, 'topic': topic, 'complexity': complexity})
    
    @staticmethod
    def get_by_article(article, topic, complexity):
        return ArticleParamsFactory._get_article_params({'article': article})
    
    def _create_article_params(query):
        try:
            article_params = Article_Params(**query)
            article_params.full_clean()
            article_params.save()
            return article_params
        except ValidationError as e:
            logger.error(f'ValidationError while creating article params in ArticleParamsFactory: {e.messages}')
            return None
        except Exception as e:
            logger.error(f'{e} while creating article params in ArticleParamsFactory')
            return None

    def _get_article_params(query):
        try:
            return Article_Params.objects.get(**query)
        except Exception as e:
            logger.error(f'{e} while getting article params in ArticleParamsFactory')
            return None


class ArticleFactory:

    @staticmethod
    def create(author, tittle, content, image=None):
        if image:
            return ArticleFactory._create_article({'author': author, 'tittle': tittle, 'content': content, 'image': image})
        return ArticleFactory._create_article({'author': author, 'tittle': tittle, 'content': content})
    
    @staticmethod
    def create_with_params(author, tittle, content, image=None, topic=None, complexity=None):
        article = ArticleFactory.create(author, tittle, content, image)
        ArticleParamsFactory.create(article=article, topic=topic, complexity=complexity)
        return article

    @staticmethod
    def get_all():
        return Article.objects.all()
    
    @staticmethod
    def get_by_slug(slug):
        return ArticleFactory._get_article({'slug': slug})

    def _get_article(query):
        try:
            return Article.objects.get(**query)
        except Exception as e:
            logger.error(f'{e} while getting article in ArticleFactory')
            return None
    
    def _create_article(query):
        try:
            article = Article(**query)
            article.slug = slugify(article.tittle)
            article.full_clean()
            article.save()
            return article
        except ValidationError as e:
            logger.error('ValidationError while creating article in ArticleFactory', extra={'errors': e.messages})
            return None
        except Exception as e:
            logger.error(f'{e} while creating article in ArticleFactory')
            return None
        
# TODO add remove readlater + tests
class ArticleReadLaterFactory:

    @staticmethod
    def create(article, user):
        return ArticleReadLaterFactory._create_read_later({'article': article, 'user': user})
    
    def _create_read_later(query):
        try:
            read_later = Article_read_later(**query)
            read_later.full_clean()
            read_later.save()
            return read_later
        except Exception as e:
            logger.error(f'{e} while creating read later in ArticleReadLaterFactory')
            return None


class ArticleLikeFactory:
    
    @staticmethod
    def create(article, user):
        return ArticleLikeFactory._create_like({'article': article, 'user': user})
    
    def _create_like(query):
        try:
            like = Article_likes(**query)
            like.full_clean()
            like.save()
            return like
        except ValidationError as e:
            logger.error('ValidationError while creating like in AticleLikeFactory', extra={'errors': e.messages})
            return None
        except Exception as e:
            logger.error(f'{e} while creating like in ArticleLikeFactory')
            return None 
    
    @staticmethod    
    def remove(article, user):
        return ArticleLikeFactory._remove_like({'article': article, 'user': user})
    
    def _remove_like(query):
        try:
            like = Article_likes.objects.get(**query)
            like.delete()
            return True
        except Exception as e:
            logger.error(f'{e} while unliking article in ArticleFactory')
            return None