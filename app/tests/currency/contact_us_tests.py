from currency.models import ContactUs


# Create
def test_contact_us_create_status_200(client):
    response = client.get('/currency/contact_us/create/')
    assert response.status_code == 200


def test_contact_us_create_empty_form_status_200(client):
    response = client.post('/currency/contact_us/create/')
    assert response.status_code == 200


def test_contact_us_create_empty_form_errors(client):
    payload = {}
    response = client.post('/currency/contact_us/create/', data=payload)
    assert response.context_data['form']._errors == {
        'email_from': ['This field is required.'],
        'subject': ['This field is required.'],
        'message': ['This field is required.']
    }


def test_contact_us_create_invalid_email_status_200(client, contact_us):
    payload = {
        'email_from': 'WRONG',
        'subject': contact_us.subject,
        'message': contact_us.message
    }
    response = client.post('/currency/contact_us/create/', data=payload)
    assert response.status_code == 200


def test_contact_us_create_invalid_email_errors(client, contact_us):
    payload = {
        'email_from': 'WRONG',
        'subject': contact_us.subject,
        'message': contact_us.message
    }
    response = client.post('/currency/contact_us/create/', data=payload)
    assert response.context_data['form']._errors == {'email_from': ['Enter a valid email address.']}


def test_contact_us_create_invalid_subject_status_200(client, contact_us):
    payload = {
        'email_from': contact_us.email_from,
        'subject': '',
        'message': contact_us.message
    }
    response = client.post('/currency/contact_us/create/', data=payload)
    assert response.status_code == 200


def test_contact_us_create_invalid_subject_errors(client, contact_us):
    payload = {
        'email_from': contact_us.email_from,
        'subject': '',
        'message': contact_us.message
    }
    response = client.post('/currency/contact_us/create/', data=payload)
    assert response.context_data['form']._errors == {'subject':  ['This field is required.']}


def test_contact_us_create_invalid_message_status_200(client, contact_us):
    payload = {
        'email_from': contact_us.email_from,
        'subject': contact_us.subject,
        'message': ''
    }
    response = client.post('/currency/contact_us/create/', data=payload)
    assert response.status_code == 200


def test_contact_us_create_invalid_message_errors(client, contact_us):
    payload = {
        'email_from': contact_us.email_from,
        'subject': contact_us.subject,
        'message': ''
    }
    response = client.post('/currency/contact_us/create/', data=payload)
    assert response.context_data['form']._errors == {'message':  ['This field is required.']}


def test_contact_us_create_valid_form_status_302(client, contact_us):
    payload = {
        'email_from': contact_us.email_from,
        'subject': contact_us.subject,
        'message': contact_us.message
    }
    response = client.post('/currency/contact_us/create/', data=payload)
    assert response.status_code == 302


def test_contact_us_create_valid_form_data(client, contact_us):
    initial_count = ContactUs.objects.count()
    payload = {
        'email_from': contact_us.email_from,
        'subject': contact_us.subject,
        'message': contact_us.message
    }
    response = client.post('/currency/contact_us/create/', data=payload)
    checks = (
        response['location'] == '/currency/contact_us/list/',
        ContactUs.objects.count() == initial_count + 1
    )
    assert all(checks)


# List
def test_contact_us_list_status_200(client):
    response = client.get('/currency/contact_us/list/')
    assert response.status_code == 200


def test_contact_us_list_empty_db(client):
    response = client.get('/currency/contact_us/list/')
    assert not response.context_data['object_list'].exists()


def test_contact_us_list_single_entity(client, contact_us):
    response = client.get('/currency/contact_us/list/')
    assert response.context_data['object_list'].count() == 1


def test_contact_us_list_multiple_entities(client, contact_us_multiple):
    response = client.get('/currency/contact_us/list/')
    assert response.context_data['object_list'].count() == len(contact_us_multiple)


# Details
# noinspection DuplicatedCode
def test_contact_us_details_no_auth_status_200(client, contact_us):
    response = client.get(f'/currency/contact_us/details/{contact_us.id}/')
    assert response.status_code == 200


def test_contact_us_details_no_auth_model_obj(client, contact_us):
    response = client.get(f'/currency/contact_us/details/{contact_us.id}/')
    assert response.context_data['object'] == contact_us


def test_contact_us_details_inactive_user_status_200(client, user, contact_us):
    client.force_login(user)
    response = client.get(f'/currency/contact_us/details/{contact_us.id}/')
    assert response.status_code == 200


