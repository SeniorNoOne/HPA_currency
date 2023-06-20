from django.urls import reverse

from currency.models import Rate

rate_list_url = reverse('currency:rate-list')
rate_create_url = reverse('currency:rate-create')


# Create
def test_rate_create_status_code_on_get(client):
    response = client.get('/currency/rate/create/')
    assert response.status_code == 200


def test_rate_create_status_code_on_post_empty_submission(client):
    payload = {}
    response = client.post(rate_create_url, data=payload)
    assert response.status_code == 200


def test_rate_create_errors_on_post_empty_submission(client):
    payload = {}
    response = client.post(rate_create_url, data=payload)
    assert response.context_data['form']._errors == {
        'buy': ['This field is required.'],
        'sell': ['This field is required.'],
        'currency': ['This field is required.'],
        'source': ['This field is required.']
    }


def test_rate_create_status_code_on_post_invalid_buy_field(client, rate):
    payload = {
        'buy': 'WRONG',
        'sell': rate.sell,
        'currency': rate.currency,
        'source': rate.source.id
    }
    response = client.post(rate_create_url, data=payload)
    assert response.status_code == 200


def test_rate_create_errors_on_post_invalid_buy_field(client, rate):
    payload = {
        'buy': 'WRONG',
        'sell': rate.sell,
        'currency': rate.currency,
        'source': rate.source.id
    }
    response = client.post(rate_create_url, data=payload)
    assert response.context_data['form']._errors == {
        'buy': ['Enter a number.']
    }


def test_rate_create_status_code_on_post_invalid_sell_field(client, rate):
    payload = {
        'buy': rate.buy,
        'sell': 'WRONG',
        'currency': rate.currency,
        'source': rate.source.id
    }
    response = client.post(rate_create_url, data=payload)
    assert response.status_code == 200


def test_rate_create_invalid_sell_errors(client, source, rate, currency):
    payload = {
        'buy': rate.buy,
        'sell': 'WRONG',
        'currency': rate.currency,
        'source': rate.source.id
    }
    response = client.post(rate_create_url, data=payload)
    assert response.context_data['form']._errors == {
        'sell': ['Enter a number.']
    }


def test_rate_create_status_code_on_post_invalid_currency_field(client, rate, invalid_currency):
    payload = {
        'buy': rate.buy,
        'sell': rate.sell,
        'currency': invalid_currency,
        'source': rate.source.id
    }
    response = client.post(rate_create_url, data=payload)
    assert response.status_code == 200


def test_rate_create_errors_on_post_invalid_currency_field(client, rate, invalid_currency):
    payload = {
        'buy': rate.buy,
        'sell': rate.sell,
        'currency': invalid_currency,
        'source': rate.source.id
    }
    response = client.post(rate_create_url, data=payload)
    assert response.context_data['form']._errors == {
        'currency': [f'Select a valid choice. {invalid_currency} is '
                     'not one of the available choices.']
    }


def test_rate_create_status_code_on_post_invalid_source_field(client, rate):
    payload = {
        'buy': rate.buy,
        'sell': rate.sell,
        'currency': rate.currency,
        'source': 'WRONG'
    }
    response = client.post(rate_create_url, data=payload)
    assert response.status_code == 200


def test_rate_create_errors_on_post_invalid_source_field(client, rate):
    payload = {
        'buy': rate.buy,
        'sell': rate.sell,
        'currency': rate.currency,
        'source': 'WRONG'
    }
    response = client.post(rate_create_url, data=payload)
    assert response.context_data['form']._errors == {
        'source': ['Select a valid choice. That choice is not one of the available choices.']
    }


def test_rate_create_status_code_on_post_valid_submission(client, rate):
    payload = {
        'buy': rate.buy,
        'sell': rate.sell,
        'currency': rate.currency,
        'source': rate.source.id
    }
    response = client.post(rate_create_url, data=payload)
    assert response.status_code == 302


def test_rate_create_on_post_valid_submission(client, rate):
    payload = {
        'buy': rate.buy,
        'sell': rate.sell,
        'currency': rate.currency,
        'source': rate.source.id
    }
    initial_count = Rate.objects.count()
    response = client.post(rate_create_url, data=payload)
    checks = (
        response['location'] == rate_list_url,
        Rate.objects.count() == initial_count + 1
    )
    assert all(checks)


# List
def test_rate_list_status_code_on_get(client):
    response = client.get(rate_list_url)
    assert response.status_code == 200


def test_rate_list_on_get_with_empty_db(client):
    response = client.get(rate_list_url)
    assert not response.context_data['object_list'].exists()


