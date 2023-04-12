from django.urls import reverse_lazy

from configparser import ConfigParser
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-ilj+w!i78*kri3#di348j7ip2dhi5&sftni$(=0w-3pzgr^mxe'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']


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
    'currency.middlewares.RequestResponseTimeMiddleware'
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
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = 'static/'
STATICFILES_DIRS = [BASE_DIR / 'static']

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

config = ConfigParser()
config.read('config.ini')

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
DEFAULT_FROM_EMAIL = 'test_sender@example.com'
EMAIL_RECEIVER = ['test_receiver@example.com']

if 'smtp' in config:
    EMAIL_HOST = config.get('smtp', 'host', fallback='')
    EMAIL_PORT = config.get('smtp', 'port', fallback='')
    EMAIL_HOST_USER = config.get('smtp', 'username', fallback='')
    EMAIL_HOST_PASSWORD = config.get('smtp', 'password', fallback='')
    EMAIL_USE_TLS = config.get('smtp', 'tls', fallback='')
    DEFAULT_FROM_EMAIL = config.get('smtp', 'validated_user', fallback='')
    EMAIL_RECEIVER = [mail.strip() for mail in
                      config.get('smtp', 'target_users', fallback=[]).split(',')]
    if DEFAULT_FROM_EMAIL and EMAIL_RECEIVER:
        EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'


DEFAULT_FILE_STORAGE = 'django.core.files.storage.FileSystemStorage'
# STATICFILES_STORAGE = 'storages.backends.s3boto3.S3StaticStorage'
MEDIA_ROOT = BASE_DIR.parent / 'static_content' / 'media'
MEDIA_URL = '/media/'

if 's3' in config:
    DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

    AWS_ACCESS_KEY_ID = config.get('s3', 'access_key_id')
    AWS_SECRET_ACCESS_KEY = config.get('s3', 'secret_access_key')
    AWS_STORAGE_BUCKET_NAME = config.get('s3', 'bucket_name')
    AWS_S3_ENDPOINT_URL = config.get('s3', 'endpoint_url')
    AWS_S3_CUSTOM_DOMAIN = AWS_STORAGE_BUCKET_NAME + config.get("s3", "custom_domain")
    AWS_S3_FILE_OVERWRITE = config.get("s3", "overwrite")

if DEBUG:
    import socket  # only if you haven't already imported this
    hostname, _, ips = socket.gethostbyname_ex(socket.gethostname())
    INTERNAL_IPS = [ip[: ip.rfind(".")] + ".1" for ip in ips] + ["127.0.0.1", "10.0.2.2"]

LOGIN_REDIRECT_URL = reverse_lazy('index')
LOGOUT_REDIRECT_URL = reverse_lazy('index')
LOGIN_URL = reverse_lazy('login')

AUTH_USER_MODEL = 'account.User'

HOST = 'localhost:8000'
HTTP_SCHEMA = 'http'

CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"

CRISPY_TEMPLATE_PACK = "bootstrap5"

# Celery
CELERY_BROKER_URL = 'amqp://localhost'
CELERY_IMPORTS = ('utils.tasks',)

CELERY_QUEUES = {
    'mail': {
        'exchange': 'mail',
        'exchange_type': 'direct',
        'binding_key': 'mail'
    },
}

CELERY_ROUTES = {
    'utils.tasks.celery_send_mail': {'queue': 'mail'}
}
