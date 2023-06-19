from django.urls import reverse

api_contact_us_list_url = reverse('api-currency:feedbacks-list')


# LIST GET
def test_api_contact_us_list_status_code_on_get_no_auth(api_client):
    response = api_client.get(api_contact_us_list_url)
    assert response.status_code == 401


def test_api_contact_us_list_errors_on_get_no_auth(api_client):
    response = api_client.get(api_contact_us_list_url)
    assert response.status_code == 401


def test_api_contact_us_list_status_code_on_get(api_client_authorized):
    response = api_client_authorized.get(api_contact_us_list_url)
    assert response.status_code == 200


def test_api_contact_us_list_on_get_with_empty_db(api_client_authorized):
    response = api_client_authorized.get(api_contact_us_list_url)
    assert len(response.json()['results']) == 0


def test_api_contact_us_list_on_get_with_one_record(api_client_authorized, contact_us):
    response = api_client_authorized.get(api_contact_us_list_url)
    assert len(response.json()['results']) == 1


def test_api_contact_us_list_on_get_with_multiple_records(api_client_authorized,
                                                          contact_us_multiple):
    response = api_client_authorized.get(api_contact_us_list_url)
    assert len(response.json()['results']) == len(contact_us_multiple)


def test_api_contact_us_list_pagination_on_get(api_client_authorized, contact_us_multiple):
    response = api_client_authorized.get(api_contact_us_list_url)
    data = response.json()
    checks = {
        'count' in data,
        'next' in data,
        'previous' in data
    }
    assert all(checks)


# LIST POST
def test_api_contact_us_list_status_code_on_post_empty_data(api_client_authorized):
    payload = {}
    response = api_client_authorized.post(api_contact_us_list_url, data=payload)
    assert response.status_code == 400


def test_api_contact_us_list_errors_on_post_empty_data(api_client_authorized):
    payload = {}
    response = api_client_authorized.post(api_contact_us_list_url, data=payload)
    assert response.json() == {
        'email_from': ['This field is required.'],
        'subject': ['This field is required.'],
        'message': ['This field is required.']
    }


def test_api_contact_us_list_status_code_on_post_invalid_email_from_field(api_client_authorized,
                                                                          contact_us):
    payload = {
        'email_from': 'WRONG_MAIL',
        'subject': contact_us.subject,
        'message': contact_us.message
    }
    response = api_client_authorized.post(api_contact_us_list_url, data=payload)
    assert response.status_code == 400


def test_api_contact_us_list_errors_on_post_invalid_email_from_field(api_client_authorized,
                                                                     contact_us):
    payload = {
        'email_from': 'WRONG_MAIL',
        'subject': contact_us.subject,
        'message': contact_us.message
    }
    response = api_client_authorized.post(api_contact_us_list_url, data=payload)
    assert response.json() == {
        'email_from': ['Enter a valid email address.']
    }


def test_api_contact_us_list_status_code_on_post_empty_email_from_field(api_client_authorized,
                                                                        contact_us):
    payload = {
        'email_from': '',
        'subject': contact_us.subject,
        'message': contact_us.message
    }
    response = api_client_authorized.post(api_contact_us_list_url, data=payload)
    assert response.status_code == 400


def test_api_contact_us_list_errors_on_post_empty_email_from_field(api_client_authorized,
                                                                   contact_us):
    payload = {
        'email_from': '',
        'subject': contact_us.subject,
        'message': contact_us.message
    }
    response = api_client_authorized.post(api_contact_us_list_url, data=payload)
    assert response.json() == {
        'email_from': ['This field may not be blank.']
    }


def test_api_contact_us_list_status_code_on_post_empty_subject_field(api_client_authorized,
                                                                     contact_us):
    payload = {
        'email_from': contact_us.email_from,
        'subject': '',
        'message': contact_us.message
    }
    response = api_client_authorized.post(api_contact_us_list_url, data=payload)
    assert response.status_code == 400


def test_api_contact_us_list_errors_on_post_empty_subject_field(api_client_authorized,
                                                                contact_us):
    payload = {
        'email_from': contact_us.email_from,
        'subject': '',
        'message': contact_us.message
    }
    response = api_client_authorized.post(api_contact_us_list_url, data=payload)
    assert response.json() == {
        'subject': ['This field may not be blank.']
    }


def test_api_contact_us_list_status_code_on_post_empty_message_field(api_client_authorized,
                                                                     contact_us):
    payload = {
        'email_from': contact_us.email_from,
        'subject': contact_us.subject,
        'message': ''
    }
    response = api_client_authorized.post(api_contact_us_list_url, data=payload)
    assert response.status_code == 400