def test_rate_list_on_get_with_one_record(client, rate):
    response = client.get(rate_list_url)
    assert response.context_data['object_list'].count() == 1


def test_rate_list_on_get_with_multiple_record(client, rates):
    response = client.get(rate_list_url)
    assert response.context_data['object_list'].count() == len(rates)


# Details
def test_rate_details_status_code_on_get_no_auth(client, rate):
    rate_details_url = reverse('currency:rate-details', args=(rate.id,))
    response = client.get(rate_details_url)
    assert response.status_code == 302


def test_rate_details_status_code_on_get_inactive_user(client, user, rate):
    client.force_login(user)
    rate_details_url = reverse('currency:rate-details', args=(rate.id,))
    response = client.get(rate_details_url)
    assert response.status_code == 302


def test_rate_details_status_code_on_get_active_user(client, active_user, rate):
    client.force_login(active_user)
    rate_details_url = reverse('currency:rate-details', args=(rate.id,))
    response = client.get(rate_details_url)
    assert response.status_code == 200


def test_rate_details_return_obj_on_get_active_user(client, active_user, rate):
    client.force_login(active_user)
    rate_details_url = reverse('currency:rate-details', args=(rate.id,))
    response = client.get(rate_details_url)
    assert response.context_data['object'] == rate


def test_rate_details_status_code_on_get_super_user(client, super_user, rate):
    client.force_login(super_user)
    rate_details_url = reverse('currency:rate-details', args=(rate.id,))
    response = client.get(rate_details_url)
    assert response.status_code == 200


def test_rate_details_return_obj_on_get_super_user(client, super_user, rate):
    client.force_login(super_user)
    rate_details_url = reverse('currency:rate-details', args=(rate.id,))
    response = client.get(rate_details_url)
    assert response.context_data['object'] == rate


# Update
def test_rate_update_status_code_on_get_no_auth(client, rate):
    rate_update_url = reverse('currency:rate-update', args=(rate.id,))
    response = client.get(rate_update_url)
    assert response.status_code == 302


def test_rate_update_status_code_on_get_inactive_user(client, user, rate):
    client.force_login(user)
    rate_update_url = reverse('currency:rate-update', args=(rate.id,))
    response = client.get(rate_update_url)
    assert response.status_code == 302


def test_rate_update_status_code_on_get_active_user(client, active_user, rate):
    client.force_login(active_user)
    rate_update_url = reverse('currency:rate-update', args=(rate.id,))
    response = client.get(rate_update_url)
    assert response.status_code == 403


def test_rate_update_status_code_on_get_super_user(client, super_user, rate):
    client.force_login(super_user)
    rate_update_url = reverse('currency:rate-update', args=(rate.id,))
    response = client.get(rate_update_url)
    assert response.status_code == 200


def test_rate_update_status_code_on_post_empty_submission(client, super_user, rate):
    payload = {}
    client.force_login(super_user)
    rate_update_url = reverse('currency:rate-update', args=(rate.id,))
    response = client.post(rate_update_url, data=payload)
    assert response.status_code == 200


def test_rate_update_errors_on_post_empty_submission(client, super_user, rate):
    payload = {}
    client.force_login(super_user)
    rate_update_url = reverse('currency:rate-update', args=(rate.id,))
    response = client.post(rate_update_url, data=payload)
    assert response.context_data['form']._errors == {
        'buy': ['This field is required.'],
        'sell': ['This field is required.'],
        'source': ['This field is required.'],
        'currency': ['This field is required.']
    }


def test_rate_update_status_code_on_post_invalid_buy_field(client, super_user, rate):
    payload = {
        'buy': 'WRONG',
        'sell': rate.sell,
        'currency': rate.currency,
        'source': rate.source.id
    }
    client.force_login(super_user)
    rate_update_url = reverse('currency:rate-update', args=(rate.id,))
    response = client.post(rate_update_url, data=payload)
    assert response.status_code == 200


def test_rate_update_errors_on_post_invalid_buy_field(client, super_user, rate):
    payload = {
        'buy': 'WRONG',
        'sell': rate.sell,
        'currency': rate.currency,
        'source': rate.source.id
    }
    client.force_login(super_user)
    rate_update_url = reverse('currency:rate-update', args=(rate.id,))
    response = client.post(rate_update_url, data=payload)
    assert response.context_data['form']._errors == {
        'buy': ['Enter a number.']
    }


