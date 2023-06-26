from django.urls import reverse

from currency.models import ContactUs

contact_us_list_url = reverse('currency:contactus-list')
contact_us_create_url = reverse('currency:contactus-create')


# Create
def test_contact_us_create_status_code_on_get(client):
    response = client.get(contact_us_create_url)
    assert response.status_code == 200


def test_contact_us_create_status_code_on_post_empty_submission(client):
    payload = {}
    response = client.post(contact_us_create_url, data=payload)
    assert response.status_code == 200


def test_contact_us_create_errors_on_post_empty_submission(client):
    payload = {}
    response = client.post(contact_us_create_url, data=payload)
    assert response.context_data['form']._errors == {
        'email_from': ['This field is required.'],
        'subject': ['This field is required.'],
        'message': ['This field is required.']
    }


def test_contact_us_create_status_code_on_post_invalid_email_from_field(client, contact_us):
    payload = {
        'email_from': 'WRONG',
        'subject': contact_us.subject,
        'message': contact_us.message
    }
    response = client.post(contact_us_create_url, data=payload)
    assert response.status_code == 200


def test_contact_us_create_errors_on_post_invalid_email_from_field(client, contact_us):
    payload = {
        'email_from': 'WRONG',
        'subject': contact_us.subject,
        'message': contact_us.message
    }
    response = client.post(contact_us_create_url, data=payload)
    assert response.context_data['form']._errors == {
        'email_from': ['Enter a valid email address.']
    }


def test_contact_us_create_status_code_on_post_invalid_subject_field(client, contact_us):
    payload = {
        'email_from': contact_us.email_from,
        'subject': '',
        'message': contact_us.message
    }
    response = client.post(contact_us_create_url, data=payload)
    assert response.status_code == 200


def test_contact_us_create_errors_on_post_invalid_subject_field(client, contact_us):
    payload = {
        'email_from': contact_us.email_from,
        'subject': '',
        'message': contact_us.message
    }
    response = client.post(contact_us_create_url, data=payload)
    assert response.context_data['form']._errors == {
        'subject':  ['This field is required.']
    }


def test_contact_us_create_status_code_on_post_invalid_message_field(client, contact_us):
    payload = {
        'email_from': contact_us.email_from,
        'subject': contact_us.subject,
        'message': ''
    }
    response = client.post(contact_us_create_url, data=payload)
    assert response.status_code == 200


def test_contact_us_create_errors_on_post_invalid_message_field(client, contact_us):
    payload = {
        'email_from': contact_us.email_from,
        'subject': contact_us.subject,
        'message': ''
    }
    response = client.post(contact_us_create_url, data=payload)
    assert response.context_data['form']._errors == {
        'message':  ['This field is required.']
    }


def test_contact_us_create_status_code_on_post_valid_submission(client, contact_us):
    payload = {
        'email_from': contact_us.email_from,
        'subject': contact_us.subject,
        'message': contact_us.message
    }
    response = client.post(contact_us_create_url, data=payload)
    assert response.status_code == 302


def test_contact_us_create_on_post_valid_submission(client, contact_us):
    payload = {
        'email_from': contact_us.email_from,
        'subject': contact_us.subject,
        'message': contact_us.message
    }
    initial_count = ContactUs.objects.count()
    response = client.post(contact_us_create_url, data=payload)
    checks = (
        response['location'] == contact_us_list_url,
        ContactUs.objects.count() == initial_count + 1
    )
    assert all(checks)


# List
def test_contact_us_list_status_code_on_get(client):
    response = client.get(contact_us_list_url)
    assert response.status_code == 200


def test_contact_us_list_on_get_with_empty_db(client):
    response = client.get(contact_us_list_url)
    assert not response.context_data['object_list'].exists()


def test_contact_us_list_on_get_with_one_record(client, contact_us):
    response = client.get(contact_us_list_url)
    assert response.context_data['object_list'].count() == 1


