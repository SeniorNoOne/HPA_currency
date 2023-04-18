import re
import requests

from decimal import Decimal
from pathlib import Path


def get_upload_to_path(instance, file_name, unique_key='username'):
    return get_instance_path(instance, unique_key) + '/' + file_name


def get_instance_path(instance, unique_key):
    return str(
        Path(instance.__class__.__name__ + '/' +
             str(getattr(instance, unique_key))
             )
    )


def get_response(url, return_html=False):
    response = requests.get(url)
    response.raise_for_status()
    return response.content if return_html else response.json()


def json_to_decimal(json_lst, decimal_places=2, keys_to_convert=None):
    for _json in json_lst:
        keys = _json.keys() if keys_to_convert is None else keys_to_convert
        for key in keys:
            value = str(_json[key])
            if value and re.match(r'^[0-9]*[\.,][0-9]+$', value):
                value = value.replace(',', '.')
                _json[key] = Decimal(value).quantize(Decimal(f'1.{"0" * decimal_places}'))
    return json_lst
