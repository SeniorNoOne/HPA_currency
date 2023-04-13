from enum import Enum


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

    USD = (840, 'US Dollar')
    EUR = (978, 'Euro')
    GBP = (826, 'Pound Sterling')
    JPY = (392, 'Yen')


class PrivatConfig:
    source_code = 0
    source_name = 'PrivatBank'
    source_url = 'https://api.privatbank.ua/p24api/pubinfo?exchange&json&coursid=11'
    source_create_params = {
        'code': source_code,
        'name': source_name,
        'source_url': source_url,
    }


class MonoConfig:
    source_code = 1
    source_name = 'Monobank'
    source_url = 'https://api.monobank.ua/bank/currency'
    source_create_params = {
        'code': source_code,
        'name': source_name,
        'source_url': source_url
    }