def test_contact_us_list_on_get_with_multiple_records(client, contact_us_multiple):
    response = client.get(contact_us_list_url)
    assert response.context_data['object_list'].count() == len(contact_us_multiple)


# Details
def test_contact_us_details_status_code_on_get_no_auth(client, contact_us):
    contact_us_details_url = reverse('currency:contactus-details', args=(contact_us.id,))
    response = client.get(contact_us_details_url)
    assert response.status_code == 200


def test_contact_us_details_return_obj_on_get_no_auth(client, contact_us):
    contact_us_details_url = reverse('currency:contactus-details', args=(contact_us.id,))
    response = client.get(contact_us_details_url)
    assert response.context_data['object'] == contact_us


def test_contact_us_details_status_code_on_get_inactive_user(client, user, contact_us):
    client.force_login(user)
    contact_us_details_url = reverse('currency:contactus-details', args=(contact_us.id,))
    response = client.get(contact_us_details_url)
    assert response.status_code == 200


def test_contact_us_details_return_obj_on_get_inactive_user(client, user, contact_us):
    client.force_login(user)
    contact_us_details_url = reverse('currency:contactus-details', args=(contact_us.id,))
    response = client.get(contact_us_details_url)
    assert response.context_data['object'] == contact_us


def test_contact_us_details_status_code_on_get_active_user(client, active_user, contact_us):
    client.force_login(active_user)
    contact_us_details_url = reverse('currency:contactus-details', args=(contact_us.id,))
    response = client.get(contact_us_details_url)
    assert response.status_code == 200


def test_contact_us_details_return_obj_on_get_active_user(client, active_user, contact_us):
    client.force_login(active_user)
    contact_us_details_url = reverse('currency:contactus-details', args=(contact_us.id,))
    response = client.get(contact_us_details_url)
    assert response.context_data['object'] == contact_us


def test_contact_us_details_status_code_on_get_super_user(client, super_user, contact_us):
    client.force_login(super_user)
    contact_us_details_url = reverse('currency:contactus-details', args=(contact_us.id,))
    response = client.get(contact_us_details_url)
    assert response.status_code == 200


def test_contact_us_details_return_obj_on_get_super_user(client, super_user, contact_us):
    client.force_login(super_user)
    contact_us_details_url = reverse('currency:contactus-details', args=(contact_us.id,))
    response = client.get(contact_us_details_url)
    assert response.context_data['object'] == contact_us


# Update
def test_contact_us_update_status_code_on_get_no_auth(client, contact_us):
    contact_us_update_url = reverse('currency:contactus-update', args=(contact_us.id,))
    response = client.get(contact_us_update_url)
    assert response.status_code == 200


def test_contact_us_update_return_obj_on_get_no_auth(client, contact_us):
    contact_us_update_url = reverse('currency:contactus-update', args=(contact_us.id,))
    response = client.get(contact_us_update_url)
    assert response.context_data['object'] == contact_us


def test_contact_us_update_status_code_on_get_inactive_user(client, user, contact_us):
    client.force_login(user)
    contact_us_update_url = reverse('currency:contactus-update', args=(contact_us.id,))
    response = client.get(contact_us_update_url)
    assert response.status_code == 200


def test_contact_us_update_return_obj_on_get_inactive_user(client, user, contact_us):
    client.force_login(user)
    contact_us_update_url = reverse('currency:contactus-update', args=(contact_us.id,))
    response = client.get(contact_us_update_url)
    assert response.context_data['object'] == contact_us


def test_contact_us_update_status_code_on_get_active_user(client, active_user, contact_us):
    client.force_login(active_user)
    contact_us_update_url = reverse('currency:contactus-update', args=(contact_us.id,))
    response = client.get(contact_us_update_url)
    assert response.status_code == 200


def test_contact_us_update_return_obj_on_get_active_user(client, active_user, contact_us):
    client.force_login(active_user)
    contact_us_update_url = reverse('currency:contactus-update', args=(contact_us.id,))
    response = client.get(contact_us_update_url)
    assert response.context_data['object'] == contact_us


