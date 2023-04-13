from celery import shared_task

from currency.constants import PrivatConfig, MonoConfig, AvailableCurrency
from utils.celery_classes import BaseTaskWithRetry
from utils.helpers import get_response_from_api, json_to_decimal


@shared_task(base=BaseTaskWithRetry)
def parse_privatbank():
    from currency.models import Rate, Source

    responce = get_response_from_api(PrivatConfig.source_url)
    rates = json_to_decimal(responce, keys_to_convert=['buy', 'sale'])

    for rate in rates:
        if rate['ccy'] in AvailableCurrency.names():
            print(rate)



@shared_task(base=BaseTaskWithRetry)
def parse_monobank():
    from currency.models import Rate, Source

    responce = get_response_from_api(MonoConfig.source_url)
    rates = json_to_decimal(responce, keys_to_convert=['rateBuy', 'rateSell'])

    for rate in rates:
        if rate['currencyCodeA'] in AvailableCurrency.codes():
            print(rate)
