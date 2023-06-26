from django.urls import reverse

api_auth_endpoint = reverse('api-account:token_obtain_pair')
api_refresh_endpoint = reverse('api-account:token_refresh')


# GET request tests
def test_api_auth_endpoint_status_code_on_get(api_client):
    response = api_client.get(api_auth_endpoint)
    assert response.status_code == 405


def test_api_auth_endpoint_errors_on_get(api_client):
    response = api_client.get(api_auth_endpoint)
    assert response.json() == {
        'detail': 'Method \"GET\" not allowed.'
    }


def test_api_refresh_endpoint_status_code_on_get(api_client):
    response = api_client.get(api_refresh_endpoint)
    assert response.status_code == 405


def test_api_refresh_endpoint_errors_on_get(api_client):
    response = api_client.get(api_refresh_endpoint)
    assert response.json() == {
        'detail': 'Method \"GET\" not allowed.'
    }


# POST request tests
def test_api_auth_endpoint_status_code_on_post_empty_submission(api_client):
    payload = {}
    response = api_client.post(api_auth_endpoint, data=payload)
    assert response.status_code == 400


def test_api_auth_endpoint_errors_on_post_empty_submission(api_client):
    payload = {}
    response = api_client.post(api_auth_endpoint, data=payload)
    assert response.json() == {
        'email': ['This field is required.'],
        'password': ['This field is required.']
    }


def test_api_auth_endpoint_status_code_on_post_empty_email(api_client,
                                                           active_user_hashed_password):
    payload = {
        'email': '',
        'password': active_user_hashed_password.raw_password
    }
    response = api_client.post(api_auth_endpoint, data=payload)
    assert response.status_code == 400


def test_api_auth_endpoint_errors_on_empty_email(api_client, active_user_hashed_password):
    payload = {
        'email': '',
        'password': active_user_hashed_password.raw_password
    }
    response = api_client.post(api_auth_endpoint, data=payload)
    assert response.json() == {
        'email': ['This field may not be blank.']
    }


def test_api_auth_endpoint_status_code_on_post_empty_password(api_client,
                                                              active_user_hashed_password):
    payload = {
        'email': active_user_hashed_password.email,
        'password': ''
    }
    response = api_client.post(api_auth_endpoint, data=payload)
    assert response.status_code == 400


def test_api_auth_endpoint_errors_on_post_empty_password(api_client,
                                                         active_user_hashed_password):
    payload = {
        'email': active_user_hashed_password.email,
        'password': ''
    }
    response = api_client.post(api_auth_endpoint, data=payload)
    assert response.json() == {
        'password': ['This field may not be blank.']
    }


def test_api_auth_endpoint_status_code_on_post_valid_submission(api_client,
                                                                active_user_hashed_password):
    payload = {
        'email': active_user_hashed_password.email,
        'password': active_user_hashed_password.raw_password
    }
    response = api_client.post(api_auth_endpoint, data=payload)
    assert response.status_code == 200


def test_api_auth_endpoint_errors_on_post_valid_submission(api_client,
                                                           active_user_hashed_password):
    payload = {
        'email': active_user_hashed_password.email,
        'password': active_user_hashed_password.raw_password
    }
    response = api_client.post(api_auth_endpoint, data=payload)
    data = response.json()
    checks = (
        'refresh' in data,
        'access' in data
    )
    assert all(checks)


def test_api_refresh_endpoint_status_code_on_post_empty_submission(api_client):
    payload = {}
    response = api_client.post(api_refresh_endpoint, data=payload)
    assert response.status_code == 400


def test_api_refresh_endpoint_errors_on_post_empty_submission(api_client):
    payload = {}
    response = api_client.post(api_refresh_endpoint, data=payload)
    assert response.json() == {
        'refresh': [
            'This field is required.'
        ]
    }


def test_api_refresh_endpoint_status_code_on_post_empty_refresh(api_client):
    payload = {
        'refresh': ''
    }
    response = api_client.post(api_refresh_endpoint, data=payload)
    assert response.status_code == 400


def test_api_refresh_endpoint_errors_on_post_empty_refresh(api_client):
    payload = {
        'refresh': ''
    }
    response = api_client.post(api_refresh_endpoint, data=payload)
    assert response.json() == {
        'refresh': [
            'This field may not be blank.'
        ]
    }


