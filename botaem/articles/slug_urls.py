from django.urls import path
from articles.views import article

app_name = 'article'

urlpatterns = [
    path('<slug:slug>', article, name='article'),
]
