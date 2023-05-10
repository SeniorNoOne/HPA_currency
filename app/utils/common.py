import re
import requests
from decimal import Decimal

from django.core.files.storage import default_storage


def get_instance_path(instance, unique_field_name):
    model_name = instance.__class__.__name__
    path_to_instance = model_name + '/' + str(getattr(instance, unique_field_name))
    return path_to_instance


def get_upload_to_path(instance, unique_field_name, filename):
    path_to_instance = get_instance_path(instance, unique_field_name)
    return path_to_instance + '/' + filename


def delete_dir(instance, unique_field_name):
    path_to_instance = get_instance_path(instance, unique_field_name)
    try:
        dirs = default_storage.listdir(path_to_instance)
        for file_name in dirs[1]:
            file_path = f"{path_to_instance}/{file_name}"
            default_storage.delete(file_path)
        default_storage.delete(path_to_instance)
    except FileNotFoundError:
        pass


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
