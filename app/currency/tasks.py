from celery import shared_task

from currency.constants import PrivatbankConfig, MonobankConfig, AvailableCurrency
from currency.models import RateCurrencyChoices
from utils.celery_classes import BaseTaskWithRetry
from utils.helpers import get_response_from_api, json_to_decimal


@shared_task(base=BaseTaskWithRetry)
def parse_privatbank():
    from currency.models import Rate, Source

    source, _ = Source.objects.get_or_create(code=PrivatbankConfig.code,
                                             defaults=PrivatbankConfig.source_create_params)

    response = get_response_from_api(PrivatbankConfig.url)
    rates = json_to_decimal(response, keys_to_convert=['buy', 'sale'])

    for rate in rates:
        if rate['ccy'] in AvailableCurrency.names():
            last_rate = Rate.objects.filter(currency=RateCurrencyChoices[rate['ccy']],
                                            source=source).first()

            if last_rate is None or last_rate.buy != rate['buy'] \
                    or last_rate.sell != rate['sale']:
                Rate.objects.create(
                    buy=rate['buy'],
                    sell=rate['sale'],
                    currency=RateCurrencyChoices[rate['ccy']],
                    source=source
                )


@shared_task(base=BaseTaskWithRetry)
def parse_monobank():
    from currency.models import Rate, Source

    source, _ = Source.objects.get_or_create(code=MonobankConfig.code,
                                             defaults=MonobankConfig.source_create_params)

    response = get_response_from_api(MonobankConfig.url)
    rates = json_to_decimal(response, keys_to_convert=['rateBuy', 'rateSell'])

    for rate in rates:
        if rate['currencyCodeA'] in AvailableCurrency.codes():
            code_name_enum = AvailableCurrency.from_code(rate['currencyCodeA'])
            last_rate = Rate.objects.filter(currency=RateCurrencyChoices[code_name_enum.name],
                                            source=source).first()

            if last_rate is None or last_rate.buy != rate['rateBuy'] \
                    or last_rate.sell != rate['rateSell']:
                Rate.objects.create(
                    buy=rate['rateBuy'],
                    sell=rate['rateSell'],
                    currency=RateCurrencyChoices[code_name_enum.name],
                    source=source
                )
