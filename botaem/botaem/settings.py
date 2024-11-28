import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

REDIS_HOST = os.environ.get('REDIS_HOST', 'localhost')
REDIS_PORT = os.environ.get('REDIS_PORT', 6379)
REDIS_PASSWORD=os.environ.get('REDIS_PASSWORD', None)
REDIS_USER=os.environ.get('REDIS_USER', None)
REDIS_USER_PASSWORD=os.environ.get('REDIS_USER_PASSWORD', None)

DATABASE_NAME = os.environ.get('DATABASE_NAME', 'notpassed')
DATABASE_USER = os.environ.get('DATABASE_USER', 'notpassed')
DATABASE_PASSWORD = os.environ.get('DATABASE_PASSWORD', 'notpassed')
DATABASE_HOST = os.environ.get('DATABASE_HOST', 'localhost')
DATABASE_PORT = os.environ.get('DATABASE_PORT', 5432)

GOOGLE_CLIENT_ID = os.environ.get('GOOGLE_CLIENT_ID', 'notpassed')
GOOGLE_CLIENT_SECRET = os.environ.get('GOOGLE_CLIENT_SECRET', 'notpassed')

GOOGLE_CLIENT_ID = os.environ.get('GOOGLE_CLIENT_ID', 'notpassed')
GOOGLE_CLIENT_SECRET = os.environ.get('GOOGLE_CLIENT_SECRET', 'notpassed')

DJANGO_SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', 'notpassed')

SECRET_KEY = f'{DJANGO_SECRET_KEY}'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition
INSTALLED_APPS = [
    'daphne',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',

    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',

    'crispy_forms',
    'crispy_bootstrap5',

    'myprofile',
    'publicprofile',
    'follower',
    'home',
    'articles',
    'user',
    'chatapp',
    'referral',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'allauth.account.middleware.AccountMiddleware',
]

ROOT_URLCONF = 'botaem.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'botaem.wsgi.application'


# Database
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": f"{DATABASE_NAME}",
        "USER": f"{DATABASE_USER}",
        "PASSWORD": f"{DATABASE_PASSWORD}",
        "HOST": f"{DATABASE_HOST}",
        "PORT": f"{int(DATABASE_PORT)}",
    }
}


# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

AUTHENTICATION_BACKENDS = (
        'django.contrib.auth.backends.ModelBackend',
        'allauth.account.auth_backends.AuthenticationBackend',
    )
AUTH_USER_MODEL = 'user.CustomUser'
LOGIN_URL = '/auth/login'


# Internationalization
LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Europe/Moscow'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images, etc.)
STATIC_ROOT = '/botaem/static'
STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, "static")]
STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.CachedStaticFilesStorage'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"


#cache
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.redis.RedisCache',
        'LOCATION': f'redis://{REDIS_HOST}:{REDIS_PORT}/2',
        'OPTIONS': {
            # 'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        }
    }
}
CACHE_TIMEOUT = 0


#logging 
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
        },
    },
    "root": {
        "handlers": ["console"],
        "level": "DEBUG",
    },
    "loggers": {
        "user.views": {
            "handlers": ["console"],
            "level": "INFO",
            "propagate": False,
        },
    },
}


# websockets
ASGI_APPLICATION = 'botaem.asgi.application'

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels.layers.InMemoryChannelLayer"
    }
}


# social accounts (all-auth)
LOGIN_URL = 'user:login'
LOGOUT_URL = 'user:logout'
LOGIN_REDIRECT_URL = '/'
ACCOUNT_LOGOUT_REDIRECT_URL = 'home:main_page'
SITE_ID = 1
SOCIALACCOUNT_ADAPTER = 'user.adapters.CustomAccountAdapter'
SOCIALACCOUNT_AUTO_SIGNUP = False
SOCIALACCOUNT_FORMS = {
    'signup': 'user.forms.SocialPasswordedSignupForm'
}
SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'APP': {
            'client_id': f'{GOOGLE_CLIENT_ID}',
            'secret': f'{GOOGLE_CLIENT_SECRET}',
            'key': '',
            'settings': {
                'scope': [
                    'email',
                    'profile',
                ]
            }
        }
    }
}
