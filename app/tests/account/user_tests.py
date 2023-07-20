from django.conf import settings
from django.templatetags.static import static
from django.urls import reverse

from account.models import User
from account.constants import StorageUniqueFields
from utils.common import get_upload_to_path

user_signup_url = reverse('account:signup')
user_login_url = reverse('login')
user_profile_url = reverse('account:profile')


# Singup form test
def test_user_singup_form_status_code_on_get(client):
    response = client.get(user_signup_url)
    assert response.status_code == 200


def test_user_signup_form_status_code_on_post_empty_submission(client):
    payload = {}
    response = client.post(user_signup_url, data=payload)
    assert response.status_code == 200


def test_user_signup_form_errors_on_post_empty_submission(client):
    payload = {}
    response = client.post(user_signup_url, data=payload)
    assert response.context_data['form']._errors == {
        'email': ['This field is required.'],
        'password1': ['This field is required.'],
        'password2': ['This field is required.']
    }


def test_user_signup_form_status_code_on_post_wrong_email_field(client, user_data):
    payload = {
        'email': 'WRONG_EMAIL',
        'password1': user_data.password,
        'password2': user_data.password
    }
    response = client.post(user_signup_url, data=payload)
    assert response.status_code == 200


def test_user_signup_form_errors_on_post_wrong_email_field(client, user_data):
    payload = {
        'email': 'WRONG_EMAIL',
        'password1': user_data.password,
        'password2': user_data.password
    }
    response = client.post(user_signup_url, data=payload)
    assert response.context_data['form']._errors == {
        'email': ['Enter a valid email address.']
    }


def test_user_signup_form_status_code_on_post_wrong_password1_field(client, user_data):
    payload = {
        'email': user_data.email,
        'password1': '_',
        'password2': user_data.password
    }
    response = client.post(user_signup_url, data=payload)
    assert response.status_code == 200


def test_user_signup_form_errors_on_post_wrong_password1_field(client, user_data):
    payload = {
        'email': user_data.email,
        'password1': '_',
        'password2': user_data.password
    }
    response = client.post(user_signup_url, data=payload)
    assert response.context_data['form']._errors == {
        'password1': ['Passwords should match!'],
        'password2': ['Passwords should match!']
    }


def test_user_signup_form_status_code_on_post_wrong_password2_field(client, user_data):
    payload = {
        'email': user_data.email,
        'password1': user_data.password,
        'password2': '_'
    }
    response = client.post(user_signup_url, data=payload)
    assert response.status_code == 200


def test_user_signup_form_errors_on_post_wrong_password2_field(client, user_data):
    payload = {
        'email': user_data.email,
        'password1': user_data.password,
        'password2': '_'
    }
    response = client.post(user_signup_url, data=payload)
    assert response.context_data['form']._errors == {
        'password1': ['Passwords should match!'],
        'password2': ['Passwords should match!']
    }


def test_user_signup_form_status_code_on_post_same_invalid_passwords(client, user_data):
    payload = {
        'email': user_data.email,
        'password1': '_',
        'password2': '_'
    }
    response = client.post(user_signup_url, data=payload)
    assert response.status_code == 200


def test_user_signup_form_errors_on_post_same_invalid_passwords(client, user_data):
    payload = {
        'email': user_data.email,
        'password1': '_',
        'password2': '_'
    }
    response = client.post(user_signup_url, data=payload)
    assert response.context_data['form']._errors == {
        '__all__': ['This password is too short. It must contain at least 8 characters.']
    }


def test_user_signup_form_status_code_on_post_existing_user(client, user):
    payload = {
        'email': user.email,
        'password1': user.password,
        'password2': user.password
    }
    response = client.post(user_signup_url, data=payload)
    assert response.status_code == 200


def test_user_signup_form_errors_on_post_existing_user(client, user):
    payload = {
        'email': user.email,
        'password1': user.password,
        'password2': user.password
    }
    response = client.post(user_signup_url, data=payload)
    assert response.context_data['form']._errors == {
        'email': ['Email is already in use!']
    }


def test_user_signup_form_on_post_valid_submission(client, user_data):
    payload = {
        'email': user_data.email,
        'password1': user_data.password,
        'password2': user_data.password
    }
    initial_count = User.objects.count()
    response = client.post(user_signup_url, data=payload)
    checks = (
        response.status_code == 302,
        response['location'] == reverse('index'),
        User.objects.count() == initial_count + 1
    )
    assert all(checks)


def test_user_send_email_signal_on_signup(client, user_data, mailoutbox):
    payload = {
        'email': user_data.email,
        'password1': user_data.password,
        'password2': user_data.password
    }
    response = client.post(user_signup_url, data=payload)
    email = mailoutbox[0]
    checks = (
        email.subject == 'Thank you for registration!',
        email.from_email == settings.DEFAULT_FROM_EMAIL,
        email.to == [user_data.email.lower()],
        response.status_code == 302,
        response['location'] == reverse('index')
    )
    assert all(checks)


# Login form tests
def test_user_login_form_status_code_on_get(client):
    response = client.get(user_login_url)
    assert response.status_code == 200


def test_user_login_form_status_code_on_post_empty_submission(client):
    payload = {}
    response = client.post(user_login_url, data=payload)
    assert response.status_code == 200


