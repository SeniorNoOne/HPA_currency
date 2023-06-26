from django.conf import settings
from django.templatetags.static import static
from django.urls import reverse

from currency.models import Source
from currency.constants import StorageUniqueFields
from utils.common import get_upload_to_path

source_list_url = reverse('currency:source-list')
source_create_url = reverse('currency:source-create')


# Create
def test_source_create_status_code_on_get(client):
    response = client.get(source_create_url)
    assert response.status_code == 200


def test_source_create_status_code_on_post_empty_submission(client):
    payload = {}
    response = client.post(source_create_url, data=payload)
    assert response.status_code == 200


def test_source_create_errors_on_post_empty_submission(client):
    payload = {}
    response = client.post(source_create_url, data=payload)
    assert response.context_data['form']._errors == {
        'url': ['This field is required.'],
        'name': ['This field is required.'],
        'code': ['This field is required.']
    }


def test_source_create_status_code_on_post_empty_url_field(client, source):
    payload = {
        'url': '',
        'name': source.name,
        'code': source.code + 1
    }
    response = client.post(source_create_url, data=payload)
    assert response.status_code == 200


def test_source_create_errors_on_post_empty_url_field(client, source):
    payload = {
        'url': '',
        'name': source.name,
        'code': source.code + 1
    }
    response = client.post(source_create_url, data=payload)
    assert response.context_data['form']._errors == {
        'url': ['This field is required.']
    }


def test_source_create_status_code_on_post_empty_name_field(client, source):
    payload = {
        'url': source.url,
        'name': '',
        'code': source.code + 1
    }
    response = client.post(source_create_url, data=payload)
    assert response.status_code == 200


def test_source_create_errors_on_post_empty_name_field(client, source):
    payload = {
        'url': source.url,
        'name': '',
        'code': source.code + 1
    }
    response = client.post(source_create_url, data=payload)
    assert response.context_data['form']._errors == {
        'name': ['This field is required.']
    }


def test_source_create_status_code_on_post_existing_code_field(client, source):
    payload = {
        'url': source.url,
        'name': source.name,
        'code': source.code
    }
    response = client.post(source_create_url, data=payload)
    assert response.status_code == 200


def test_source_create_errors_on_post_existing_code_field(client, source):
    payload = {
        'url': source.url,
        'name': source.name,
        'code': source.code
    }
    response = client.post(source_create_url, data=payload)
    assert response.context_data['form']._errors == {
        'code': ['Source with this Code already exists.']
    }


def test_source_create_status_code_on_post_invalid_code_field(client, source):
    payload = {
        'url': source.url,
        'name': source.name,
        'code': 'WRONG'
    }
    response = client.post(source_create_url, data=payload)
    assert response.status_code == 200


def test_source_create_errors_on_post_invalid_code_field(client, source):
    payload = {
        'url': source.url,
        'name': source.name,
        'code': 'WRONG'
    }
    response = client.post(source_create_url, data=payload)
    assert response.context_data['form']._errors == {
        'code': ['Enter a whole number.']
    }


def test_source_create_status_code_on_post_valid_submission(client, source):
    payload = {
        'url': source.url,
        'name': source.name,
        'code': source.code + 1
    }
    response = client.post(source_create_url, data=payload)
    assert response.status_code == 302


def test_source_create_on_post_valid_submission(client, source):
    payload = {
        'url': source.url,
        'name': source.name,
        'code': source.code + 1
    }
    initial_count = Source.objects.count()
    response = client.post(source_create_url, data=payload)
    checks = (
        response['location'] == source_list_url,
        Source.objects.count() == initial_count + 1
    )
    assert all(checks)


# List
def test_source_list_status_code_on_get(client):
    response = client.get(source_list_url)
    assert response.status_code == 200


def test_source_list_on_get_with_empty_db(client):
    response = client.get(source_list_url)
    assert not response.context_data['object_list'].exists()


def test_source_list_on_get_with_one_record(client, source):
    response = client.get(source_list_url)
    assert response.context_data['object_list'].count() == 1


def test_source_list_on_get_with_multiple_record(client, sources):
    response = client.get(source_list_url)
    assert response.context_data['object_list'].count() == len(sources)


# Details
def test_source_details_status_code_on_get_no_auth(client, source):
    source_details_url = reverse('currency:source-details', args=(source.id,))
    response = client.get(source_details_url)
    assert response.status_code == 200


def test_source_details_return_obj_on_get_no_auth(client, source):
    source_details_url = reverse('currency:source-details', args=(source.id,))
    response = client.get(source_details_url)
    assert response.context_data['object'] == source


def test_source_details_status_code_on_get_inactive_user(client, user, source):
    client.force_login(user)
    source_details_url = reverse('currency:source-details', args=(source.id,))
    response = client.get(source_details_url)
    assert response.status_code == 200


