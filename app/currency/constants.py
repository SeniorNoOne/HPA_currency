from enum import Enum

from django.templatetags.static import static


class AvailableCurrency(int, Enum):
    def __new__(cls, num_code, full_name):
        obj = int.__new__(cls, num_code)
        obj._value_ = num_code
        obj.full_name = full_name
        return obj

    @classmethod
    def names(cls):
        return [currency.name for currency in cls]

    @classmethod
    def codes(cls):
        return [currency.value for currency in cls]

    @classmethod
    def full_names(cls):
        return [currency.full_name for currency in cls]

    @classmethod
    def choices(cls):
        return [(idx, currency.full_name) for idx, currency in enumerate(cls)]

    @classmethod
    def from_code(cls, code):
        for currency in cls:
            if currency.value == code:
                return currency

    USD = (840, 'US Dollar')
    EUR = (978, 'Euro')
    GBP = (826, 'Pound Sterling')
    JPY = (392, 'Yen')
    UAH = (980, 'Ukrainian hryvnia')


class PrivatbankConfig:
    code = 0
    name = 'PrivatBank'
    url = 'https://api.privatbank.ua/p24api/pubinfo?exchange&json&coursid=11'
    logo = static('images/source_privatbank_logo.png')
    source_create_params = {
        'code': code,
        'name': name,
        'url': url,
        'logo': logo,
    }


class MonobankConfig:
    code = 1
    name = 'Monobank'
    url = 'https://api.monobank.ua/bank/currency'
    logo = static('images/source_monobank_logo.png')
    source_create_params = {
        'code': code,
        'name': name,
        'url': url,
        'logo': logo,
    }


class NBUConfig:
    code = 2
    name = 'NBU'
    url = 'https://bank.gov.ua/ua/markets/exchangerates'
    logo = static('images/source_nbu_logo.png')
    source_create_params = {
        'code': code,
        'name': name,
        'url': url,
        'logo': logo,
    }


class StorageUniqueFields:
    source = 'code'


class RateFilterConfig:
    filter_fields = (
        'buy',
        'sell',
        'source__name',
    )

    buy = (
        ('exact', 'Exact'),
        ('lt', 'Less than'),
        ('lte', 'Less than or equal to'),
        ('gt', 'Greater than'),
        ('gte', 'Greater than or equal to'),
    )

    sell = (
        ('exact', 'Exact'),
        ('lt', 'Less than'),
        ('lte', 'Less than or equal to'),
        ('gt', 'Greater than'),
        ('gte', 'Greater than or equal to'),
    )

    source_name = (
        ('icontains', 'Contains'),
        ('exact', 'Exact'),
    )


LATEST_RATE_CACHE_KEY = 'api::currency::rates::latest'
