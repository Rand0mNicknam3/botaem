from django.urls import path
from articles.views import articles, create_article, article_read_later, article_like

app_name = 'articles'

urlpatterns = [
    path('', articles, name='articles'),
    path('create/', create_article, name='create_article'),
    path('article_read_later/<slug:slug>', article_read_later, name='article_read_later'),
    path('article_like/<slug:slug>', article_like, name='article_like'),
    ]