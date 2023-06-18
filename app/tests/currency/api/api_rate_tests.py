from django.urls import reverse

api_rates_list_url = reverse('api-currency:rates-list')


# LIST GET
def test_api_rate_list_status_code_on_get(api_client):
    response = api_client.get(api_rates_list_url)
    assert response.status_code == 200


def test_api_rate_list_on_get_with_empty_db(api_client):
    response = api_client.get(api_rates_list_url)
    assert len(response.json()['results']) == 0


def test_api_rate_list_on_get_with_one_record(api_client, rate):
    response = api_client.get(api_rates_list_url)
    assert len(response.json()['results']) == 1


def test_api_rate_list_on_get_with_multiple_records(api_client, rates):
    response = api_client.get(api_rates_list_url)
    assert len(response.json()['results']) == len(rates)


def test_api_rate_list_pagination_on_get(api_client, rates):
    response = api_client.get(api_rates_list_url)
    data = response.json()
    checks = {
        'count' in data,
        'next' in data,
        'previous' in data
    }
    assert all(checks)


# LIST POST
def test_api_rate_list_status_code_on_post_empty_data(api_client):
    payload = {}
    response = api_client.post(api_rates_list_url, data=payload)
    assert response.status_code == 400


def test_api_rate_list_errors_on_post_empty_data(api_client):
    payload = {}
    response = api_client.post(api_rates_list_url, data=payload)
    assert response.json() == {
        'buy': ['This field is required.'],
        'sell': ['This field is required.'],
        'source': ['This field is required.']
    }


def test_api_rate_list_status_code_on_post_invalid_buy_field(api_client, source, rate):
    payload = {
        'buy': '',
        'sell': rate.sell,
        'source': source.id
    }
    response = api_client.post(api_rates_list_url, data=payload)
    assert response.status_code == 400


def test_api_rate_list_errors_on_post_invalid_buy_field(api_client, source, rate):
    payload = {
        'buy': '',
        'sell': rate.sell,
        'source': source.id
    }
    response = api_client.post(api_rates_list_url, data=payload)
    assert response.json() == {
        'buy': ['A valid number is required.']
    }


def test_api_rate_list_status_code_on_post_empty_buy_field(api_client, source, rate):
    payload = {
        'sell': rate.sell,
        'source': source.id
    }
    response = api_client.post(api_rates_list_url, data=payload)
    assert response.status_code == 400


def test_api_rate_list_errors_on_post_empty_buy_field(api_client, source, rate):
    payload = {
        'sell': rate.sell,
        'source': source.id
    }
    response = api_client.post(api_rates_list_url, data=payload)
    assert response.json() == {
        'buy': ['This field is required.']
    }


def test_api_rate_list_status_code_on_post_invalid_sell_field(api_client, source, rate):
    payload = {
        'buy': rate.buy,
        'sell': '',
        'source': source.id
    }
    response = api_client.post(api_rates_list_url, data=payload)
    assert response.status_code == 400


def test_api_rate_list_errors_on_post_invalid_sell_field(api_client, source, rate):
    payload = {
        'buy': rate.buy,
        'sell': '',
        'source': source.id
    }
    response = api_client.post(api_rates_list_url, data=payload)
    assert response.json() == {
        'sell': ['A valid number is required.']
    }


def test_api_rate_list_status_code_on_post_empty_sell_field(api_client, source, rate):
    payload = {
        'buy': rate.buy,
        'source': source.id
    }
    response = api_client.post(api_rates_list_url, data=payload)
    assert response.status_code == 400


def test_api_rate_list_errors_on_post_empty_sell_field(api_client, source, rate):
    payload = {
        'buy': rate.buy,
        'source': source.id
    }
    response = api_client.post(api_rates_list_url, data=payload)
    assert response.json() == {
        'sell': ['This field is required.']
    }


def test_api_rate_list_status_code_on_post_invalid_source_field(api_client, source, rate):
    payload = {
        'buy': rate.buy,
        'sell': rate.sell,
        'source': ''
    }
    response = api_client.post(api_rates_list_url, data=payload)
    assert response.status_code == 400


def test_api_rate_list_errors_on_post_invalid_source_field(api_client, source, rate):
    payload = {
        'buy': rate.buy,
        'sell': rate.sell,
        'source': ''
    }
    response = api_client.post(api_rates_list_url, data=payload)
    assert response.json() == {
        'source': ['This field may not be null.']
    }


def test_api_rate_list_status_code_on_post_empty_source_field(api_client, source, rate):
    payload = {
        'buy': rate.buy,
        'sell': rate.sell,
    }
    response = api_client.post(api_rates_list_url, data=payload)
    assert response.status_code == 400


