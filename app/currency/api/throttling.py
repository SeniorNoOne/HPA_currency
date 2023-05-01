from rest_framework.throttling import AnonRateThrottle, UserRateThrottle


class CurrencyAnonThrottle(AnonRateThrottle):
    scope = 'currency_anon'
    rate = '15/min'


class CurrencyUserThrottle(UserRateThrottle):
    scope = 'currency_auth'
    rate = '40/min'
