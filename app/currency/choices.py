from django.db import models


class RateCurrencyChoices(models.IntegerChoices):
    USD = 1, 'Dollar'
    EUR = 2, 'Euro'
    GBP = 3, 'Pound Sterling'
    JPY = 4, 'Yen'


class RequestMethodChoices(models.IntegerChoices):
    GET = 1, 'GET'
    POST = 2, 'POST'
    PUT = 3, 'PUT',
    PATCH = 4, 'PATCH',
    DELETE = 5, 'DELETE'
    HEAD = 6, 'HEAD'
    OPTIONS = 7, ' OPTIONS'
