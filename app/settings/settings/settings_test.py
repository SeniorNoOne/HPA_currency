from .base import *

DEBUG = False

REST_FRAMEWORK.update(
    {
        'DEFAULT_THROTTLE_RATES': {
            'currency_anon': '150/min',
            'currency_auth': '150/min',
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
