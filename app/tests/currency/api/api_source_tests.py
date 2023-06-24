from django.urls import reverse

api_sources_list_url = reverse('api-currency:sources-list')


# LIST GET
def test_api_source_list_status_code_on_get_no_auth(api_client):
    response = api_client.get(api_sources_list_url)
    assert response.status_code == 401


def test_api_source_list_errors_on_get_no_auth(api_client):
    response = api_client.get(api_sources_list_url)
    assert response.json() == {
        'detail': 'Authentication credentials were not provided.'
    }


def test_api_source_list_status_code_on_get(api_client_authorized):
    response = api_client_authorized.get(api_sources_list_url)
    assert response.status_code == 200


def test_api_source_list_on_get_with_empty_db(api_client_authorized):
    response = api_client_authorized.get(api_sources_list_url)
    assert len(response.json()['results']) == 0


def test_api_source_list_on_get_with_one_record(api_client_authorized, source):
    response = api_client_authorized.get(api_sources_list_url)
    assert len(response.json()['results']) == 1


def test_api_source_list_on_get_with_multiple_record(api_client_authorized, sources):
    response = api_client_authorized.get(api_sources_list_url)
    assert len(response.json()['results']) == len(sources)


def test_api_source_list_pagination_on_get(api_client_authorized, sources):
    response = api_client_authorized.get(api_sources_list_url)
    data = response.json()
    checks = {
        'results' in data,
        'next' in data,
        'previous' in data
    }
    assert all(checks)


# LIST POST
def test_api_source_list_status_code_on_post_no_auth_empty_submission(api_client):
    payload = {}
    response = api_client.post(api_sources_list_url, data=payload)
    assert response.status_code == 401


def test_api_source_list_errors_on_post_no_auth_empty_submission(api_client):
    payload = {}
    response = api_client.post(api_sources_list_url, data=payload)
    assert response.json() == {
        'detail': 'Authentication credentials were not provided.'
    }


def test_api_source_list_status_code_on_post_empty_submission(api_client_authorized):
    payload = {}
    response = api_client_authorized.post(api_sources_list_url, data=payload)
    assert response.status_code == 405


def test_api_source_list_errors_on_post_empty_submission(api_client_authorized):
    payload = {}
    response = api_client_authorized.post(api_sources_list_url, data=payload)
    assert response.json() == {
        'detail': 'Method \"POST\" not allowed.'
    }


# LIST PUT
def test_api_source_list_status_code_on_put_no_auth(api_client):
    response = api_client.put(api_sources_list_url)
    assert response.status_code == 401


def test_api_source_list_errors_on_put_no_auth(api_client):
    response = api_client.put(api_sources_list_url)
    assert response.json() == {
        'detail': 'Authentication credentials were not provided.'
    }


def test_api_source_list_status_code_on_put(api_client_authorized):
    response = api_client_authorized.put(api_sources_list_url)
    assert response.status_code == 405


def test_api_source_list_errors_on_put(api_client_authorized):
    response = api_client_authorized.put(api_sources_list_url)
    assert response.json() == {
        'detail': 'Method \"PUT\" not allowed.'
    }


# LIST DELETE
def test_api_source_list_status_code_on_delete_no_auth(api_client):
    response = api_client.delete(api_sources_list_url)
    assert response.status_code == 401


def test_api_source_list_errors_on_delete_no_auth(api_client):
    response = api_client.delete(api_sources_list_url)
    assert response.json() == {
        'detail': 'Authentication credentials were not provided.'
    }


def test_api_source_list_status_code_on_delete(api_client_authorized):
    response = api_client_authorized.delete(api_sources_list_url)
    assert response.status_code == 405


def test_api_source_list_errors_on_delete(api_client_authorized):
    response = api_client_authorized.delete(api_sources_list_url)
    assert response.json() == {
        'detail': 'Method \"DELETE\" not allowed.'
    }


# DETAILS GET
def test_api_source_details_status_code_on_get_no_auth(api_client, source):
    response = api_client.get(api_sources_list_url + f'{source.id}/')
    assert response.status_code == 401


def test_api_source_details_errors_on_get_no_auth(api_client, source):
    response = api_client.get(api_sources_list_url + f'{source.id}/')
    assert response.json() == {
        'detail': 'Authentication credentials were not provided.'
    }


def test_api_source_details_status_code_on_get(api_client_authorized, source):
    response = api_client_authorized.get(api_sources_list_url + f'{source.id}/')
    assert response.status_code == 200


def test_api_source_details_return_obj_on_get(api_client_authorized, source):
    response = api_client_authorized.get(api_sources_list_url + f'{source.id}/')
    assert response.json() == {
        'id': source.id,
        'url': source.url,
        'code': source.code,
        'name': source.name,
        'city': source.city,
        'phone': source.phone
    }


# DETAILS PUT
def test_api_source_details_status_code_on_put_no_auth(api_client, source):
    response = api_client.put(api_sources_list_url + f'{source.id}/')
    assert response.status_code == 401


def test_api_source_details_errors_on_put_no_auth(api_client, source):
    response = api_client.put(api_sources_list_url + f'{source.id}/')
    assert response.json() == {
        'detail': 'Authentication credentials were not provided.'
    }


def test_api_source_details_status_code_on_put(api_client_authorized, source):
    response = api_client_authorized.put(api_sources_list_url + f'{source.id}/')
    assert response.status_code == 405


def test_api_source_details_errors_on_put(api_client_authorized, source):
    response = api_client_authorized.put(api_sources_list_url + f'{source.id}/')
    assert response.json() == {
        'detail': 'Method \"PUT\" not allowed.'
    }


# DETAILS DELETE
def test_api_source_details_status_code_on_delete_no_auth(api_client, source):
    response = api_client.delete(api_sources_list_url + f'{source.id}/')
    assert response.status_code == 401


def test_api_source_details_errors_on_delete_no_auth(api_client, source):
    response = api_client.delete(api_sources_list_url + f'{source.id}/')
    assert response.json() == {
        'detail': 'Authentication credentials were not provided.'
    }


def test_api_source_details_status_code_on_delete(api_client_authorized, source):
    response = api_client_authorized.delete(api_sources_list_url + f'{source.id}/')
    assert response.status_code == 405


def test_api_source_details_errors_on_delete(api_client_authorized, source):
    response = api_client_authorized.delete(api_sources_list_url + f'{source.id}/')
    assert response.json() == {
        'detail': 'Method \"DELETE\" not allowed.'
    }


# Throttling test
def test_api_source_list_status_code_on_get_throttling(api_client_authorized, api_throttling_rate,
                                                       source):
    response = api_client_authorized.get(api_sources_list_url)
    for _ in range(api_throttling_rate):
        response = api_client_authorized.get(api_sources_list_url)
    assert response.status_code == 429


def test_api_source_details_status_code_on_get_throttling(api_client_authorized,
                                                          api_throttling_rate, source):
    response = api_client_authorized.get(api_sources_list_url + f'{source.id}/')
    for _ in range(api_throttling_rate):
        response = api_client_authorized.get(api_sources_list_url + f'{source.id}/')
    assert response.status_code == 429
