from currency.models import Source


# Create
def test_source_create_status_200(client):
    response = client.get('/currency/source/create/')
    assert response.status_code == 200


def test_source_create_empty_form_status_200(client):
    response = client.post('/currency/source/create/')
    assert response.status_code == 200


def test_source_create_empty_form_errors(client):
    payload = {}
    response = client.post('/currency/source/create/', data=payload)
    assert response.context_data['form']._errors == {
        'url': ['This field is required.'],
        'name': ['This field is required.'],
        'code': ['This field is required.']
    }


def test_source_create_invalid_url_status_200(client, source):
    payload = {
        'url': '',
        'name': source.name,
        'code': source.code + 1
    }
    response = client.post('/currency/source/create/', data=payload)
    assert response.status_code == 200


def test_source_create_invalid_url_errors(client, source, rate, currency):
    payload = {
        'url': '',
        'name': source.name,
        'code': source.code + 1
    }
    response = client.post('/currency/source/create/', data=payload)
    assert response.context_data['form']._errors == {'url': ['This field is required.']}


def test_source_create_invalid_name_status_200(client, source):
    payload = {
        'url': source.url,
        'name': '',
        'code': source.code + 1
    }
    response = client.post('/currency/source/create/', data=payload)
    assert response.status_code == 200


def test_source_create_invalid_name_errors(client, source):
    payload = {
        'url': source.url,
        'name': '',
        'code': source.code + 1
    }
    response = client.post('/currency/source/create/', data=payload)
    assert response.context_data['form']._errors == {'name': ['This field is required.']}


def test_source_create_duplicate_code_status_200(client, source):
    payload = {
        'url': source.url,
        'name': source.name,
        'code': source.code
    }
    response = client.post('/currency/source/create/', data=payload)
    assert response.status_code == 200


def test_source_create_duplicate_code_errors(client, source):
    payload = {
        'url': source.url,
        'name': source.name,
        'code': source.code
    }
    response = client.post('/currency/source/create/', data=payload)
    assert response.context_data['form']._errors == \
           {'code': ['Source with this Code already exists.']}


def test_source_create_valid_form_status_302(client, source):
    payload = {
        'url': source.url,
        'name': source.name,
        'code': source.code + 1
    }
    response = client.post('/currency/source/create/', data=payload)
    assert response.status_code == 302


def test_source_create_valid_form_data(client, source):
    initial_count = Source.objects.count()
    payload = {
        'url': source.url,
        'name': source.name,
        'code': source.code + 1
    }
    response = client.post('/currency/source/create/', data=payload)
    checks = (
        response['location'] == '/currency/source/list/',
        Source.objects.count() == initial_count + 1
    )
    assert all(checks)


# List
def test_source_list_status_200(client):
    response = client.get('/currency/source/list/')
    assert response.status_code == 200


def test_source_list_empty_db(client):
    response = client.get('/currency/source/list/')
    assert not response.context_data['object_list'].exists()


def test_source_list_single_entity(client, source):
    response = client.get('/currency/source/list/')
    assert response.context_data['object_list'].count() == 1


def test_source_list_multiple_entities(client, sources):
    response = client.get('/currency/source/list/')
    assert response.context_data['object_list'].count() == len(sources)


# Details
# noinspection DuplicatedCode
def test_source_details_no_auth_status_200(client, source):
    response = client.get(f'/currency/source/details/{source.id}/')
    assert response.status_code == 200


def test_source_details_no_auth_model_obj(client, source):
    response = client.get(f'/currency/source/details/{source.id}/')
    assert response.context_data['object'] == source


def test_source_details_inactive_user_status_200(client, user, source):
    client.force_login(user)
    response = client.get(f'/currency/source/details/{source.id}/')
    assert response.status_code == 200


def test_source_details_inactive_user_model_obj(client, user, source):
    client.force_login(user)
    response = client.get(f'/currency/source/details/{source.id}/')
    assert response.context_data['object'] == source


def test_source_details_active_user_status_200(client, active_user, source):
    client.force_login(active_user)
    response = client.get(f'/currency/source/details/{source.id}/')
    assert response.status_code == 200


def test_source_details_active_user_model_obj(client, active_user, source):
    client.force_login(active_user)
    response = client.get(f'/currency/source/details/{source.id}/')
    assert response.context_data['object'] == source


def test_source_details_super_user_status_200(client, super_user, source):
    client.force_login(super_user)
    response = client.get(f'/currency/source/details/{source.id}/')
    assert response.status_code == 200


def test_source_details_super_user_model_obj(client, super_user, source):
    client.force_login(super_user)
    response = client.get(f'/currency/source/details/{source.id}/')
    assert response.context_data['object'] == source


# Update
# noinspection DuplicatedCode
def test_source_update_no_auth_status_200(client, source):
    response = client.get(f'/currency/source/update/{source.id}/')
    assert response.status_code == 200


def test_source_update_no_auth_model_obj(client, source):
    response = client.get(f'/currency/source/update/{source.id}/')
    assert response.context_data['object'] == source


def test_source_update_inactive_user_status_200(client, user, source):
    client.force_login(user)
    response = client.get(f'/currency/source/update/{source.id}/')
    assert response.status_code == 200


def test_source_update_inactive_user_model_obj(client, user, source):
    client.force_login(user)
    response = client.get(f'/currency/source/update/{source.id}/')
    assert response.context_data['object'] == source


