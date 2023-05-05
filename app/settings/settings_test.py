from .settings import *

DEBUG = False

REST_FRAMEWORK = {
    'DEFAULT_THROTTLE_RATES': {
        'currency_anon': '100/min',
        'currency_auth': '100/min',
    }
}
