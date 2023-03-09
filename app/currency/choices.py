from django.db import models


class RateCurrencyChoices(models.IntegerChoices):
    USD = 1, 'USD'
    EUR = 2, 'EUR'
    UAH = 3, 'Hryvnia'
    GBP = 4, 'Pound Sterling'
    JPY = 5, 'Yen'
