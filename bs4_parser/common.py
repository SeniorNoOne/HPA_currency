import requests
from bs4 import BeautifulSoup

from constants import AutoriaConfig, RandomUserAgent, FilesDir
from classes import CSVWriter, SQLiteWriter, ProgressBar


def get_response(url, return_html=False, params=None, headers=None):
    response = requests.get(url, params=params, headers=headers)
    response.raise_for_status()
    return response.text if return_html else response.json()


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
    bar = ProgressBar()
    query_params = AutoriaConfig.query_params
    file_writers = (
        CSVWriter(FilesDir + 'autoria.csv', AutoriaConfig.headers),
        SQLiteWriter(FilesDir + 'autoria.sqlite3',
                     AutoriaConfig.sql['table_queries'],
                     AutoriaConfig.sql['insert_query']
                     )
    )

    try:
        while True:
            headers = RandomUserAgent()
            content = get_response(AutoriaConfig.url,
                                   params=query_params,
                                   headers=headers,
                                   return_html=True
                                   )

            # Parsing search page
            soup = BeautifulSoup(content, features="html.parser")
            search_results = soup.find("div", {"id": "searchResults"})
            items = search_results.find_all("section", {"class": "ticket-item"})

            # If nothing found parsing stops
            if not items:
                break

            # Otherwise parsing each search result
            for index, ticket_item in enumerate(items):
                # Updating and printing progress bar
                bar.show(index,
                         query_params['size'],
                         f'item {index} on page {query_params["page"]}'
                         )

                # Getting data from search result item
                data = {key: None for key in AutoriaConfig.headers}
                post_details = ticket_item.find("div", {"class": "hide"})
                data |= parse_item(post_details, AutoriaConfig.headers_config)

                # Getting HTML page of search item
                car_page = get_response(AutoriaConfig.base_url +
                                        post_details['data-link-to-view'],
                                        return_html=True
                                        )
                item_soup = BeautifulSoup(car_page, features='html.parser')
                item_details = item_soup.find('div', {'class': 'technical-info'})

                # Skipping item if its page does not have any technical-info
                if item_details is None:
                    continue

                # Otherwise parsing data from technical-info
                item_details = item_details.find_all('dd')
                for lst in item_details:
                    data |= parse_item(lst, AutoriaConfig.items_config)

                # Writing data in files
                for writer in file_writers:
                    writer.write_row(data)
            query_params['page'] += 1

    # Closing writers before exiting
    except KeyboardInterrupt:
        for writer in file_writers:
            writer.close()
