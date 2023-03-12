from django.db import models


class RateCurrencyChoices(models.IntegerChoices):
    USD = 1, 'Dollar'
    EUR = 2, 'Euro'
    UAH = 3, 'Hryvnia'
    GBP = 4, 'Pound Sterling'
    JPY = 5, 'Yen'


class RequestMethodChoices(models.IntegerChoices):
    GET = 1, 'GET'
    POST = 2, 'POST'
