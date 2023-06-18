from django.urls import reverse

api_auth_url = reverse('api-account:token_obtain_pair')


# GET request tests
def test_api_auth_tokens_status_code_on_get_request(api_client):
    response = api_client.get(api_auth_url)
    assert response.status_code == 405


def test_api_auth_tokens_errors_on_get_request(api_client):
    response = api_client.get(api_auth_url)
    data = response.json()
    assert data == {
        'detail': 'Method \"GET\" not allowed.'
    }


# POST request tests
def test_api_auth_tokens_status_code_on_empty_payload(api_client):
    response = api_client.post(api_auth_url)
    assert response.status_code == 400


def test_api_auth_tokens_errors_on_empty_payload(api_client):
    response = api_client.post(api_auth_url)
    data = response.json()
    assert data == {
        'email': ['This field is required.'],
        'password': ['This field is required.']
    }


def test_api_auth_endpoint_status_code_on_empty_email(api_client, active_user_with_hashed_password):
    payload = {
        'email': '',
        'password': active_user_with_hashed_password.raw_password
    }
    response = api_client.post(api_auth_url, data=payload)
    assert response.status_code == 400


def test_api_auth_endpoint_errors_on_empty_email(api_client, active_user_with_hashed_password):
    payload = {
        'email': '',
        'password': active_user_with_hashed_password.raw_password
    }
    response = api_client.post(api_auth_url, data=payload)
    data = response.json()
    assert data == {
        'email': ['This field may not be blank.']
    }


def test_api_auth_endpoint_status_code_on_empty_password(api_client,
                                                         active_user_with_hashed_password):
    payload = {
        'email': active_user_with_hashed_password.email,
        'password': ''
    }
    response = api_client.post(api_auth_url, data=payload)
    assert response.status_code == 400


def test_api_auth_endpoint_errors_on_empty_password(api_client, active_user_with_hashed_password):
    payload = {
        'email': active_user_with_hashed_password.email,
        'password': ''
    }
    response = api_client.post(api_auth_url, data=payload)
    data = response.json()
    assert data == {
        'password': ['This field may not be blank.']
    }


def test_api_auth_endpoint_on_valid_submission(api_client, active_user_with_hashed_password):
    payload = {
        'email': active_user_with_hashed_password.email,
        'password': active_user_with_hashed_password.raw_password
    }
    response = api_client.post(api_auth_url, data=payload)
    data = response.json()
    checks = (
        response.status_code == 200,
        'refresh' in data,
        'access' in data
    )
    assert all(checks)


# PUT request tests
def test_api_auth_tokens_status_code_on_put_request(api_client):
    response = api_client.put(api_auth_url)
    assert response.status_code == 405


def test_api_auth_tokens_errors_on_put_request(api_client):
    response = api_client.put(api_auth_url)
    data = response.json()
    assert data == {
        'detail': 'Method \"PUT\" not allowed.'
    }


# PATCH request tests
def test_api_auth_tokens_status_code_on_patch_request(api_client):
    response = api_client.patch(api_auth_url)
    assert response.status_code == 405


def test_api_auth_tokens_errors_on_patch_request(api_client):
    response = api_client.patch(api_auth_url)
    data = response.json()
    assert data == {
        'detail': 'Method \"PATCH\" not allowed.'
    }


# DELETE request tests
def test_api_auth_tokens_status_code_on_delete_request(api_client):
    response = api_client.delete(api_auth_url)
    assert response.status_code == 405


def test_api_auth_tokens_errors_on_delete_request(api_client):
    response = api_client.delete(api_auth_url)
    data = response.json()
    assert data == {
        'detail': 'Method \"DELETE\" not allowed.'
    }


# HEAD request tests
def test_api_auth_tokens_status_code_on_head_request(api_client):
    response = api_client.head(api_auth_url)
    assert response.status_code == 405


# OPTIONS request tests
def test_api_auth_tokens_status_code_on_options_request(api_client):
    response = api_client.options(api_auth_url)
    assert response.status_code == 200
