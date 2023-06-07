import re
import requests
from decimal import Decimal

from bs4 import BeautifulSoup
from django.core.files.storage import default_storage


from constants import AutoriaConfig, RandomUserAgent, TABLE_QUERIES, INSERT_QUERY
from classes import CSVWriter, SQLiteWriter


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


# Beautiful soup 4 parser
def get_response(url, return_html=False, params=None, headers=None):
    response = requests.get(url, params=params, headers=headers)
    response.raise_for_status()
    return response.text if return_html else response.json()


def json_to_decimal(json_lst, decimal_places=2, keys_to_convert=None):
    for _json in json_lst:
        keys = _json.keys() if keys_to_convert is None else keys_to_convert
        for key in keys:
            value = str(_json[key])
            if value and re.match(r'^[0-9]*[\.,][0-9]+$', value):
                value = value.replace(',', '.')
                _json[key] = Decimal(value).quantize(Decimal(f'1.{"0" * decimal_places}'))
    return json_lst


def parse_item(search_result, config):
    items_data = {}
    for item_config in config:
        item_headers = config[item_config]['headers']
        item_data = config[item_config]['data']
        if item_headers:
            data = search_result.find(item_headers['tag'], **item_headers['search_kwargs'])
            if data and data.text == item_headers['value']:
                data = search_result.find(item_data['tag'], **item_data['search_kwargs'])
                if data and item_data['handler']:
                    data = item_data['handler'](data)
                items_data[item_config] = data
        else:
            data = search_result[item_data['key']]
            if data and item_data['handler']:
                data = item_data['handler'](data)
            items_data[item_config] = data
    return items_data


def parse_autoria():
    file_writers = (
        CSVWriter('autoria.csv', AutoriaConfig.headers),
        SQLiteWriter('autoria.db', TABLE_QUERIES, INSERT_QUERY)
    )
    params = AutoriaConfig.query_params
    page = 0

    while True:
        headers = RandomUserAgent()
        params['page'] = page
        content = get_response(AutoriaConfig.url, params=params, headers=headers, return_html=True)

        soup = BeautifulSoup(content, features="html.parser")

        search_results = soup.find("div", {"id": "searchResults"})
        items = search_results.find_all("section", {"class": "ticket-item"})

        if not items:
            break

        for ticket_item in items:
            data = {key: None for key in AutoriaConfig.headers}
            post_details = ticket_item.find("div", {"class": "hide"})
            data |= parse_item(post_details, AutoriaConfig.headers_config)

            car_page = get_response(AutoriaConfig.base_url +
                                    post_details['data-link-to-view'],
                                    return_html=True)
            soup_1 = BeautifulSoup(car_page, features='html.parser')
            item_details = soup_1.find('div', {'class': 'technical-info'})
            item_details = item_details.find_all('dd')
            for lst in item_details:
                data |= parse_item(lst, AutoriaConfig.items_config)

            for writer in file_writers:
                writer.write_row(data)
        page += 1


if __name__ == '__main__':
    parse_autoria()
