from currency.models import Rate


# Create
def test_rate_create_status_200(client):
    response = client.get('/currency/rate/create/')
    assert response.status_code == 200


def test_rate_create_empty_form_status_200(client):
    response = client.post('/currency/rate/create/')
    assert response.status_code == 200


def test_rate_create_empty_form_errors(client):
    payload = {}
    response = client.post('/currency/rate/create/', data=payload)
    assert response.context_data['form']._errors == {
        'buy': ['This field is required.'],
        'sell': ['This field is required.'],
        'currency': ['This field is required.'],
        'source': ['This field is required.']
    }


def test_rate_create_invalid_buy_status_200(client, source, rate, currency):
    payload = {
        'buy': 'WRONG',
        'sell': rate.sell,
        'currency': currency,
        'source': source.id
    }
    response = client.post('/currency/rate/create/', data=payload)
    assert response.status_code == 200


def test_rate_create_invalid_buy_errors(client, source, rate, currency):
    payload = {
        'buy': 'WRONG',
        'sell': rate.sell,
        'currency': currency,
        'source': source.id
    }
    response = client.post('/currency/rate/create/', data=payload)
    assert response.context_data['form']._errors == {'buy': ['Enter a number.']}


def test_rate_create_invalid_sell_status_200(client, source, rate, currency):
    payload = {
        'buy': rate.buy,
        'sell': 'WRONG',
        'currency': currency,
        'source': source.id
    }
    response = client.post('/currency/rate/create/', data=payload)
    assert response.status_code == 200


def test_rate_create_invalid_sell_errors(client, source, rate, currency):
    payload = {
        'buy': rate.buy,
        'sell': 'WRONG',
        'currency': currency,
        'source': source.id
    }
    response = client.post('/currency/rate/create/', data=payload)
    assert response.context_data['form']._errors == {'sell': ['Enter a number.']}


def test_rate_create_invalid_currency_status_200(client, source, rate, invalid_currency):
    payload = {
        'buy': rate.buy,
        'sell': rate.sell,
        'currency': invalid_currency,
        'source': source.id
    }
    response = client.post('/currency/rate/create/', data=payload)
    assert response.status_code == 200


def test_rate_create_invalid_currency_errors(client, source, rate, invalid_currency):
    payload = {
        'buy': rate.buy,
        'sell': rate.sell,
        'currency': invalid_currency,
        'source': source.id
    }
    response = client.post('/currency/rate/create/', data=payload)
    assert response.context_data['form']._errors == \
           {'currency': [f'Select a valid choice. {invalid_currency} is not '
                         f'one of the available choices.']}


def test_rate_create_invalid_source_status_200(client, source, rate, currency):
    payload = {
        'buy': rate.buy,
        'sell': rate.sell,
        'currency': currency,
        'source': 'WRONG'
    }
    response = client.post('/currency/rate/create/', data=payload)
    assert response.status_code == 200


def test_rate_create_invalid_source_errors(client, source, rate, currency):
    payload = {
        'buy': rate.buy,
        'sell': rate.sell,
        'currency': currency,
        'source': 'WRONG'
    }
    response = client.post('/currency/rate/create/', data=payload)
    assert response.context_data['form']._errors == \
           {'source': ['Select a valid choice. That choice is not one of the available choices.']}


def test_rate_create_valid_form_status_302(client, source, rate, currency):
    payload = {
        'buy': rate.buy,
        'sell': rate.sell,
        'currency': currency,
        'source': source.id
    }
    response = client.post('/currency/rate/create/', data=payload)
    assert response.status_code == 302


def test_rate_create_valid_form_data(client, source, rate, currency):
    initial_count = Rate.objects.count()
    payload = {
        'buy': rate.buy,
        'sell': rate.sell,
        'currency': currency,
        'source': source.id
    }
    response = client.post('/currency/rate/create/', data=payload)
    checks = (
        response['location'] == '/currency/rate/list/',
        Rate.objects.count() == initial_count + 1
    )
    assert all(checks)


# List
def test_rate_list_status_200(client):
    response = client.get('/currency/rate/list/')
    assert response.status_code == 200


def test_rate_list_empty_db(client):
    response = client.get('/currency/rate/list/')
    assert not response.context_data['object_list'].exists()


def test_rate_list_single_entity(client, rate):
    response = client.get('/currency/rate/list/')
    assert response.context_data['object_list'].count() == 1


def test_rate_list_multiple_entities(client, rates):
    response = client.get('/currency/rate/list/')
    assert response.context_data['object_list'].count() == len(rates)


# Details
def test_rate_details_no_auth_status_302(client, rate):
    response = client.get(f'/currency/rate/details/{rate.id}/')
    assert response.status_code == 302


def test_rate_details_inactive_user_status_302(client, user, rate):
    client.force_login(user)
    response = client.get(f'/currency/rate/details/{rate.id}/')
    assert response.status_code == 302


# noinspection DuplicatedCode
def test_rate_details_active_user_status_200(client, active_user, rate):
    client.force_login(active_user)
    response = client.get(f'/currency/rate/details/{rate.id}/')
    assert response.status_code == 200


def test_rate_details_active_user_model_obj(client, active_user, rate):
    client.force_login(active_user)
    response = client.get(f'/currency/rate/details/{rate.id}/')
    assert response.context_data['object'] == rate


def test_rate_details_super_user_status_200(client, super_user, rate):
    client.force_login(super_user)
    response = client.get(f'/currency/rate/details/{rate.id}/')
    assert response.status_code == 200


