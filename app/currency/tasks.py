from bs4 import BeautifulSoup
from celery import shared_task

from currency.constants import AvailableCurrency, MonobankConfig, NBUConfig, PrivatbankConfig
from currency.models import RateCurrencyChoices
from utils.celery_classes import BaseTaskWithRetry
from utils.common import get_response, json_to_decimal


def extract_nbu_data():
    response = get_response(NBUConfig.url, return_html=True)
    soup = BeautifulSoup(response, 'html.parser')

    table = soup.find('table', {'id': 'exchangeRates'})
    tbody = table.find('tbody')
    trows = tbody.find_all('tr')
    page_data = []
    # creating some sort of JSON (dict) that can be processed by json_to_decimal func
    for tr in trows:
        page_data.append(
            {
                'num_code': tr.find('td', {'data-label': 'Код цифровий'}).span.text,
                'short_name': tr.find('td', {'data-label': 'Код літерний'}).text,
                'buy': tr.find('td', {'data-label': 'Офіційний курс'}).text,
                'sell': tr.find('td', {'data-label': 'Офіційний курс'}).text,
            }
        )
    return page_data


@shared_task(base=BaseTaskWithRetry)
def parse_privatbank():
    from currency.models import Rate, Source

    source, _ = Source.objects.get_or_create(code=PrivatbankConfig.code,
                                             defaults=PrivatbankConfig.source_create_params)

    response = get_response(PrivatbankConfig.url)
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

    response = get_response(MonobankConfig.url)
    rates = json_to_decimal(response, keys_to_convert=['rateBuy', 'rateSell'])

    for rate in rates:
        if rate['currencyCodeA'] in AvailableCurrency.codes() and \
                rate['currencyCodeB'] == AvailableCurrency.UAH.value:
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


@shared_task(base=BaseTaskWithRetry)
def parse_nbu():
    from currency.models import Rate, Source
    source, _ = Source.objects.get_or_create(code=NBUConfig.code,
                                             defaults=NBUConfig.source_create_params)

    rates = json_to_decimal(extract_nbu_data(), keys_to_convert=['buy', 'sell'])
    for rate in rates:
        if rate['short_name'] in AvailableCurrency.names():
            last_rate = Rate.objects.filter(currency=RateCurrencyChoices[rate['short_name']],
                                            source=source).first()

            if last_rate is None or last_rate.buy != rate['buy'] or last_rate.sell != rate['sell']:
                Rate.objects.create(
                    buy=rate['buy'],
                    sell=rate['sell'],
                    currency=RateCurrencyChoices[rate['short_name']],
                    source=source
                )