def test_api_contact_us_list_errors_on_post_empty_message_field(api_client_authorized, contact_us):
    payload = {
        'email_from': contact_us.email_from,
        'subject': contact_us.subject,
        'message': ''
    }
    response = api_client_authorized.post(api_contact_us_list_url, data=payload)
    assert response.json() == {
        'message': ['This field may not be blank.']
    }


def test_api_contact_us_list_status_code_on_post_valid_submission(api_client_authorized,
                                                                  contact_us):
    payload = {
        'email_from': contact_us.email_from,
        'subject': contact_us.subject,
        'message': contact_us.message
    }
    response = api_client_authorized.post(api_contact_us_list_url, data=payload)
    assert response.status_code == 201


def test_api_contact_us_list_return_obj_on_post_valid_submission(api_client_authorized, contact_us):
    payload = {
        'email_from': contact_us.email_from,
        'subject': contact_us.subject,
        'message': contact_us.message
    }
    response = api_client_authorized.post(api_contact_us_list_url, data=payload)
    assert response.json() == payload


# LIST PUT
def test_api_contact_us_list_status_code_on_put_no_auth(api_client):
    response = api_client.put(api_contact_us_list_url)
    assert response.status_code == 401


def test_api_contact_us_list_errors_on_put_no_auth(api_client):
    response = api_client.put(api_contact_us_list_url)
    assert response.json() == {
        'detail': 'Authentication credentials were not provided.'
    }


def test_api_contact_us_list_status_code_on_put(api_client_authorized):
    response = api_client_authorized.put(api_contact_us_list_url)
    assert response.status_code == 405


def test_api_contact_us_list_errors_on_put(api_client_authorized):
    response = api_client_authorized.put(api_contact_us_list_url)
    assert response.json() == {
        'detail': 'Method \"PUT\" not allowed.'
    }


# LIST DELETE
def test_api_contact_us_list_status_code_on_delete_no_auth(api_client):
    response = api_client.delete(api_contact_us_list_url)
    assert response.status_code == 401


def test_api_contact_us_list_errors_on_delete_no_auth(api_client):
    response = api_client.delete(api_contact_us_list_url)
    assert response.json() == {
        'detail': 'Authentication credentials were not provided.'
    }


def test_api_contact_us_list_status_code_on_delete(api_client_authorized):
    response = api_client_authorized.delete(api_contact_us_list_url)
    assert response.status_code == 405


def test_api_contact_us_list_errors_on_delete(api_client_authorized):
    response = api_client_authorized.delete(api_contact_us_list_url)
    assert response.json() == {
        'detail': 'Method \"DELETE\" not allowed.'
    }


# DETAILS GET
def test_api_contact_us_details_status_code_on_get_no_auth(api_client, contact_us):
    response = api_client.get(api_contact_us_list_url + f'{contact_us.id}/')
    assert response.status_code == 401


def test_api_contact_us_details_errors_on_get_no_auth(api_client, contact_us):
    response = api_client.get(api_contact_us_list_url + f'{contact_us.id}/')
    assert response.json() == {
        'detail': 'Authentication credentials were not provided.'
    }


def test_api_contact_us_details_status_code_on_get(api_client_authorized, contact_us):
    response = api_client_authorized.get(api_contact_us_list_url + f'{contact_us.id}/')
    assert response.status_code == 200


def test_api_contact_us_details_return_obj_on_get(api_client_authorized, contact_us):
    response = api_client_authorized.get(api_contact_us_list_url + f'{contact_us.id}/')
    assert response.json() == {
        'email_from': contact_us.email_from,
        'subject': contact_us.subject,
        'message': contact_us.message
    }


# DETAILS PUT
def test_api_contact_us_details_status_code_on_put_no_auth(api_client, contact_us):
    response = api_client.put(api_contact_us_list_url + f'{contact_us.id}/')
    assert response.status_code == 401


def test_api_contact_us_details_errors_on_put_no_auth(api_client, contact_us):
    response = api_client.put(api_contact_us_list_url + f'{contact_us.id}/')
    assert response.json() == {
        'detail': 'Authentication credentials were not provided.'
    }


def test_api_contact_uf_details_status_code_on_put_valid_submission(api_client_authorized,
                                                                    contact_us):
    payload = {
        'email_from': contact_us.email_from,
        'subject': contact_us.subject,
        'message': contact_us.message
    }
    response = api_client_authorized.put(api_contact_us_list_url + f'{contact_us.id}/',
                                         data=payload)
    assert response.status_code == 200