def test_rate_details_super_user_model_obj(client, super_user, rate):
    client.force_login(super_user)
    response = client.get(f'/currency/rate/details/{rate.id}/')
    assert response.context_data['object'] == rate


# Update
# noinspection DuplicatedCode
def test_rate_update_no_auth_status_302(client, rate):
    response = client.get(f'/currency/rate/update/{rate.id}/')
    assert response.status_code == 302


def test_rate_update_inactive_user_status_302(client, user, rate):
    client.force_login(user)
    response = client.get(f'/currency/rate/update/{rate.id}/')
    assert response.status_code == 302


def test_rate_update_active_user_status_403(client, active_user, rate):
    client.force_login(active_user)
    response = client.get(f'/currency/rate/update/{rate.id}/')
    assert response.status_code == 403


def test_rate_update_super_user_status_200(client, super_user, rate):
    client.force_login(super_user)
    response = client.get(f'/currency/rate/update/{rate.id}/')
    assert response.status_code == 200


def test_rate_update_super_user_empty_form_status_200(client, super_user, rate):
    payload = {}
    client.force_login(super_user)
    response = client.post(f'/currency/rate/update/{rate.id}/', data=payload)
    assert response.status_code == 200


def test_rate_update_super_user_empty_form_errors(client, super_user, rate):
    payload = {}
    client.force_login(super_user)
    response = client.post(f'/currency/rate/update/{rate.id}/', data=payload)
    assert response.context_data['form']._errors == {
        'buy': ['This field is required.'],
        'sell': ['This field is required.'],
        'source': ['This field is required.'],
        'currency': ['This field is required.']
    }


def test_rate_update_super_user_invalid_buy_errors(client, super_user, source, rate, currency):
    payload = {
        'buy': 'WRONG',
        'sell': rate.sell,
        'currency': currency,
        'source': source.id
    }
    client.force_login(super_user)
    response = client.post(f'/currency/rate/update/{rate.id}/', data=payload)
    assert response.context_data['form']._errors == {'buy': ['Enter a number.']}


def test_rate_update_super_user_invalid_sell_errors(client, super_user, source, rate, currency):
    payload = {
        'buy': rate.buy,
        'sell': 'WRONG',
        'currency': currency,
        'source': source.id
    }
    client.force_login(super_user)
    response = client.post(f'/currency/rate/update/{rate.id}/', data=payload)
    assert response.context_data['form']._errors == {'sell': ['Enter a number.']}


def test_rate_update_super_user_invalid_currency_errors(client, super_user, source, rate,
                                                        invalid_currency):
    payload = {
        'buy': rate.buy,
        'sell': rate.sell,
        'currency': invalid_currency,
        'source': source.id
    }
    client.force_login(super_user)
    response = client.post(f'/currency/rate/update/{rate.id}/', data=payload)
    assert response.context_data['form']._errors == {
        'currency': [f'Select a valid choice. {invalid_currency} '
                     f'is not one of the available choices.']
    }


def test_rate_update_super_user_invalid_source_errors(client, super_user, source, rate, currency):
    payload = {
        'buy': rate.buy,
        'sell': rate.sell,
        'currency': currency,
        'source': 'WRONG'
    }
    client.force_login(super_user)
    response = client.post(f'/currency/rate/update/{rate.id}/', data=payload)
    assert response.context_data['form']._errors == {
        'source': ['Select a valid choice. That choice is not one of the available choices.']
    }


def test_rate_update_super_user_valid_form_status_302(client, super_user, source, rate, currency):
    payload = {
        'buy': rate.buy,
        'sell': rate.sell,
        'currency': currency,
        'source': source.id
    }
    client.force_login(super_user)
    response = client.post(f'/currency/rate/update/{rate.id}/', data=payload)
    assert response.status_code == 302


def test_rate_update_super_user_valid_form_data(client, super_user, source, rate, currency):
    payload = {
        'buy': rate.buy,
        'sell': rate.sell,
        'currency': currency,
        'source': source.id
    }
    client.force_login(super_user)
    response = client.post(f'/currency/rate/update/{rate.id}/', data=payload)
    assert response['location'] == '/currency/rate/list/'


# Delete
# noinspection DuplicatedCode
def test_rate_delete_no_auth_status_302(client, rate):
    response = client.get(f'/currency/rate/delete/{rate.id}/')
    assert response.status_code == 302


def test_rate_delete_inactive_user_status_403(client, user, rate):
    client.force_login(user)
    response = client.get(f'/currency/rate/delete/{rate.id}/')
    assert response.status_code == 302


def test_rate_delete_active_user_status_403(client, active_user, rate):
    client.force_login(active_user)
    response = client.get(f'/currency/rate/delete/{rate.id}/')
    assert response.status_code == 403


def test_rate_delete_super_user_status_200(client, super_user, rate):
    client.force_login(super_user)
    response = client.get(f'/currency/rate/delete/{rate.id}/')
    assert response.status_code == 200


def test_rate_delete_super_user_status_302(client, super_user, rate):
    client.force_login(super_user)
    response = client.post(f'/currency/rate/delete/{rate.id}/')
    assert response.status_code == 302


def test_rate_delete_super_user_data(client, super_user, rate):
    initial_count = Rate.objects.count()
    client.force_login(super_user)
    response = client.post(f'/currency/rate/delete/{rate.id}/')
    checks = (
        response['location'] == '/currency/rate/list/',
        Rate.objects.count() == initial_count - 1
    )
    assert all(checks)