def test_contact_us_details_inactive_user_model_obj(client, user, contact_us):
    client.force_login(user)
    response = client.get(f'/currency/contact_us/details/{contact_us.id}/')
    assert response.context_data['object'] == contact_us


def test_contact_us_details_active_user_status_200(client, active_user, contact_us):
    client.force_login(active_user)
    response = client.get(f'/currency/contact_us/details/{contact_us.id}/')
    assert response.status_code == 200


def test_contact_us_details_active_user_model_obj(client, active_user, contact_us):
    client.force_login(active_user)
    response = client.get(f'/currency/contact_us/details/{contact_us.id}/')
    assert response.context_data['object'] == contact_us


def test_contact_us_details_super_user_status_200(client, super_user, contact_us):
    client.force_login(super_user)
    response = client.get(f'/currency/contact_us/details/{contact_us.id}/')
    assert response.status_code == 200


def test_contact_us_details_super_user_model_obj(client, super_user, contact_us):
    client.force_login(super_user)
    response = client.get(f'/currency/contact_us/details/{contact_us.id}/')
    assert response.context_data['object'] == contact_us


# Update
# noinspection DuplicatedCode
def test_contact_us_update_no_auth_status_200(client, contact_us):
    response = client.get(f'/currency/contact_us/update/{contact_us.id}/')
    assert response.status_code == 200


def test_contact_us_update_no_auth_model_obj(client, contact_us):
    response = client.get(f'/currency/contact_us/update/{contact_us.id}/')
    assert response.context_data['object'] == contact_us


def test_contact_us_update_inactive_user_status_200(client, user, contact_us):
    client.force_login(user)
    response = client.get(f'/currency/contact_us/update/{contact_us.id}/')
    assert response.status_code == 200


def test_contact_us_update_inactive_user_model_obj(client, user, contact_us):
    client.force_login(user)
    response = client.get(f'/currency/contact_us/update/{contact_us.id}/')
    assert response.context_data['object'] == contact_us


def test_contact_us_update_active_user_status_200(client, active_user, contact_us):
    client.force_login(active_user)
    response = client.get(f'/currency/contact_us/update/{contact_us.id}/')
    assert response.status_code == 200


def test_contact_us_update_active_user_model_obj(client, active_user, contact_us):
    client.force_login(active_user)
    response = client.get(f'/currency/contact_us/update/{contact_us.id}/')
    assert response.context_data['object'] == contact_us


def test_contact_us_update_super_user_status_200(client, super_user, contact_us):
    client.force_login(super_user)
    response = client.get(f'/currency/contact_us/update/{contact_us.id}/')
    assert response.status_code == 200


def test_contact_us_update_super_user_model_obj(client, super_user, contact_us):
    client.force_login(super_user)
    response = client.get(f'/currency/contact_us/update/{contact_us.id}/')
    assert response.context_data['object'] == contact_us


def test_contact_us_update_empty_form_status_200(client, contact_us):
    payload = {}
    response = client.post(f'/currency/contact_us/update/{contact_us.id}/', data=payload)
    assert response.status_code == 200


def test_contact_us_update_empty_form_errors(client, contact_us):
    payload = {}
    response = client.post(f'/currency/contact_us/update/{contact_us.id}/', data=payload)
    assert response.context_data['form']._errors == {
        'email_from': ['This field is required.'],
        'subject': ['This field is required.'],
        'message': ['This field is required.']
    }


def test_contact_us_update_invalid_email_from_status_200(client, contact_us):
    payload = {
        'email_from': '',
        'subject': contact_us.subject,
        'message': contact_us.message
    }
    response = client.post(f'/currency/contact_us/update/{contact_us.id}/', data=payload)
    assert response.status_code == 200


def test_contact_us_update_invalid_email_from_errors(client, contact_us):
    payload = {
        'email_from': '',
        'subject': contact_us.subject,
        'message': contact_us.message
    }
    response = client.post(f'/currency/contact_us/update/{contact_us.id}/', data=payload)
    assert response.context_data['form']._errors == {'email_from': ['This field is required.']}


def test_contact_us_update_empty_email_from_errors(client, contact_us):
    payload = {
        'email_from': 'WRONG',
        'subject': contact_us.subject,
        'message': contact_us.message
    }
    response = client.post(f'/currency/contact_us/update/{contact_us.id}/', data=payload)
    assert response.context_data['form']._errors == {'email_from': ['Enter a valid email address.']}