def test_api_contact_uf_details_return_obj_on_put_valid_submission(api_client_authorized,
                                                                   contact_us):
    payload = {
        'email_from': contact_us.email_from,
        'subject': contact_us.subject,
        'message': contact_us.message
    }
    response = api_client_authorized.put(api_contact_us_list_url + f'{contact_us.id}/',
                                         data=payload)
    assert response.json() == payload


def test_api_contact_uf_details_status_code_on_put_empty_submission(api_client_authorized,
                                                                    contact_us):
    payload = {}
    response = api_client_authorized.put(api_contact_us_list_url + f'{contact_us.id}/',
                                         data=payload)
    assert response.status_code == 400


def test_api_contact_uf_details_return_obj_on_put_empty_submission(api_client_authorized,
                                                                   contact_us):
    payload = {}
    response = api_client_authorized.put(api_contact_us_list_url + f'{contact_us.id}/',
                                         data=payload)
    assert response.json() == {
        'email_from': ['This field is required.'],
        'subject': ['This field is required.'],
        'message': ['This field is required.']
    }


def test_api_contact_us_details_status_code_on_put_new_email_from_field(api_client_authorized,
                                                                        contact_us):
    payload = {
        'email_from': 'example@mail.com',
        'subject': contact_us.subject,
        'message': contact_us.message
    }
    response = api_client_authorized.put(api_contact_us_list_url + f'{contact_us.id}/',
                                         data=payload)
    assert response.status_code == 200


def test_api_contact_us_details_errors_on_put_new_email_from_field(api_client_authorized,
                                                                   contact_us):
    payload = {
        'email_from': 'example@mail.com',
        'subject': contact_us.subject,
        'message': contact_us.message
    }
    response = api_client_authorized.put(api_contact_us_list_url + f'{contact_us.id}/',
                                         data=payload)
    assert response.json() == payload


def test_api_contact_us_details_status_code_on_put_new_subject_field(api_client_authorized,
                                                                     contact_us):
    payload = {
        'email_from': contact_us.email_from,
        'subject': 'NEW_SUBJ',
        'message': contact_us.message
    }
    response = api_client_authorized.put(api_contact_us_list_url + f'{contact_us.id}/',
                                         data=payload)
    assert response.status_code == 200


def test_api_contact_us_details_errors_on_put_new_subject_field(api_client_authorized,
                                                                contact_us):
    payload = {
        'email_from': contact_us.email_from,
        'subject': 'NEW_SUBJ',
        'message': contact_us.message
    }
    response = api_client_authorized.put(api_contact_us_list_url + f'{contact_us.id}/',
                                         data=payload)
    assert response.json() == payload


def test_api_contact_us_details_status_code_on_put_new_message_field(api_client_authorized,
                                                                     contact_us):
    payload = {
        'email_from': contact_us.email_from,
        'subject': contact_us.subject,
        'message': 'NEW_MSG'
    }
    response = api_client_authorized.put(api_contact_us_list_url + f'{contact_us.id}/',
                                         data=payload)
    assert response.status_code == 200


def test_api_contact_us_details_errors_on_put_new_message_field(api_client_authorized,
                                                                contact_us):
    payload = {
        'email_from': contact_us.email_from,
        'subject': contact_us.subject,
        'message': 'NEW_MSG'
    }
    response = api_client_authorized.put(api_contact_us_list_url + f'{contact_us.id}/',
                                         data=payload)
    assert response.json() == payload


# DETAILS DELETE
def test_api_contact_us_details_status_code_on_delete_no_auth_valid_submission(api_client,
                                                                               contact_us):
    response = api_client.delete(api_contact_us_list_url + f'{contact_us.id}/')
    assert response.status_code == 401


def test_api_contact_us_details_status_code_on_delete_no_auth_invalid_submission(api_client):
    response = api_client.delete(api_contact_us_list_url + '-1/')
    assert response.status_code == 401


def test_api_contact_us_details_status_code_on_delete_valid_submission(api_client_authorized,
                                                                       contact_us):
    response = api_client_authorized.delete(api_contact_us_list_url + f'{contact_us.id}/')
    assert response.status_code == 204


def test_api_contact_us_details_status_code_on_delete_invalid_submission(api_client_authorized):
    response = api_client_authorized.delete(api_contact_us_list_url + '-1/')
    assert response.status_code == 404
