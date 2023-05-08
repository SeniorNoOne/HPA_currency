from rest_framework.throttling import AnonRateThrottle, UserRateThrottle


class CurrencyAnonThrottle(AnonRateThrottle):
    scope = 'currency_anon'


class CurrencyUserThrottle(UserRateThrottle):
    scope = 'currency_auth'