def test_user_login_form_errors_on_post_empty_submission(client):
    payload = {}
    response = client.post(user_login_url, data=payload)
    assert response.context_data['form']._errors == {
        'username': ['This field is required.'],
        'password': ['This field is required.']
    }


def test_user_login_form_status_code_on_post_wrong_username(client, active_user):
    payload = {
        'username': 'WRONG_USERNAME',
        'password': active_user.password
    }
    response = client.post(user_login_url, data=payload)
    assert response.status_code == 200


def test_user_login_form_errors_on_post_wrong_username(client, active_user):
    payload = {
        'username': 'WRONG_USERNAME',
        'password': active_user.password
    }
    response = client.post(user_login_url, data=payload)
    assert response.context_data['form']._errors == {
        'username': ['Enter a valid email address.']
    }


def test_user_login_form_status_code_on_post_wrong_password(client, active_user):
    payload = {
        'username': active_user.email,
        'password': '_'
    }
    response = client.post(user_login_url, data=payload)
    assert response.status_code == 200


def test_user_login_form_errors_on_post_wrong_password(client, active_user):
    payload = {
        'username': active_user.email,
        'password': '_'
    }
    response = client.post(user_login_url, data=payload)
    assert response.context_data['form']._errors == {
        '__all__': ['Please enter a correct email and password. '
                    'Note that both fields may be case-sensitive.']
    }


def test_user_login_form_on_post_valid_submission(client, active_user_hashed_password):
    payload = {
        'username': active_user_hashed_password.email,
        'password': active_user_hashed_password.raw_password
    }
    response = client.post(user_login_url, data=payload)
    checks = (
        response['location'] == reverse('index'),
        response.status_code == 302
    )
    assert all(checks)


# User avatar_url property and signals tests
def test_user_avatar_url_property_on_default_value(client, user):
    assert user.avatar_url == static('images/account_avatar_default.png')


def test_user_avatar_url_property_on_uploaded_image(client, active_user_with_avatar):
    # Since there is actually passed an image to ImageField there will be:
    # - created a dir in corresponding MEDIA_URL, so upload_to property of model and
    #   related functions form utils.common are tested as well
    # - to delete dir user.delete method is called which invoke post_delete signal
    #   and related functions from utils.common, so these are tested too
    user, avatar = active_user_with_avatar
    checks = (
        user.avatar_url == settings.MEDIA_URL + get_upload_to_path(user,
                                                                   StorageUniqueFields.user,
                                                                   avatar
                                                                   ),
        user.delete() == (
            # number of instances deleted
            1,
            # detailed info about what was deleted
            {'account.User': 1}
        )
    )
    assert all(checks)


def test_user_clean_phone_field_signal(client, active_user):
    phone = '380 10 200 30 40'
    active_user.phone = phone
    active_user.save()
    assert active_user.phone == phone.replace(' ', '')


def test_user_activation_url(client, user):
    initial_user_state = user.is_active
    activate_url = reverse('account:activate', args=(user.username,))
    response = client.get(activate_url)
    user.refresh_from_db()
    checks = (
        initial_user_state is False,
        response.status_code == 302,
        response['location'] == user_login_url,
        user.is_active is True
    )
    assert all(checks)


# Profile form tests
def test_user_profile_form_on_inactive_user_login(client, user):
    client.force_login(user)
    response = client.get(user_profile_url)
    checks = (
        response.status_code == 302,
        response['location'] == user_login_url + '?next=' + user_profile_url
    )
    assert all(checks)


def test_user_profile_form_status_code_on_active_user_login(client, active_user):
    client.force_login(active_user)
    response = client.get(user_profile_url)
    assert response.status_code == 200


def test_user_profile_form_on_first_name_update(client, user_data, active_user):
    client.force_login(active_user)
    payload = {
        'first_name': user_data.first_name
    }
    response = client.post(user_profile_url, data=payload)
    active_user.refresh_from_db()
    checks = (
        response.status_code == 302,
        response['location'] == reverse('index'),
        active_user.first_name == user_data.first_name
    )
    assert all(checks)


def test_user_profile_form_on_last_name_update(client, user_data, active_user):
    client.force_login(active_user)
    response = client.post(user_profile_url, data={'last_name': user_data.last_name})
    active_user.refresh_from_db()
    checks = (
        response.status_code == 302,
        response['location'] == reverse('index'),
        active_user.last_name == user_data.last_name
    )
    assert all(checks)


def test_user_profile_form_on_avatar_update(client, active_user, active_user_with_avatar):
    client.force_login(active_user)
    user, avatar = active_user_with_avatar
    payload = {
        'avatar': user.avatar.read()
    }
    response = client.post(user_profile_url, data=payload)
    active_user.refresh_from_db()
    checks = (
        response.status_code == 302,
        response['location'] == reverse('index'),
        active_user.last_name == user.last_name
    )
    # removing created files
    active_user.delete()
    assert all(checks)


def test_createsuperuser_command(monkeypatch, user_data):
    user_manager = User._default_manager
    superuser = user_manager.create_superuser(
        email=user_data.email,
        password='some_1_password',
        first_name=user_data.first_name,
        last_name=user_data.last_name
    )
    db_superuser = User.objects.get(email=user_data.email.lower())
    checks = (
        db_superuser.is_staff,
        db_superuser.is_active,
        db_superuser.is_superuser,
        db_superuser == superuser
    )
    assert all(checks)