def test_source_update_active_user_status_200(client, active_user, source):
    client.force_login(active_user)
    response = client.get(f'/currency/source/update/{source.id}/')
    assert response.status_code == 200


def test_source_update_active_user_model_obj(client, active_user, source):
    client.force_login(active_user)
    response = client.get(f'/currency/source/update/{source.id}/')
    assert response.context_data['object'] == source


def test_source_update_super_user_status_200(client, super_user, source):
    client.force_login(super_user)
    response = client.get(f'/currency/source/update/{source.id}/')
    assert response.status_code == 200


def test_source_update_super_user_model_obj(client, super_user, source):
    client.force_login(super_user)
    response = client.get(f'/currency/source/update/{source.id}/')
    assert response.context_data['object'] == source


def test_source_update_empty_form_status_200(client, source):
    payload = {}
    response = client.post(f'/currency/source/update/{source.id}/', data=payload)
    assert response.status_code == 200


def test_source_update_empty_form_errors(client, source):
    payload = {}
    response = client.post(f'/currency/source/update/{source.id}/', data=payload)
    assert response.context_data['form']._errors == {
        'url': ['This field is required.'],
        'name': ['This field is required.'],
        'code': ['This field is required.']
    }


def test_source_update_invalid_url_status_200(client, source):
    payload = {
        'url': '',
        'name': source.name,
        'code': source.name
    }
    response = client.post(f'/currency/source/update/{source.id}/', data=payload)
    assert response.status_code == 200


def test_source_update_invalid_url_errors(client, source):
    payload = {
        'url': '',
        'name': source.name,
        'code': source.code
    }
    response = client.post(f'/currency/source/update/{source.id}/', data=payload)
    assert response.context_data['form']._errors == {'url': ['This field is required.']}


def test_source_update_invalid_name_status_200(client, source):
    payload = {
        'url': source.url,
        'name': '',
        'code': source.code
    }
    response = client.post(f'/currency/source/update/{source.id}/', data=payload)
    assert response.status_code == 200


def test_source_update_invalid_name_errors(client, source):
    payload = {
        'url': source.url,
        'name': '',
        'code': source.code
    }
    response = client.post(f'/currency/source/update/{source.id}/', data=payload)
    assert response.context_data['form']._errors == {'name': ['This field is required.']}


def test_source_update_invalid_code_status_200(client, source):
    payload = {
        'url': source.url,
        'name': source.name,
        'code': 'WRONG'
    }
    response = client.post(f'/currency/source/update/{source.id}/', data=payload)
    assert response.status_code == 200


def test_source_update_invalid_code_errors(client, source):
    payload = {
        'url': source.url,
        'name': source.name,
        'code': 'WRONG'
    }
    response = client.post(f'/currency/source/update/{source.id}/', data=payload)
    assert response.context_data['form']._errors == {'code': ['Enter a whole number.']}


def test_source_update_valid_form_status_302(client, super_user, source):
    payload = {
        'url': source.url,
        'name': source.name,
        'code': source.code + 1
    }
    response = client.post(f'/currency/source/update/{source.id}/', data=payload)
    assert response.status_code == 302


def test_source_update_valid_form_data(client, super_user, source, rate, currency):
    payload = {
        'url': source.url,
        'name': source.name,
        'code': source.code + 1
    }
    response = client.post(f'/currency/source/update/{source.id}/', data=payload)
    assert response['location'] == '/currency/source/list/'


# Delete
# noinspection DuplicatedCode
def test_source_delete_no_auth_status_200(client, source):
    response = client.get(f'/currency/source/delete/{source.id}/')
    assert response.status_code == 200


def test_source_delete_no_auth_data(client, source):
    initial_count = Source.objects.count()
    response = client.post(f'/currency/source/delete/{source.id}/')
    checks = (
        response['location'] == '/currency/source/list/',
        Source.objects.count() == initial_count - 1
    )
    assert all(checks)


# noinspection DuplicatedCode
def test_source_delete_inactive_user_status_200(client, user, source):
    client.force_login(user)
    response = client.get(f'/currency/source/delete/{source.id}/')
    assert response.status_code == 200


def test_source_delete_inactive_user_data(client, user, source):
    initial_count = Source.objects.count()
    client.force_login(user)
    response = client.post(f'/currency/source/delete/{source.id}/')
    checks = (
        response['location'] == '/currency/source/list/',
        Source.objects.count() == initial_count - 1
    )
    assert all(checks)


# noinspection DuplicatedCode
def test_source_delete_active_user_status_200(client, active_user, source):
    client.force_login(active_user)
    response = client.get(f'/currency/source/delete/{source.id}/')
    assert response.status_code == 200


def test_source_delete_active_user_data(client, active_user, source):
    initial_count = Source.objects.count()
    client.force_login(active_user)
    response = client.post(f'/currency/source/delete/{source.id}/')
    checks = (
        response['location'] == '/currency/source/list/',
        Source.objects.count() == initial_count - 1
    )
    assert all(checks)


# noinspection DuplicatedCode
def test_source_delete_super_user_status_200(client, super_user, source):
    client.force_login(super_user)
    response = client.get(f'/currency/source/delete/{source.id}/')
    assert response.status_code == 200


def test_source_delete_super_user_data(client, super_user, source):
    initial_count = Source.objects.count()
    client.force_login(super_user)
    response = client.post(f'/currency/source/delete/{source.id}/')
    checks = (
        response['location'] == '/currency/source/list/',
        Source.objects.count() == initial_count - 1
    )
    assert all(checks)
