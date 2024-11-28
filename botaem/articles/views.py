import logging
import uuid
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import login_required
from articles.factories import TopicFactory
from articles.models import Article, Article_Params, Article_read_later, Article_likes
from articles.factories import ArticleFactory, ArticleLikeFactory
from articles.forms import ArticleForm, ArticleParamsForm

logger = logging.getLogger(__name__)


# View to get all articles(main page)
def articles(request):
    logger.info('got request for articles main page')
    articles_all = ArticleFactory.get_all()
    context = {
        'articles': articles_all
    }
    return render(request, 'articles/main_page.html', context=context)

# View to add article to read later (TODO make opposite view)
@login_required
def article_read_later(request, slug):
    logger.info('got request to add article to read later')
    article = get_object_or_404(Article, slug=slug)
    read_later, created = Article_read_later.objects.get_or_create(article=article, user=request.user)
    if read_later:
        logger.info('Article added to read later', extra={'article': article.tittle, 'user': request.user.username})
        return JsonResponse({'status': 'success', 'message': 'Article added to read later'})
    else:
        error_id = uuid.uuid4()
        logger.info('Error adding article to read later', extra={'article': article.tittle, 'user': request.user.username, 'error_id': error_id})
        return JsonResponse({'status': 'fail', 'message': f'{error_id} please provide to support'})


# View to like an article
@login_required
def article_like(request, slug):
    logger.info('got request to like article')
    article = get_object_or_404(Article, slug=slug)
    like, created = Article_likes.objects.get_or_create(article=article, user=request.user)
    if like and created:
        logger.info('Article liked', extra={'article': article.tittle, 'user': request.user.username})
        return JsonResponse({'status': 'success', 'message': 'Article liked'})
    if like: # if article was already liked - removing like
        return article_unlike(request, slug)
    else:
        error_id = uuid.uuid4()
        logger.info('Error liking article', extra={'article': article.tittle, 'user': request.user.username, 'error_id': error_id})
        return JsonResponse({'status': 'fail', 'message': f'{error_id} please provide to support'})

@login_required
def article_unlike(request, slug):
    logger.info('got request to unlike article')
    article = get_object_or_404(Article, slug=slug)
    removed = ArticleLikeFactory.remove(article, request.user)
    if removed:
        logger.info('Article unliked', extra={'article': article.tittle, 'user': request.user.username})
        return JsonResponse({'status': 'success', 'message': 'Article unliked'})
    else:
        error_id = uuid.uuid4()
        logger.info('Error unliking article', extra={'article': article.tittle, 'user': request.user.username, 'error_id': error_id})
        return JsonResponse({'status': 'fail', 'message': f'{error_id} please provide to support'})


# View to create article
@login_required
def create_article(request):
    if request.method == 'POST':
        logger.info('got post request to create article')
        article_data = _get_article_data(request)
        article_params_data = _get_article_params_data(request)
        if _validate_article(article_data) and _validate_article_params(article_params_data):
            article = _create_article_with_params(request.user, article_data, article_params_data)
            logger.info(f'created article: {article}')
            return JsonResponse({'message': 'Article created successfully', 'slug': article.slug})
        else:
            errors = _get_errors(article_data, article_params_data)
            return JsonResponse({'errors': errors})
    logger.info('got get request to create article')
    context = _get_forms_to_render()
    return render(request, 'articles/create.html', context=context)


# Private functions for create_article
def _get_article_data(request):
    article_data ={
        'tittle': request.POST['tittle'],
        'content': request.POST['content'],
    }
    if request.FILES.get('image'):
        article_data['image'] = request.FILES['image']
    return article_data


def _get_article_params_data(request):
    topic = TopicFactory.get_by_id(request.POST['topic'])
    if request.POST['topic'] == '' or topic is None:
        topic = 'value_to_get_validation_error'
    return {
        'topic': topic,
        'complexity': request.POST['complexity'],
    }


def _validate_article(article_data):
    form = ArticleForm(data=article_data)
    return form.is_valid()


def _validate_article_params(article_params_data):
    form = ArticleParamsForm(data=article_params_data)
    return form.is_valid()


def _create_article_with_params(author, article_data, article_params_data):
    return ArticleFactory.create_with_params(author=author, **article_data, **article_params_data)


def _get_errors(article_data, article_params_data):
    errors = {}
    if not _validate_article(article_data):
        errors['article'] = ArticleForm(data=article_data).errors
    if not _validate_article_params(article_params_data):
        errors['article_params'] = ArticleParamsForm(data=article_params_data).errors
    return errors


def _get_forms_to_render():
    article_form = ArticleForm()
    article_params_form = ArticleParamsForm()
    context = {
        'article_form': article_form,
        'article_params_form': article_params_form
    }
    return context



# View to show article
def article(request, slug):
    article = get_object_or_404(Article, slug=slug)
    article_params = get_object_or_404(Article_Params, article=article)
    article_params.views += 1
    article_params.save()
    context = {
        'article': article,
        'article_params': article_params
    }
    return render(request, 'articles/article.html', context=context)