def test_rate_update_status_code_on_post_invalid_sell_field(client, super_user, rate):
    payload = {
        'buy': rate.buy,
        'sell': 'WRONG',
        'currency': rate.currency,
        'source': rate.source.id
    }
    client.force_login(super_user)
    rate_update_url = reverse('currency:rate-update', args=(rate.id,))
    response = client.post(rate_update_url, data=payload)
    assert response.status_code == 200


def test_rate_update_errors_on_post_invalid_sell_field(client, super_user, rate):
    payload = {
        'buy': rate.buy,
        'sell': 'WRONG',
        'currency': rate.currency,
        'source': rate.source.id
    }
    client.force_login(super_user)
    rate_update_url = reverse('currency:rate-update', args=(rate.id,))
    response = client.post(rate_update_url, data=payload)
    assert response.context_data['form']._errors == {
        'sell': ['Enter a number.']
    }


def test_rate_update_status_code_on_post_invalid_currency_field(client, super_user, rate,
                                                                invalid_currency):
    payload = {
        'buy': rate.buy,
        'sell': rate.sell,
        'currency': invalid_currency,
        'source': rate.source.id
    }
    client.force_login(super_user)
    rate_update_url = reverse('currency:rate-update', args=(rate.id,))
    response = client.post(rate_update_url, data=payload)
    assert response.status_code == 200


def test_rate_update_errors_on_post_invalid_currency_field(client, super_user, rate,
                                                           invalid_currency):
    payload = {
        'buy': rate.buy,
        'sell': rate.sell,
        'currency': invalid_currency,
        'source': rate.source.id
    }
    client.force_login(super_user)
    rate_update_url = reverse('currency:rate-update', args=(rate.id,))
    response = client.post(rate_update_url, data=payload)
    assert response.context_data['form']._errors == {
        'currency': [f'Select a valid choice. {invalid_currency} '
                     'is not one of the available choices.']
    }


def test_rate_update_status_code_on_post_invalid_source_field(client, super_user, rate):
    payload = {
        'buy': rate.buy,
        'sell': rate.sell,
        'currency': rate.currency,
        'source': 'WRONG'
    }
    client.force_login(super_user)
    rate_update_url = reverse('currency:rate-update', args=(rate.id,))
    response = client.post(rate_update_url, data=payload)
    assert response.status_code == 200


def test_rate_update_errors_on_post_invalid_source_field(client, super_user, rate):
    payload = {
        'buy': rate.buy,
        'sell': rate.sell,
        'currency': rate.currency,
        'source': 'WRONG'
    }
    client.force_login(super_user)
    rate_update_url = reverse('currency:rate-update', args=(rate.id,))
    response = client.post(rate_update_url, data=payload)
    assert response.context_data['form']._errors == {
        'source': ['Select a valid choice. That choice is not one of the available choices.']
    }


def test_rate_update_on_post_valid_submission(client, super_user, rate):
    payload = {
        'buy': rate.buy,
        'sell': rate.sell,
        'currency': rate.currency,
        'source': rate.source.id
    }
    client.force_login(super_user)
    rate_update_url = reverse('currency:rate-update', args=(rate.id,))
    response = client.post(rate_update_url, data=payload)
    checks = (
        response.status_code == 302,
        response['location'] == rate_list_url
    )
    assert all(checks)


# Delete
def test_rate_delete_status_code_on_get_no_auth(client, rate):
    rate_delete_url = reverse('currency:rate-delete', args=(rate.id,))
    response = client.get(rate_delete_url)
    assert response.status_code == 302


def test_rate_delete_status_code_on_get_inactive_user(client, user, rate):
    client.force_login(user)
    rate_delete_url = reverse('currency:rate-delete', args=(rate.id,))
    response = client.get(rate_delete_url)
    assert response.status_code == 302


def test_rate_delete_status_code_on_get_active_user(client, active_user, rate):
    client.force_login(active_user)
    rate_delete_url = reverse('currency:rate-delete', args=(rate.id,))
    response = client.get(rate_delete_url)
    assert response.status_code == 403


def test_rate_delete_status_code_on_get_super_user(client, super_user, rate):
    client.force_login(super_user)
    rate_delete_url = reverse('currency:rate-delete', args=(rate.id,))
    response = client.get(rate_delete_url)
    assert response.status_code == 200


def test_rate_delete_on_post_super_user(client, super_user, rate):
    client.force_login(super_user)
    initial_count = Rate.objects.count()
    rate_delete_url = reverse('currency:rate-delete', args=(rate.id,))
    response = client.post(rate_delete_url)
    checks = (
        response.status_code == 302,
        response['location'] == rate_list_url,
        Rate.objects.count() == initial_count - 1
    )
    assert all(checks)
