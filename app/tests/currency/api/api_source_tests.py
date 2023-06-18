from django.urls import reverse

api_sources_list_url = reverse('api-currency:sources-list')


# LIST GET
def test_get_source_list_status_200(api_client_authorized):
    response = api_client_authorized.get(api_sources_list_url)
    assert response.status_code == 200


def test_get_source_list_empty_db(api_client_authorized):
    response = api_client_authorized.get(api_sources_list_url)
    assert len(response.json()['results']) == 0


def test_get_source_list_single_entity(api_client_authorized, source):
    response = api_client_authorized.get(api_sources_list_url)
    assert len(response.json()['results']) == 1


def test_get_source_list_multiple_entities(api_client_authorized, sources):
    response = api_client_authorized.get(api_sources_list_url)
    assert len(response.json()['results']) == len(sources)


def test_get_source_list_pagination(api_client_authorized, sources):
    response = api_client_authorized.get(api_sources_list_url)
    json = response.json()
    checks = {
        'count' in json,
        'next' in json,
        'previous' in json
    }
    assert all(checks)


# LIST POST
def test_post_source_list_empty_payload_status_405(api_client_authorized, user):
    payload = {}
    api_client_authorized.force_login(user)
    response = api_client_authorized.post(api_sources_list_url, data=payload)
    assert response.status_code == 405


# DETAILS GET
def test_get_source_details_status_200(api_client_authorized, source):
    response = api_client_authorized.get(api_sources_list_url + f'{source.id}/')
    assert response.status_code == 200


def test_get_source_details_status_404(api_client_authorized):
    response = api_client_authorized.get(api_sources_list_url + f'{-1}/')
    assert response.status_code == 404


def test_get_source_details_data(api_client_authorized, source):
    response = api_client_authorized.get(api_sources_list_url + f'{source.id}/')
    assert response.json() == {
        'url': source.url,
        'code': source.code,
        'city': source.city,
        'phone': source.phone
    }


# DETAILS PUT
def test_put_source_details_same_source_status_405(api_client_authorized, source):
    payload = {
        'id': source.id,
        'url': source.url,
        'code': source.code,
    }
    response = api_client_authorized.put(api_sources_list_url + f'{source.id}/', data=payload)
    assert response.status_code == 405


def test_put_source_details_same_source_data(api_client_authorized, source):
    payload = {
        'id': source.id,
        'url': source.url,
        'code': source.code,
    }
    response = api_client_authorized.put(api_sources_list_url + f'{source.id}/', data=payload)
    assert response.json() == {'detail': 'Method \"PUT\" not allowed.'}


# DETAILS DELETE
def test_delete_source_details_status_405(api_client_authorized, source):
    response = api_client_authorized.delete(api_sources_list_url + f'{source.id}/')
    assert response.status_code == 405


def test_delete_source_details_same_source_data(api_client_authorized, source):
    payload = {
        'id': source.id,
        'url': source.url,
        'code': source.code,
    }
    response = api_client_authorized.delete(api_sources_list_url + f'{source.id}/', data=payload)
    assert response.json() == {'detail': 'Method \"DELETE\" not allowed.'}


# Throttling test
def test_get_source_list_status_429(api_client_authorized, api_throttling_rate, source):
    response = api_client_authorized.get(api_sources_list_url)
    for _ in range(api_throttling_rate):
        response = api_client_authorized.get(api_sources_list_url)
    assert response.status_code == 429


def test_get_source_details_status_429(api_client_authorized, api_throttling_rate, source):
    response = api_client_authorized.get(api_sources_list_url + f'{source.id}/')
    for _ in range(api_throttling_rate):
        response = api_client_authorized.get(api_sources_list_url + f'{source.id}/')
    assert response.status_code == 429


def test_put_source_status_429(api_client_authorized, api_throttling_rate, source):
    payload = {}
    response = api_client_authorized.put(api_sources_list_url + f'{source.id}/', data=payload)
    for _ in range(api_throttling_rate):
        response = api_client_authorized.put(api_sources_list_url + f'{source.id}/', data=payload)
    assert response.status_code == 429


def test_delete_source_status_429(api_client_authorized, api_throttling_rate, source):
    response = api_client_authorized.delete(api_sources_list_url + f'{source.id}/')
    for _ in range(api_throttling_rate):
        response = api_client_authorized.delete(api_sources_list_url + f'{source.id}/')
    assert response.status_code == 429