def test_api_rate_list_errors_on_post_empty_source_field(api_client, source, rate):
    payload = {
        'buy': rate.buy,
        'sell': rate.sell,
    }
    response = api_client.post(api_rates_list_url, data=payload)
    assert response.json() == {
        'source': ['This field is required.']
    }


def test_api_rate_list_status_code_on_post_valid_submission(api_client, source, rate):
    payload = {
        'buy': rate.buy,
        'sell': rate.sell,
        'source': source.id
    }
    response = api_client.post(api_rates_list_url, data=payload)
    assert response.status_code == 201


def test_api_rate_list_return_obj_on_post_valid_submission(api_client, rate):
    payload = {
        'buy': str(rate.buy),
        'sell': str(rate.sell),
        'currency': rate.currency,
        'source': rate.source.id
    }
    response = api_client.post(api_rates_list_url, data=payload)
    data = response.json()
    data.pop('created')
    payload['id'] = rate.id + 1
    assert data == payload


# LIST PUT
def test_api_rate_list_status_code_on_put(api_client):
    response = api_client.put(api_rates_list_url)
    assert response.status_code == 405


def test_api_rate_list_errors_on_put(api_client):
    response = api_client.put(api_rates_list_url)
    assert response.json() == {
        'detail': 'Method \"PUT\" not allowed.'
    }


# LIST PATCH
def test_api_rate_list_status_code_on_patch(api_client):
    response = api_client.patch(api_rates_list_url)
    assert response.status_code == 405


def test_api_rate_list_errors_on_patch(api_client):
    response = api_client.patch(api_rates_list_url)
    assert response.json() == {
        'detail': 'Method \"PATCH\" not allowed.'
    }


# LIST HEAD
def test_api_rate_list_status_code_on_head(api_client):
    response = api_client.head(api_rates_list_url)
    assert response.status_code == 200


# LIST OPTIONS
def test_api_rate_list_status_code_on_options(api_client):
    response = api_client.options(api_rates_list_url)
    assert response.status_code == 200


# LIST DELETE
def test_api_rate_list_status_code_on_delete(api_client):
    response = api_client.head(api_rates_list_url)
    assert response.status_code == 200


# DETAILS GET
def test_api_rate_details_status_code_on_get(api_client, rate):
    response = api_client.get(api_rates_list_url + f'{rate.id}/')
    assert response.status_code == 200


def test_api_rate_details_return_obj_on_get(api_client, rate):
    response = api_client.get(api_rates_list_url + f'{rate.id}/')
    data = response.json()
    data.pop('created')
    assert data == {
        'id': rate.id,
        'buy': str(rate.buy),
        'sell': str(rate.sell),
        'currency': rate.currency,
        'source': rate.source.id
    }


def test_api_rate_details_status_code_on_get_invalid_id(api_client):
    response = api_client.get(api_rates_list_url + f'{-1}/')
    assert response.status_code == 404


def test_api_rate_details_errors_on_get_invalid_id(api_client):
    response = api_client.get(api_rates_list_url + f'{-1}/')
    assert response.json() == {
        'detail': 'Not found.'
    }


# DETAILS PUT
def test_api_rate_details_status_code_on_put_valid_submission(api_client, rate):
    payload = {
        'id': rate.id,
        'buy': str(rate.buy),
        'sell': str(rate.sell),
        'currency': rate.currency,
        'source': rate.source.id
    }
    response = api_client.put(api_rates_list_url + f'{rate.id}/', data=payload)
    assert response.status_code == 200


def test_api_rate_details_errors_on_put_valid_submission(api_client, rate):
    payload = {
        'id': rate.id,
        'buy': str(rate.buy),
        'sell': str(rate.sell),
        'currency': rate.currency,
        'source': rate.source.id
    }
    response = api_client.put(api_rates_list_url + f'{rate.id}/', data=payload)
    data = response.json()
    data.pop('created')
    assert data == payload


def test_api_rate_details_status_code_on_put_empty_submission(api_client, rate):
    payload = {}
    response = api_client.put(api_rates_list_url + f'{rate.id}/', data=payload)
    assert response.status_code == 400


def test_api_rate_details_errors_on_put_empty_submission(api_client, rate):
    payload = {}
    response = api_client.put(api_rates_list_url + f'{rate.id}/', data=payload)
    assert response.json() == {
        'buy': ['This field is required.'],
        'sell': ['This field is required.'],
        'source': ['This field is required.']
    }


def test_api_rate_details_status_code_on_put_new_buy_field(api_client, rate):
    payload = {
        'id': rate.id,
        'buy': str(rate.buy + 1),
        'sell': str(rate.sell),
        'currency': rate.currency,
        'source': rate.source.id
    }
    response = api_client.put(api_rates_list_url + f'{rate.id}/', data=payload)
    assert response.status_code == 200


