import environ

from datetime import timedelta
from pathlib import Path

from django.urls import reverse_lazy
from django.db.backends.postgresql.psycopg_any import IsolationLevel
from celery.schedules import crontab


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent


# Load environment variables from .env file
env_file = BASE_DIR.parent / 'env' / '.env'
env = environ.Env()
env.read_env(env_file)


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env.str('SECRET_KEY')
DEBUG = False
ALLOWED_HOSTS = env.list('ALLOWED_HOSTS', default=[])


# Application definition
DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

EXTERNAL_APPS = [
    'django_extensions',
    'phonenumber_field',
    'debug_toolbar',
    'rangefilter',
    'import_export',
    'storages',
    'crispy_forms',
    'crispy_bootstrap5',
    'django_filters',
    'rest_framework',
    'rest_framework_simplejwt',
    'drf_yasg',
]

CUSTOM_APPS = [
    'currency',
    'account',
]

INSTALLED_APPS = DJANGO_APPS + EXTERNAL_APPS + CUSTOM_APPS

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'currency.middlewares.RequestResponseTimeMiddleware',
]

ROOT_URLCONF = 'settings.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            BASE_DIR / 'templates',

        ],
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

WSGI_APPLICATION = 'settings.wsgi.application'


# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': env.str('POSTGRES_DB', 'postgres-db'),
        'USER': env.str('POSTGRES_USER', 'postgres'),
        'PASSWORD': env.str('POSTGRES_PASSWORD', 'postgres'),
        'HOST': env.str('POSTGRES_HOST', 'localhost'),
        'PORT': env.str('POSTGRES_PORT', '5432'),
        'CONN_MAX_AGE': None,
        'CONN_HEALTH_CHECKS': True,
        'OPTIONS': {
            'isolation_level': IsolationLevel.REPEATABLE_READ,
        }
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


# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True


# Static files (CSS, JavaScript, Images)
STATIC_URL = 'static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR.parent / 'static_content' / 'static'


# SMTP
EMAIL_BACKEND = env.str('EMAIL_BACKEND', 'django.core.mail.backends.console.EmailBackend')
EMAIL_HOST = env.str('EMAIL_HOST', 'localhost')
EMAIL_PORT = env.str('EMAIL_PORT', '2525')

EMAIL_HOST_USERNAME = env.str('EMAIL_HOST_USERNAME', 'user')
EMAIL_HOST_PASSWORD = env.str('EMAIL_PASSWORD', 'password')
EMAIL_USE_TLS = env.bool('EMAIL_USR_TLS', True)

DEFAULT_FROM_EMAIL = env.str('EMAIL_VALIDATED_SENDER_USER', 'test_sender@example.com')
EMAIL_RECEIVER = env.list('EMAIL_TARGET_USERS', default='test_receiver@example.com')


# Static and media
DEFAULT_FILE_STORAGE = env.str('STORAGE_BACKEND', 'django.core.files.storage.FileSystemStorage')
# STATICFILES_STORAGE = 'storages.backends.s3boto3.S3StaticStorage'
MEDIA_ROOT = BASE_DIR.parent / 'static_content' / 'media'
MEDIA_URL = '/media/'


# Storage
AWS_ACCESS_KEY_ID = env.str('STORAGE_ACCESS_KEY_ID', '')
AWS_SECRET_ACCESS_KEY = env.str('STORAGE_SECRET_ACCESS_KEY', '')
AWS_STORAGE_BUCKET_NAME = env.str('STORAGE_BUCKET_NAME', '')
AWS_S3_ENDPOINT_URL = env.str('STORAGE_ENDPOINT_URL', '')
AWS_S3_CUSTOM_DOMAIN = AWS_STORAGE_BUCKET_NAME + env.str('STORAGE_CUSTOM_DOMAIN', '')
AWS_S3_FILE_OVERWRITE = env.bool('STORAGE_FILE_OVERWRITE', False)


# Debug toolbar fix
if DEBUG:
    import socket  # only if you haven't already imported this
    hostname, _, ips = socket.gethostbyname_ex(socket.gethostname())
    INTERNAL_IPS = [ip[: ip.rfind(".")] + ".1" for ip in ips] + ["127.0.0.1", "10.0.2.2"]


