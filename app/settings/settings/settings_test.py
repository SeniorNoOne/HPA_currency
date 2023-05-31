from .base import *

SECRET_KEY = 'ypwmoh-=)5v&3tln+36fybv0!l)i7t##27@iceem40cycm=ug1'

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
