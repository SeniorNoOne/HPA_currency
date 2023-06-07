import random


class AutoriaConfig:
    url = 'https://auto.ria.com/uk/search/'
    base_url = 'https://auto.ria.com/uk'
    query_params = {
        'size': 100,
        'page': 0
    }
    headers_config = {
        'car_id': {
            'headers': None,
            'data': {
                'key': 'data-id',
                'handler': None
            }
        },

        'data_link': {
            'headers': None,
            'data': {
                'key': 'data-link-to-view',
                'handler': None
            }
        },

    }
    items_config = {
        'mileage': {
            'headers': {
                'tag': 'span',
                'search_kwargs': {
                    'class_': 'label'
                },
                'value': 'Пробіг перевірено',
            },
            'data': {
                'tag': 'span',
                'search_kwargs': {
                    'class_': 'argument',
                },
                'handler': lambda x: x.contents[0].replace('км', '').replace(' тис.', 'K').strip()
            }
        },

        'car_decs': {
            'headers': {
                'tag': 'span',
                'search_kwargs': {
                    'class_': 'label'
                },
                'value': 'Марка, модель, рік',
            },
            'data': {
                'tag': 'span',
                'search_kwargs': {
                    'class_': 'argument'
                },
                'handler': lambda x: x.text
            }
        },

        'engine': {
            'headers': {
                'tag': 'span',
                'search_kwargs': {
                    'class_': 'label'
                },
                'value': 'Двигун',
            },
            'data': {
                'tag': 'span',
                'search_kwargs': {
                    'class_': 'argument'
                },
                'handler': lambda x: x.text.replace('• ', '').replace(' л', 'L')
            }
        }
    }
    headers = list(headers_config) + list(items_config)


class RandomUserAgent:
    user_agents = (
        'Mozilla/5.0 (Windows NT x.y; rv:10.0) Gecko/20100101 Firefox/10.0',
        'Mozilla/5.0 (Windows NT x.y; Win64; x64; rv:10.0) Gecko/20100101 Firefox/10.0',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X x.y; rv:10.0) Gecko/20100101 Firefox/10.0',
        'Mozilla/5.0 (Macintosh; PPC Mac OS X x.y; rv:10.0) Gecko/20100101 Firefox/10.0',
        'Mozilla/5.0 (X11; Linux i686; rv:10.0) Gecko/20100101 Firefox/10.0',
        'Mozilla/5.0 (X11; Linux x86_64; rv:10.0) Gecko/20100101 Firefox/10.0'

        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
        'Chrome/114.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 '
        '(KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 '
        '(KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 13_4) AppleWebKit/537.36 (KHTML, like Gecko) '
        'Chrome/114.0.0.0 Safari/537.36',
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 '
        '(KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'
    )

    def __call__(self):
        return {
            "User-Agent": random.choice(self.user_agents)
        }


RandomUserAgent = RandomUserAgent()
