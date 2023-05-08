from .settings import *

DEBUG = False

REST_FRAMEWORK.update(
    {
        'DEFAULT_THROTTLE_RATES': {
            'currency_anon': '150/min',
            'currency_auth': '150/min',
        }
    }
)
