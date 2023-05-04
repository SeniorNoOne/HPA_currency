from currency.models import Source


# Create
def test_source_create_status_200(client):
    response = client.post('/currency/source/create/')
    assert response.status_code == 200


def test_source_create_empty_form_status_200(client):
    response = client.post('/currency/source/create/')
    assert response.status_code == 200


def test_source_create_empty_form_errors(client):
    payload = {}
    response = client.post('/currency/source/create/', data=payload)
    assert response.context_data['form']._errors == {
        'url': ['This field is required.'],
        'code': ['This field is required.'],
        'name': ['This field is required.'],
    }


def test_source_create_invalid_url_status_200(client, source, currency):
    payload = {
        'url': '',
        'code': 100,
        'name': 'Source name',
    }
    response = client.post('/currency/source/create/', data=payload)
    assert response.status_code == 200


def test_source_create_invalid_url_type(client, source, currency):
    payload = {
        'url': '',
        'code': 100,
        'name': 'Source name',
    }
    response = client.post('/currency/source/create/', data=payload)
    assert response.context_data['form']._errors == {'url': ['This field is required.']}


def test_source_create_invalid_code_status_200(client, source, currency):
    payload = {
        'url': 'some/url',
        'code': 'WRONG',
        'name': 'Source name',
    }
    response = client.post('/currency/source/create/', data=payload)
    assert response.status_code == 200


def test_source_create_invalid_code_type(client, source, currency):
    payload = {
        'url': 'some/url',
        'code': 'WRONG',
        'name': 'Source name',
    }
    response = client.post('/currency/source/create/', data=payload)
    assert response.context_data['form']._errors == {'code': ['Enter a whole number.']}


def test_source_create_invalid_name_status_200(client, source, currency):
    payload = {
        'url': 'some/url',
        'code': 100,
        'name': '',
    }
    response = client.post('/currency/source/create/', data=payload)
    assert response.status_code == 200


def test_source_create_invalid_name_type(client, source, currency):
    payload = {
        'url': 'some/url',
        'code': 100,
        'name': '',
    }
    response = client.post('/currency/source/create/', data=payload)
    assert response.context_data['form']._errors == {'name': ['This field is required.']}


def test_source_create_valid_form_status_302(client, source, currency):
    payload = {
        'url': 'some/url',
        'code': 100,
        'name': 'Source name',
    }
    response = client.post('/currency/source/create/', data=payload)
    assert response.status_code == 302


def test_source_create_valid_form(client, source, currency):
    initial_count = Source.objects.count()
    payload = {
        'url': 'some/url',
        'code': 100,
        'name': 'Source name',
    }
    response = client.post('/currency/source/create/', data=payload)
    checks = (
        response['location'] == '/currency/source/list/',
        Source.objects.count() == initial_count + 1
    )
    assert all(checks)
