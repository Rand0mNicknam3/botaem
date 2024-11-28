from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('user.urls', namespace='user')),
    path('myprofile/', include('myprofile.urls', namespace='myprofile')),
    path('profile/', include('publicprofile.urls', namespace='publicprofile')),
    path('follower/', include('follower.urls', namespace='follower')),
    path('', include('home.urls', namespace='home')),
    path('articles/', include('articles.urls', namespace='articles')),
    path('article/', include('articles.slug_urls', namespace='article')),
    path('chat/', include('chatapp.urls', namespace='chatapp')),
    path('rf/', include('referral.urls', namespace='referral')),
    path('accounts/', include('allauth.urls')),
    ]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)