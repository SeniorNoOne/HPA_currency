# LIST GET
def test_get_source_list_status_200(api_client):
    response = api_client.get('/api/currency/sources/')
    assert response.status_code == 200


def test_get_source_list_empty_db(api_client):
    response = api_client.get('/api/currency/sources/')
    assert len(response.json()['results']) == 0


def test_get_source_list_single_entity(api_client, source):
    response = api_client.get('/api/currency/sources/')
    assert len(response.json()['results']) == 1


def test_get_source_list_multiple_entities(api_client, sources):
    response = api_client.get('/api/currency/sources/')
    assert len(response.json()['results']) == len(sources)


def test_get_source_list_pagination(api_client, sources):
    response = api_client.get('/api/currency/sources/')
    json = response.json()
    checks = {
        'count' in json,
        'next' in json,
        'previous' in json
    }
    assert all(checks)


# LIST POST
def test_post_source_list_empty_payload_status_405(api_client, user):
    payload = {}
    api_client.force_login(user)
    response = api_client.post('/api/currency/sources/', data=payload)
    assert response.status_code == 405


# DETAILS GET
def test_get_source_details_status_200(api_client, source):
    response = api_client.get(f'/api/currency/sources/{source.id}/')
    assert response.status_code == 200


def test_get_source_details_status_404(api_client):
    response = api_client.get(f'/api/currency/sources/{-1}/')
    assert response.status_code == 404


def test_get_source_details_data(api_client, source):
    response = api_client.get(f'/api/currency/sources/{source.id}/')
    assert response.json() == {
        'url': source.url,
        'code': source.code,
        'city': source.city,
        'phone': source.phone
    }


# DETAILS PUT
def test_put_source_details_same_source_status_405(api_client, source):
    payload = {
        'id': source.id,
        'url': source.url,
        'code': source.code,
    }
    response = api_client.put(f'/api/currency/sources/{source.id}/', data=payload)
    assert response.status_code == 405


def test_put_source_details_same_source_data(api_client, source):
    payload = {
        'id': source.id,
        'url': source.url,
        'code': source.code,
    }
    response = api_client.put(f'/api/currency/sources/{source.id}/', data=payload)
    assert response.json() == {'detail': 'Method \"PUT\" not allowed.'}


# DETAILS DELETE
def test_delete_source_details_status_405(api_client, source):
    response = api_client.delete(f'/api/currency/sources/{source.id}/')
    assert response.status_code == 405


def test_delete_source_details_same_source_data(api_client, source):
    payload = {
        'id': source.id,
        'url': source.url,
        'code': source.code,
    }
    response = api_client.delete(f'/api/currency/sources/{source.id}/', data=payload)
    assert response.json() == {'detail': 'Method \"DELETE\" not allowed.'}


# Throttling test
def test_get_source_list_status_429(api_client, source):
    response = api_client.get('/api/currency/sources/')
    for _ in range(100):
        response = api_client.get('/api/currency/sources/')
    assert response.status_code == 429


def test_get_source_details_status_429(api_client, source):
    response = api_client.get(f'/api/currency/sources/{source.id}/')
    for _ in range(100):
        response = api_client.get(f'/api/currency/sources/{source.id}/')
    assert response.status_code == 429


def test_put_source_status_429(api_client, source):
    payload = {}
    response = api_client.put(f'/api/currency/sources/{source.id}/', data=payload)
    for _ in range(100):
        response = api_client.put(f'/api/currency/sources/{source.id}/', data=payload)
    assert response.status_code == 429


def test_delete_source_status_429(api_client, source):
    response = api_client.delete(f'/api/currency/sources/{source.id}/')
    for _ in range(100):
        response = api_client.delete(f'/api/currency/sources/{source.id}/')
    assert response.status_code == 429