# Login URLs
LOGIN_REDIRECT_URL = reverse_lazy('index')
LOGOUT_REDIRECT_URL = reverse_lazy('index')
LOGIN_URL = reverse_lazy('login')


# User model
AUTH_USER_MODEL = 'account.User'


# HOST and SCHEMA for SMTP mail sender
HOST = 'localhost:8000'
HTTP_SCHEMA = 'http'


# Bootstrap
CRISPY_ALLOWED_TEMPLATE_PACKS = 'bootstrap5'
CRISPY_TEMPLATE_PACK = 'bootstrap5'


# Celery
CELERY_BROKER_URL = 'amqp://{0}:{1}@{2}:{3}//'.format(
    env.str('RABBITMQ_DEFAULT_USER', 'guest'),
    env.str('RABBITMQ_DEFAULT_PASS', 'guest'),
    env.str('RABBITMQ_DEFAULT_HOST', '127.0.0.1'),
    env.str('RABBITMQ_DEFAULT_PORT', '5672'),
)

CELERY_IMPORTS = ('utils.tasks',)

CELERY_QUEUES = {
    'scheduled_tasks': {
        'exchange': 'scheduled_tasks',
        'exchange_type': 'direct',
        'routing_key': 'scheduled_tasks',
    },
}

CELERY_DEFAULT_QUEUE = 'default'
CELERY_DEFAULT_EXCHANGE = 'default'
CELERY_DEFAULT_ROUTING_KEY = 'default'

CELERY_ROUTES = {
    'utils.tasks.celery_send_mail': {
        'queue': 'default',
        'routing_key': 'default',
    },
    'currency.tasks.parse_privatbank': {
        'queue': 'scheduled_tasks',
        'routing_key': 'scheduled_tasks',
    },
    'currency.tasks.parse_monobank': {
        'queue': 'scheduled_tasks',
        'routing_key': 'scheduled_tasks',
    },
    'currency.tasks.parse_nbu': {
        'queue': 'scheduled_tasks',
        'routing_key': 'scheduled_tasks',
    }
}

CELERY_BEAT_SCHEDULE = {
    'parse_privatbank_scheduled_task': {
        'task': 'currency.tasks.parse_privatbank',
        'schedule': crontab(
            minute=env.str('CELERY_CRONTAB', '*/15')
        ),
        'options': {'queue': 'scheduled_tasks'},
    },
    'parse_monobank_scheduled_task': {
        'task': 'currency.tasks.parse_monobank',
        'schedule': crontab(
            minute=env.str('CELERY_CRONTAB', '*/15')
        ),
        'options': {'queue': 'scheduled_tasks'},
    },
    'parse_nbu_scheduled_task': {
        'task': 'currency.tasks.parse_nbu',
        'schedule': crontab(
            minute=env.str('CELERY_CRONTAB', '*/15')
        ),
        'options': {'queue': 'scheduled_tasks'},
    }
}

# REST
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_FILTER_BACKENDS': (
        'django_filters.rest_framework.DjangoFilterBackend',
        'rest_framework.filters.OrderingFilter',
        'rest_framework.filters.SearchFilter',
    ),
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
        'rest_framework_yaml.renderers.YAMLRenderer',
        'rest_framework_xml.renderers.XMLRenderer',
    ),
    'DEFAULT_THROTTLE_CLASSES': (
        'rest_framework.throttling.AnonRateThrottle',
        'rest_framework.throttling.UserRateThrottle',
    ),
    'DEFAULT_THROTTLE_RATES': {
        'anon': '20/min',
        'user': '50/min',
        'currency_anon': '15/min',
        'currency_auth': '40/min',
    },
}

# Simple JWT
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=30),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'AUTH_HEADER_TYPES': ('Bearer', 'JWT'),
}

# Caching
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.PyMemcacheCache',
        'LOCATION': '{0}:{1}'.format(
            env.str('CACHE_HOST', '127.0.0.1'),
            env.str('CACHE_PORT', '11211'),
        ),
    }
}