def test_api_refresh_endpoint_status_code_on_post_invalid_refresh(api_client,
                                                                  active_user_hashed_password):
    payload = {
        'refresh': '_'
    }
    response = api_client.post(api_refresh_endpoint, data=payload)
    assert response.status_code == 401


def test_api_refresh_endpoint_errors_on_post_invalid_refresh(api_client,
                                                             active_user_hashed_password):
    payload = {
        'refresh': '_'
    }
    response = api_client.post(api_refresh_endpoint, data=payload)
    assert response.json() == {
        'detail': 'Token is invalid or expired',
        'code': 'token_not_valid'
    }


def test_api_refresh_endpoint_status_code_on_post_valid_submission(api_client,
                                                                   active_user_hashed_password):
    payload = {
        'email': active_user_hashed_password.email,
        'password': active_user_hashed_password.raw_password
    }
    response = api_client.post(api_auth_endpoint, data=payload)
    refresh_token = response.json()['refresh']
    response = api_client.post(api_refresh_endpoint, data={'refresh': refresh_token})
    assert response.status_code == 200


def test_api_refresh_endpoint_errors_on_post_valid_submission(api_client,
                                                              active_user_hashed_password):
    payload = {
        'email': active_user_hashed_password.email,
        'password': active_user_hashed_password.raw_password
    }
    response = api_client.post(api_auth_endpoint, data=payload)
    refresh_token = response.json()['refresh']
    response = api_client.post(api_refresh_endpoint, data={'refresh': refresh_token})
    assert 'access' in response.json()


# PUT request tests
def test_api_auth_endpoint_status_code_on_put(api_client):
    response = api_client.put(api_auth_endpoint)
    assert response.status_code == 405


def test_api_auth_endpoint_errors_on_put(api_client):
    response = api_client.put(api_auth_endpoint)
    assert response.json() == {
        'detail': 'Method \"PUT\" not allowed.'
    }


def test_api_refresh_endpoint_status_code_on_put(api_client):
    response = api_client.put(api_refresh_endpoint)
    assert response.status_code == 405


def test_api_refresh_endpoint_errors_on_put(api_client):
    response = api_client.put(api_refresh_endpoint)
    assert response.json() == {
        'detail': 'Method \"PUT\" not allowed.'
    }


# PATCH request tests
def test_api_auth_endpoint_status_code_on_patch(api_client):
    response = api_client.patch(api_auth_endpoint)
    assert response.status_code == 405


def test_api_auth_endpoint_errors_on_patch(api_client):
    response = api_client.patch(api_auth_endpoint)
    assert response.json() == {
        'detail': 'Method \"PATCH\" not allowed.'
    }


def test_api_refresh_endpoint_status_code_on_patch(api_client):
    response = api_client.patch(api_refresh_endpoint)
    assert response.status_code == 405


def test_api_refresh_endpoint_errors_on_patch(api_client):
    response = api_client.patch(api_refresh_endpoint)
    assert response.json() == {
        'detail': 'Method \"PATCH\" not allowed.'
    }


# DELETE request tests
def test_api_auth_endpoint_status_code_on_delete(api_client):
    response = api_client.delete(api_auth_endpoint)
    assert response.status_code == 405


def test_api_auth_endpoint_errors_on_delete(api_client):
    response = api_client.delete(api_auth_endpoint)
    assert response.json() == {
        'detail': 'Method \"DELETE\" not allowed.'
    }


def test_api_refresh_endpoint_status_code_on_delete(api_client):
    response = api_client.delete(api_refresh_endpoint)
    assert response.status_code == 405


def test_api_refresh_endpoint_errors_on_delete(api_client):
    response = api_client.delete(api_refresh_endpoint)
    assert response.json() == {
        'detail': 'Method \"DELETE\" not allowed.'
    }


# HEAD request tests
def test_api_auth_endpoint_status_code_on_head(api_client):
    response = api_client.head(api_auth_endpoint)
    assert response.status_code == 405


def test_api_refresh_endpoint_status_code_on_head(api_client):
    response = api_client.head(api_refresh_endpoint)
    assert response.status_code == 405


# OPTIONS request tests
def test_api_auth_endpoint_status_code_on_options(api_client):
    response = api_client.options(api_auth_endpoint)
    assert response.status_code == 200


def test_api_refresh_endpoint_status_code_on_options(api_client):
    response = api_client.options(api_refresh_endpoint)
    assert response.status_code == 200