def test_contact_us_update_status_code_on_get_super_user(client, super_user, contact_us):
    client.force_login(super_user)
    contact_us_update_url = reverse('currency:contactus-update', args=(contact_us.id,))
    response = client.get(contact_us_update_url)
    assert response.status_code == 200


def test_contact_us_update_return_obj_on_get_super_user(client, super_user, contact_us):
    client.force_login(super_user)
    contact_us_update_url = reverse('currency:contactus-update', args=(contact_us.id,))
    response = client.get(contact_us_update_url)
    assert response.context_data['object'] == contact_us


def test_contact_us_update_status_code_on_post_empty_submission(client, contact_us):
    payload = {}
    contact_us_update_url = reverse('currency:contactus-update', args=(contact_us.id,))
    response = client.post(contact_us_update_url, data=payload)
    assert response.status_code == 200


def test_contact_us_update_errors_on_post_empty_submission(client, contact_us):
    payload = {}
    contact_us_update_url = reverse('currency:contactus-update', args=(contact_us.id,))
    response = client.post(contact_us_update_url, data=payload)
    assert response.context_data['form']._errors == {
        'email_from': ['This field is required.'],
        'subject': ['This field is required.'],
        'message': ['This field is required.']
    }


def test_contact_us_update_status_code_on_post_empty_email_from_field(client, contact_us):
    payload = {
        'email_from': '',
        'subject': contact_us.subject,
        'message': contact_us.message
    }
    contact_us_update_url = reverse('currency:contactus-update', args=(contact_us.id,))
    response = client.post(contact_us_update_url, data=payload)
    assert response.status_code == 200


def test_contact_us_update_errors_on_post_empty_email_from_field(client, contact_us):
    payload = {
        'email_from': '',
        'subject': contact_us.subject,
        'message': contact_us.message
    }
    contact_us_update_url = reverse('currency:contactus-update', args=(contact_us.id,))
    response = client.post(contact_us_update_url, data=payload)
    assert response.context_data['form']._errors == {
        'email_from': ['This field is required.']
    }


def test_contact_us_update_status_code_on_post_invalid_email_from_field(client, contact_us):
    payload = {
        'email_from': 'WRONG',
        'subject': contact_us.subject,
        'message': contact_us.message
    }
    contact_us_update_url = reverse('currency:contactus-update', args=(contact_us.id,))
    response = client.post(contact_us_update_url, data=payload)
    assert response.status_code == 200


def test_contact_us_update_errors_on_post_invalid_email_from_field(client, contact_us):
    payload = {
        'email_from': 'WRONG',
        'subject': contact_us.subject,
        'message': contact_us.message
    }
    contact_us_update_url = reverse('currency:contactus-update', args=(contact_us.id,))
    response = client.post(contact_us_update_url, data=payload)
    assert response.context_data['form']._errors == {
        'email_from': ['Enter a valid email address.']
    }


def test_contact_us_update_status_code_on_post_empty_subject_field(client, contact_us):
    payload = {
        'email_from': contact_us.email_from,
        'subject': '',
        'message': contact_us.message
    }
    contact_us_update_url = reverse('currency:contactus-update', args=(contact_us.id,))
    response = client.post(contact_us_update_url, data=payload)
    assert response.status_code == 200


def test_contact_us_update_errors_on_post_empty_subject_field(client, contact_us):
    payload = {
        'email_from': contact_us.email_from,
        'subject': '',
        'message': contact_us.message
    }
    contact_us_update_url = reverse('currency:contactus-update', args=(contact_us.id,))
    response = client.post(contact_us_update_url, data=payload)
    assert response.context_data['form']._errors == {
        'subject': ['This field is required.']
    }


def test_contact_us_update_status_code_on_post_empty_message_field(client, contact_us):
    payload = {
        'email_from': contact_us.email_from,
        'subject': contact_us.subject,
        'message': ''
    }
    contact_us_update_url = reverse('currency:contactus-update', args=(contact_us.id,))
    response = client.post(contact_us_update_url, data=payload)
    assert response.status_code == 200


