from .base import *

DEBUG = False

THROTTLING_RATE = 150
THROTTLING_RATE_CRONTAB = str(THROTTLING_RATE) + '/min'

REST_FRAMEWORK.update(
    {
        'DEFAULT_THROTTLE_RATES': {
            'anon': THROTTLING_RATE_CRONTAB,
            'user': THROTTLING_RATE_CRONTAB,
            'currency_anon': THROTTLING_RATE_CRONTAB,
            'currency_auth': THROTTLING_RATE_CRONTAB,
        }
    }
)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
    }
}

EMAIL_BACKEND = 'django.core.mail.backends.locmem.EmailBackend'

DEFAULT_FILE_STORAGE = 'django.core.files.storage.FileSystemStorage'

MEDIA_ROOT = BASE_DIR / 'tests' / 'media_test_dir'

MEDIA_URL = '/media/'