def test_api_rate_details_return_obj_on_put_new_buy_field(api_client, rate):
    payload = {
        'id': rate.id,
        'buy': str(rate.buy + 1),
        'sell': str(rate.sell),
        'currency': rate.currency,
        'source': rate.source.id
    }
    response = api_client.put(api_rates_list_url + f'{rate.id}/', data=payload)
    data = response.json()
    data.pop('created')
    assert data == payload


def test_api_rate_details_status_code_on_put_new_sell_field(api_client, rate):
    payload = {
        'id': rate.id,
        'buy': str(rate.buy),
        'sell': str(rate.sell + 1),
        'currency': rate.currency,
        'source': rate.source.id
    }
    response = api_client.put(api_rates_list_url + f'{rate.id}/', data=payload)
    assert response.status_code == 200


def test_api_rate_details_return_obj_on_put_new_sell_field(api_client, rate):
    payload = {
        'id': rate.id,
        'buy': str(rate.buy),
        'sell': str(rate.sell + 1),
        'currency': rate.currency,
        'source': rate.source.id
    }
    response = api_client.put(api_rates_list_url + f'{rate.id}/', data=payload)
    data = response.json()
    data.pop('created')
    assert data == payload


def test_api_rate_details_status_code_on_put_new_currency_field(api_client, source, rate):
    payload = {
        'id': rate.id,
        'buy': str(rate.buy),
        'sell': str(rate.sell),
        'currency': rate.currency + 1,
        'source': rate.source.id
    }
    response = api_client.put(api_rates_list_url + f'{rate.id}/', data=payload)
    assert response.status_code == 200


def test_api_rate_details_return_obj_on_put_new_currency_field(api_client, source, rate):
    payload = {
        'id': rate.id,
        'buy': str(rate.buy),
        'sell': str(rate.sell),
        'currency': rate.currency + 1,
        'source': rate.source.id
    }
    response = api_client.put(api_rates_list_url + f'{rate.id}/', data=payload)
    data = response.json()
    data.pop('created')
    assert data == payload


def test_api_rate_details_status_code_on_put_new_source_field(api_client, source, rate):
    payload = {
        'id': rate.id,
        'buy': str(rate.buy),
        'sell': str(rate.sell),
        'currency': rate.currency,
        'source': source.id
    }
    response = api_client.put(api_rates_list_url + f'{rate.id}/', data=payload)
    assert response.status_code == 200


def test_api_rate_details_return_obj_on_put_new_source_field(api_client, source, rate):
    payload = {
        'id': rate.id,
        'buy': str(rate.buy),
        'sell': str(rate.sell),
        'currency': rate.currency,
        'source': source.id
    }
    response = api_client.put(api_rates_list_url + f'{rate.id}/', data=payload)
    data = response.json()
    data.pop('created')
    assert data == payload


# DETAILS DELETE
def test_api_rate_details_status_code_on_delete_valid_submission(api_client, rate):
    response = api_client.delete(api_rates_list_url + f'{rate.id}/')
    assert response.status_code == 204


def test_api_rate_details_status_code_on_delete_invalid_submission(api_client):
    response = api_client.delete(api_rates_list_url + '-1/')
    assert response.status_code == 404


# Caching test of latest endpoint
def test_api_rate_list_latest_endpoint_status_code_on_get(api_client, rate):
    response = api_client.get(api_rates_list_url + 'latest/')
    assert response.status_code == 200


def test_api_rate_list_latest_endpoint_return_obj_on_get(api_client, rate, rate_caching):
    cache, cache_key = rate_caching
    payload = {
        'id': rate.id,
        'buy': str(rate.buy),
        'sell': str(rate.sell),
        'currency': rate.currency,
        'source': rate.source.id,
    }

    # Creating cache
    api_client.get(api_rates_list_url + 'latest/')

    # Accessing cache
    api_client.get(api_rates_list_url + 'latest/')

    # Reading cache value
    cache_val = cache.get(cache_key)[0]
    cache_val.pop('created')
    assert payload == cache_val


def test_api_rate_list_latest_endpoint_status_code_on_get_rate_creation(api_client, rate, rate_data,
                                                                        rate_caching):
    cache, cache_key = rate_caching

    # Creating cache
    api_client.get(api_rates_list_url + 'latest/')
    cache_initial_val = cache.get(cache_key)[0]

    # Creating new rate which deletes cache key
    rate_data.source.save()
    rate_data.save()

    checks = (
        len(cache_initial_val),
        cache.get(cache_key) is None
    )
    assert all(checks)