def test_source_details_return_obj_on_get_inactive_user(client, user, source):
    client.force_login(user)
    source_details_url = reverse('currency:source-details', args=(source.id,))
    response = client.get(source_details_url)
    assert response.context_data['object'] == source


def test_source_details_status_code_on_get_active_user(client, active_user, source):
    client.force_login(active_user)
    source_details_url = reverse('currency:source-details', args=(source.id,))
    response = client.get(source_details_url)
    assert response.status_code == 200


def test_source_details_return_obj_on_get_active_user(client, active_user, source):
    client.force_login(active_user)
    source_details_url = reverse('currency:source-details', args=(source.id,))
    response = client.get(source_details_url)
    assert response.context_data['object'] == source


def test_source_details_status_code_on_get_super_user(client, super_user, source):
    client.force_login(super_user)
    source_details_url = reverse('currency:source-details', args=(source.id,))
    response = client.get(source_details_url)
    assert response.status_code == 200


def test_source_details_return_obj_on_get_super_user(client, super_user, source):
    client.force_login(super_user)
    source_details_url = reverse('currency:source-details', args=(source.id,))
    response = client.get(source_details_url)
    assert response.context_data['object'] == source


# Update
def test_source_update_status_code_on_get_no_auth(client, source):
    source_update_url = reverse('currency:source-update', args=(source.id,))
    response = client.get(source_update_url)
    assert response.status_code == 200


def test_source_update_return_obj_on_get_no_auth(client, source):
    source_update_url = reverse('currency:source-update', args=(source.id,))
    response = client.get(source_update_url)
    assert response.context_data['object'] == source


def test_source_update_status_code_on_get_inactive_user(client, user, source):
    client.force_login(user)
    source_update_url = reverse('currency:source-update', args=(source.id,))
    response = client.get(source_update_url)
    assert response.status_code == 200


def test_source_update_return_obj_on_get_inactive_user(client, user, source):
    client.force_login(user)
    source_update_url = reverse('currency:source-update', args=(source.id,))
    response = client.get(source_update_url)
    assert response.context_data['object'] == source


def test_source_update_status_code_on_get_active_user(client, active_user, source):
    client.force_login(active_user)
    source_update_url = reverse('currency:source-update', args=(source.id,))
    response = client.get(source_update_url)
    assert response.status_code == 200


def test_source_update_return_obj_on_get_active_user(client, active_user, source):
    client.force_login(active_user)
    source_update_url = reverse('currency:source-update', args=(source.id,))
    response = client.get(source_update_url)
    assert response.context_data['object'] == source


def test_source_update_status_code_on_get_super_user(client, super_user, source):
    client.force_login(super_user)
    source_update_url = reverse('currency:source-update', args=(source.id,))
    response = client.get(source_update_url)
    assert response.status_code == 200


def test_source_update_return_ojb_on_get_super_user(client, super_user, source):
    client.force_login(super_user)
    source_update_url = reverse('currency:source-update', args=(source.id,))
    response = client.get(source_update_url)
    assert response.context_data['object'] == source


def test_source_update_status_code_on_post_empty_submission(client, source):
    payload = {}
    source_update_url = reverse('currency:source-update', args=(source.id,))
    response = client.post(source_update_url, data=payload)
    assert response.status_code == 200


def test_source_update_errors_on_post_empty_submission(client, source):
    payload = {}
    source_update_url = reverse('currency:source-update', args=(source.id,))
    response = client.post(source_update_url, data=payload)
    assert response.context_data['form']._errors == {
        'url': ['This field is required.'],
        'name': ['This field is required.'],
        'code': ['This field is required.']
    }


def test_source_update_status_code_on_post_empty_url_field(client, source):
    payload = {
        'url': '',
        'name': source.name,
        'code': source.name
    }
    source_update_url = reverse('currency:source-update', args=(source.id,))
    response = client.post(source_update_url, data=payload)
    assert response.status_code == 200


def test_source_update_errors_on_post_empty_url_field(client, source):
    payload = {
        'url': '',
        'name': source.name,
        'code': source.code
    }
    source_update_url = reverse('currency:source-update', args=(source.id,))
    response = client.post(source_update_url, data=payload)
    assert response.context_data['form']._errors == {
        'url': ['This field is required.']
    }


def test_source_update_status_code_on_post_empty_name_field(client, source):
    payload = {
        'url': source.url,
        'name': '',
        'code': source.code
    }
    source_update_url = reverse('currency:source-update', args=(source.id,))
    response = client.post(source_update_url, data=payload)
    assert response.status_code == 200


def test_source_update_errors_on_post_empty_name_field(client, source):
    payload = {
        'url': source.url,
        'name': '',
        'code': source.code
    }
    source_update_url = reverse('currency:source-update', args=(source.id,))
    response = client.post(source_update_url, data=payload)
    assert response.context_data['form']._errors == {
        'name': ['This field is required.']
    }


