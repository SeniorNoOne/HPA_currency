import json
import re
import requests

from decimal import Decimal
from pathlib import Path


def get_upload_to_path(instance, filename, field_name='username'):
    return Path(str(getattr(instance, field_name, instance.id))) / filename


def get_response_from_api(url):
    response = requests.get(url)
    response.raise_for_status()
    return json.loads(response.text)


def json_to_decimal(json_lst, decimal_places=2, keys_to_convert=None):
    for _json in json_lst:
        keys = _json.keys() if keys_to_convert is None else keys_to_convert
        for key in keys:
            value = str(_json[key])
            if value and re.match(r'^[0-9]*\.?[0-9]+$', value):
                _json[key] = Decimal(value).quantize(Decimal(f'1.{"0" * decimal_places}'))
    return json_lst