def test_contact_us_update_invalid_subject_status_200(client, contact_us):
    payload = {
        'email_from': contact_us.email_from,
        'subject': '',
        'message': contact_us.message
    }
    response = client.post(f'/currency/contact_us/update/{contact_us.id}/', data=payload)
    assert response.status_code == 200


def test_contact_us_update_invalid_subject_errors(client, contact_us):
    payload = {
        'email_from': contact_us.email_from,
        'subject': '',
        'message': contact_us.message
    }
    response = client.post(f'/currency/contact_us/update/{contact_us.id}/', data=payload)
    assert response.context_data['form']._errors == {'subject': ['This field is required.']}


def test_contact_us_update_invalid_message_status_200(client, contact_us):
    payload = {
        'email_from': contact_us.email_from,
        'subject': contact_us.subject,
        'message': ''
    }
    response = client.post(f'/currency/contact_us/update/{contact_us.id}/', data=payload)
    assert response.status_code == 200


def test_contact_us_update_invalid_message_errors(client, contact_us):
    payload = {
        'email_from': contact_us.email_from,
        'subject': contact_us.subject,
        'message': ''
    }
    response = client.post(f'/currency/contact_us/update/{contact_us.id}/', data=payload)
    assert response.context_data['form']._errors == {'message': ['This field is required.']}


def test_contact_us_update_valid_form_status_302(client, contact_us):
    payload = {
        'email_from': contact_us.email_from,
        'subject': contact_us.subject,
        'message': contact_us.message
    }
    response = client.post(f'/currency/contact_us/update/{contact_us.id}/', data=payload)
    assert response.status_code == 302


def test_contact_us_update_valid_form_data(client, contact_us):
    payload = {
        'email_from': contact_us.email_from,
        'subject': contact_us.subject,
        'message': contact_us.message
    }
    response = client.post(f'/currency/contact_us/update/{contact_us.id}/', data=payload)
    assert response['location'] == '/currency/contact_us/list/'


# Delete
# noinspection DuplicatedCode
def test_contact_us_delete_no_auth_status_200(client, contact_us):
    response = client.get(f'/currency/contact_us/delete/{contact_us.id}/')
    assert response.status_code == 200


def test_contact_us_delete_no_auth_data(client, contact_us):
    initial_count = ContactUs.objects.count()
    response = client.post(f'/currency/contact_us/delete/{contact_us.id}/')
    checks = (
        response['location'] == '/currency/contact_us/list/',
        ContactUs.objects.count() == initial_count - 1
    )
    assert all(checks)


# noinspection DuplicatedCode
def test_contact_us_delete_inactive_user_status_200(client, user, contact_us):
    client.force_login(user)
    response = client.get(f'/currency/contact_us/delete/{contact_us.id}/')
    assert response.status_code == 200


def test_contact_us_delete_inactive_user_data(client, user, contact_us):
    initial_count = ContactUs.objects.count()
    client.force_login(user)
    response = client.post(f'/currency/contact_us/delete/{contact_us.id}/')
    checks = (
        response['location'] == '/currency/contact_us/list/',
        ContactUs.objects.count() == initial_count - 1
    )
    assert all(checks)


# noinspection DuplicatedCode
def test_contact_us_delete_active_user_status_200(client, active_user, contact_us):
    client.force_login(active_user)
    response = client.get(f'/currency/contact_us/delete/{contact_us.id}/')
    assert response.status_code == 200


def test_contact_us_delete_active_user_data(client, active_user, contact_us):
    initial_count = ContactUs.objects.count()
    client.force_login(active_user)
    response = client.post(f'/currency/contact_us/delete/{contact_us.id}/')
    checks = (
        response['location'] == '/currency/contact_us/list/',
        ContactUs.objects.count() == initial_count - 1
    )
    assert all(checks)


# noinspection DuplicatedCode
def test_contact_us_delete_super_user_status_200(client, super_user, contact_us):
    client.force_login(super_user)
    response = client.get(f'/currency/contact_us/delete/{contact_us.id}/')
    assert response.status_code == 200


def test_contact_us_delete_super_user_data(client, super_user, contact_us):
    initial_count = ContactUs.objects.count()
    client.force_login(super_user)
    response = client.post(f'/currency/contact_us/delete/{contact_us.id}/')
    checks = (
        response['location'] == '/currency/contact_us/list/',
        ContactUs.objects.count() == initial_count - 1
    )
    assert all(checks)