def test_source_update_status_code_on_post_invalid_code_field(client, source):
    payload = {
        'url': source.url,
        'name': source.name,
        'code': 'WRONG'
    }
    source_update_url = reverse('currency:source-update', args=(source.id,))
    response = client.post(source_update_url, data=payload)
    assert response.status_code == 200


def test_source_update_errors_on_post_invalid_code_field(client, source):
    payload = {
        'url': source.url,
        'name': source.name,
        'code': 'WRONG'
    }
    source_update_url = reverse('currency:source-update', args=(source.id,))
    response = client.post(source_update_url, data=payload)
    assert response.context_data['form']._errors == {
        'code': ['Enter a whole number.']
    }


def test_source_update_on_post_valid_submission(client, source):
    payload = {
        'url': source.url,
        'name': source.name,
        'code': source.code + 1
    }
    source_update_url = reverse('currency:source-update', args=(source.id,))
    response = client.post(source_update_url, data=payload)
    checks = (
        response.status_code == 302,
        response['location'] == source_list_url
    )
    assert all(checks)


# Delete
def test_source_delete_status_code_on_get_no_auth(client, source):
    source_delete_url = reverse('currency:source-delete', args=(source.id,))
    response = client.get(source_delete_url)
    assert response.status_code == 200


def test_source_delete_on_get_no_auth(client, source):
    initial_count = Source.objects.count()
    source_delete_url = reverse('currency:source-delete', args=(source.id,))
    response = client.post(source_delete_url)
    checks = (
        response.status_code == 302,
        response['location'] == source_list_url,
        Source.objects.count() == initial_count - 1
    )
    assert all(checks)


def test_source_delete_status_code_on_get_inactive_user(client, user, source):
    client.force_login(user)
    source_delete_url = reverse('currency:source-delete', args=(source.id,))
    response = client.get(source_delete_url)
    assert response.status_code == 200


def test_source_delete_on_get_inactive_user(client, user, source):
    client.force_login(user)
    initial_count = Source.objects.count()
    source_delete_url = reverse('currency:source-delete', args=(source.id,))
    response = client.post(source_delete_url)
    checks = (
        response.status_code == 302,
        response['location'] == source_list_url,
        Source.objects.count() == initial_count - 1
    )
    assert all(checks)


def test_source_delete_status_code_on_get_active_user(client, active_user, source):
    client.force_login(active_user)
    source_delete_url = reverse('currency:source-delete', args=(source.id,))
    response = client.get(source_delete_url)
    assert response.status_code == 200


def test_source_delete_active_user_data(client, active_user, source):
    client.force_login(active_user)
    initial_count = Source.objects.count()
    source_delete_url = reverse('currency:source-delete', args=(source.id,))
    response = client.post(source_delete_url)
    checks = (
        response.status_code == 302,
        response['location'] == source_list_url,
        Source.objects.count() == initial_count - 1
    )
    assert all(checks)


def test_source_delete_status_code_on_get_super_user(client, super_user, source):
    client.force_login(super_user)
    source_delete_url = reverse('currency:source-delete', args=(source.id,))
    response = client.get(source_delete_url)
    assert response.status_code == 200


def test_source_delete_on_get_super_user(client, super_user, source):
    client.force_login(super_user)
    initial_count = Source.objects.count()
    source_delete_url = reverse('currency:source-delete', args=(source.id,))
    response = client.post(source_delete_url)
    checks = (
        response.status_code == 302,
        response['location'] == source_list_url,
        Source.objects.count() == initial_count - 1
    )
    assert all(checks)


# User logo_url property and signals tests
def test_source_logo_url_property_on_default_value(client, source):
    assert source.logo_url == static('images/source_logo_default.png')


def test_source_logo_url_property_on_uploaded_image(client, source_with_logo):
    # Since there is actually passed an image to ImageField there will be:
    # - created a dir in corresponding MEDIA_URL, so upload_to property of model and
    #   related functions form utils.common are tested as well
    # - to delete dir source.delete method is called which invoke post_delete signal
    #   and related functions from utils.common, so these are tested too
    source, logo = source_with_logo
    checks = (
        source.logo_url == settings.MEDIA_URL + get_upload_to_path(source,
                                                                   StorageUniqueFields.source,
                                                                   logo
                                                                   ),
        source.delete() == (
            # number of instances deleted
            1,
            # detailed info about what was deleted
            {'currency.Source': 1}
        )
    )
    assert all(checks)


def test_source_logo_url_property_on_uploaded_image_(client, source):
    # In celery beat parsers predefined images from static dir are used:
    # This test ensures that those are served properly
    logo_url = static('images/source_monobank_logo.png')
    source.logo = logo_url
    checks = (
        source.logo_url == logo_url,
        source.delete() == (
            # number of instances deleted
            1,
            # detailed info about what was deleted
            {'currency.Source': 1}
        )
    )
    assert all(checks)