def test_contact_us_update_errors_on_post_empty_message_field(client, contact_us):
    payload = {
        'email_from': contact_us.email_from,
        'subject': contact_us.subject,
        'message': ''
    }
    contact_us_update_url = reverse('currency:contactus-update', args=(contact_us.id,))
    response = client.post(contact_us_update_url, data=payload)
    assert response.context_data['form']._errors == {
        'message': ['This field is required.']
    }


def test_contact_us_update_on_post_valid_submission(client, contact_us):
    payload = {
        'email_from': contact_us.email_from,
        'subject': contact_us.subject,
        'message': contact_us.message
    }
    contact_us_update_url = reverse('currency:contactus-update', args=(contact_us.id,))
    response = client.post(contact_us_update_url, data=payload)
    checks = (
        response.status_code == 302,
        response['location'] == contact_us_list_url
    )
    assert all(checks)


# Delete
def test_contact_us_delete_status_code_on_get_no_auth(client, contact_us):
    contact_us_delete_url = reverse('currency:contactus-delete', args=(contact_us.id,))
    response = client.get(contact_us_delete_url)
    assert response.status_code == 200


def test_contact_us_delete_on_post_no_auth(client, contact_us):
    initial_count = ContactUs.objects.count()
    contact_us_delete_url = reverse('currency:contactus-delete', args=(contact_us.id,))
    response = client.post(contact_us_delete_url)
    checks = (
        response.status_code == 302,
        response['location'] == contact_us_list_url,
        ContactUs.objects.count() == initial_count - 1
    )
    assert all(checks)


def test_contact_us_delete_status_code_on_get_inactive_user(client, user, contact_us):
    client.force_login(user)
    contact_us_delete_url = reverse('currency:contactus-delete', args=(contact_us.id,))
    response = client.get(contact_us_delete_url)
    assert response.status_code == 200


def test_contact_us_delete_on_post_inactive_user(client, user, contact_us):
    client.force_login(user)
    initial_count = ContactUs.objects.count()
    contact_us_delete_url = reverse('currency:contactus-delete', args=(contact_us.id,))
    response = client.post(contact_us_delete_url)
    checks = (
        response.status_code == 302,
        response['location'] == contact_us_list_url,
        ContactUs.objects.count() == initial_count - 1
    )
    assert all(checks)


def test_contact_us_delete_status_code_on_get_active_user(client, active_user, contact_us):
    client.force_login(active_user)
    contact_us_delete_url = reverse('currency:contactus-delete', args=(contact_us.id,))
    response = client.get(contact_us_delete_url)
    assert response.status_code == 200


def test_contact_us_delete_on_post_active_user(client, active_user, contact_us):
    client.force_login(active_user)
    initial_count = ContactUs.objects.count()
    contact_us_delete_url = reverse('currency:contactus-delete', args=(contact_us.id,))
    response = client.post(contact_us_delete_url)
    checks = (
        response.status_code == 302,
        response['location'] == contact_us_list_url,
        ContactUs.objects.count() == initial_count - 1
    )
    assert all(checks)


def test_contact_us_delete_status_code_on_get_super_user(client, super_user, contact_us):
    client.force_login(super_user)
    contact_us_delete_url = reverse('currency:contactus-delete', args=(contact_us.id,))
    response = client.get(contact_us_delete_url)
    assert response.status_code == 200


def test_contact_us_delete_on_post_super_user(client, super_user, contact_us):
    client.force_login(super_user)
    initial_count = ContactUs.objects.count()
    contact_us_delete_url = reverse('currency:contactus-delete', args=(contact_us.id,))
    response = client.post(contact_us_delete_url)
    checks = (
        response.status_code == 302,
        response['location'] == contact_us_list_url,
        ContactUs.objects.count() == initial_count - 1
    )
    assert all(checks)
