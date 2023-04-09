from django.db import models


class CurrencyInfoCurrencyChoices(models.IntegerChoices):
    USD = 1, 'Dollar'
    EUR = 2, 'Euro'
    GBP = 3, 'Pound Sterling'
    JPY = 4, 'Yen'


CurrencyInfoCurrencyMap = {
    CurrencyInfoCurrencyChoices.USD: ('Dollar', 'url1'),
    CurrencyInfoCurrencyChoices.EUR: ('Euro', 'url2'),
    CurrencyInfoCurrencyChoices.UAH: ('Hryvnia', 'url3'),
    CurrencyInfoCurrencyChoices.GBP: ('Pound Sterling', 'url]4'),
    CurrencyInfoCurrencyChoices.JPY: ('Yen', 'url5'),
}


class RequestMethodChoices(models.IntegerChoices):
    GET = 1, 'GET'
    POST = 2, 'POST'
    PUT = 3, 'PUT',
    PATCH = 4, 'PATCH',
    DELETE = 5, 'DELETE'
    HEAD = 6, 'HEAD'
    OPTIONS = 7, ' OPTIONS'
