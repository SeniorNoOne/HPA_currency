from django.conf import settings
from django.templatetags.static import static
from django.urls import reverse

from account.models import User
from account.constants import StorageUniqueFields
from utils.common import get_upload_to_path


# Singup form test
def test_singup_form_status_code_on_get_request(client):
    response = client.get(reverse('account:signup'))
    assert response.status_code == 200


def test_signup_form_status_code_on_empty_submission(client):
    payload = {}
    response = client.post(reverse('account:signup'), data=payload)
    assert response.status_code == 200


def test_signup_form_errors_on_empty_submission(client):
    payload = {}
    response = client.post(reverse('account:signup'), data=payload)
    assert response.context_data['form']._errors == {
        'email': ['This field is required.'],
        'password1': ['This field is required.'],
        'password2': ['This field is required.']
    }


def test_signup_form_status_code_on_wrong_email_field(client, user_data):
    payload = {
        'email': 'WRONG_EMAIL',
        'password1': user_data.password,
        'password2': user_data.password
    }
    response = client.post(reverse('account:signup'), data=payload)
    assert response.status_code == 200


def test_signup_form_errors_on_wrong_email_field(client, user_data):
    payload = {
        'email': 'WRONG_EMAIL',
        'password1': user_data.password,
        'password2': user_data.password
    }
    response = client.post(reverse('account:signup'), data=payload)
    assert response.context_data['form']._errors == {
        'email': ['Enter a valid email address.']
    }


def test_signup_form_status_code_on_wrong_password1_field(client, user_data):
    payload = {
        'email': user_data.email,
        'password1': '_',
        'password2': user_data.password
    }
    response = client.post(reverse('account:signup'), data=payload)
    assert response.status_code == 200


def test_signup_form_errors_on_wrong_password1_field(client, user_data):
    payload = {
        'email': user_data.email,
        'password1': '_',
        'password2': user_data.password
    }
    response = client.post(reverse('account:signup'), data=payload)
    assert response.context_data['form']._errors == {
        'password1': ['Passwords should match!'],
        'password2': ['Passwords should match!']
    }


def test_signup_form_status_code_on_wrong_password2_field(client, user_data):
    payload = {
        'email': user_data.email,
        'password1': user_data.password,
        'password2': '_'
    }
    response = client.post(reverse('account:signup'), data=payload)
    assert response.status_code == 200


def test_signup_form_errors_on_wrong_password2_field(client, user_data):
    payload = {
        'email': user_data.email,
        'password1': user_data.password,
        'password2': '_'
    }
    response = client.post(reverse('account:signup'), data=payload)
    assert response.context_data['form']._errors == {
        'password1': ['Passwords should match!'],
        'password2': ['Passwords should match!']
    }


def test_signup_form_status_code_on_same_invalid_passwords(client, user_data):
    payload = {
        'email': user_data.email,
        'password1': '_',
        'password2': '_'
    }
    response = client.post(reverse('account:signup'), data=payload)
    assert response.status_code == 200


def test_signup_form_errors_on_same_invalid_passwords(client, user_data):
    payload = {
        'email': user_data.email,
        'password1': '_',
        'password2': '_'
    }
    response = client.post(reverse('account:signup'), data=payload)
    assert response.context_data['form']._errors == {
        '__all__': ['This password is too short. It must contain at least 8 characters.']
    }


def test_signup_form_status_code_on_existing_user(client, user):
    payload = {
        'email': user.email,
        'password1': user.password,
        'password2': user.password
    }
    response = client.post(reverse('account:signup'), data=payload)
    assert response.status_code == 200


def test_signup_form_errors_on_existing_user(client, user):
    payload = {
        'email': user.email,
        'password1': user.password,
        'password2': user.password
    }
    response = client.post(reverse('account:signup'), data=payload)
    assert response.context_data['form']._errors == {
        'email': ['Email is already in use!']
    }


def test_signup_form_on_valid_submission(client, user_data):
    payload = {
        'email': user_data.email,
        'password1': user_data.password,
        'password2': user_data.password
    }
    initial_count = User.objects.count()
    response = client.post(reverse('account:signup'), data=payload)
    checks = (
        response.status_code == 302,
        response['location'] == reverse('index'),
        User.objects.count() == initial_count + 1
    )
    assert all(checks)


def test_send_email_signal_on_signup(client, user_data, mailoutbox):
    payload = {
        'email': user_data.email,
        'password1': user_data.password,
        'password2': user_data.password
    }
    response = client.post(reverse('account:signup'), data=payload)
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
def test_login_form_status_code_on_get_request(client):
    response = client.get(reverse('login'))
    assert response.status_code == 200


def test_login_form_status_code_on_empty_submission(client):
    payload = {}
    response = client.post(reverse('login'), data=payload)
    assert response.status_code == 200


def test_login_form_errors_on_empty_submission(client):
    payload = {}
    response = client.post(reverse('login'), data=payload)
    assert response.context_data['form']._errors == {
        'username': ['This field is required.'],
        'password': ['This field is required.']
    }


def test_login_form_status_code_on_wrong_username(client, active_user):
    payload = {
        'username': 'WRONG_USERNAME',
        'password': active_user.password
    }
    response = client.post(reverse('login'), data=payload)
    assert response.status_code == 200


def test_login_form_errors_on_wrong_username(client, active_user):
    payload = {
        'username': 'WRONG_USERNAME',
        'password': active_user.password
    }
    response = client.post(reverse('login'), data=payload)
    assert response.context_data['form']._errors == {
        '__all__': ['Please enter a correct email and password. '
                    'Note that both fields may be case-sensitive.']
    }


def test_login_form_status_code_on_wrong_password(client, active_user):
    payload = {
        'username': active_user.email,
        'password': '_'
    }
    response = client.post(reverse('login'), data=payload)
    assert response.status_code == 200


def test_login_form_errors_on_wrong_password(client, active_user):
    payload = {
        'username': active_user.email,
        'password': '_'
    }
    response = client.post(reverse('login'), data=payload)
    assert response.context_data['form']._errors == {
        '__all__': ['Please enter a correct email and password. '
                    'Note that both fields may be case-sensitive.']
    }


def test_login_form_on_valid_submission(client, active_user_with_hashed_password):
    payload = {
        'username': active_user_with_hashed_password.email,
        'password': active_user_with_hashed_password.raw_password
    }
    response = client.post(reverse('login'), data=payload)
    checks = (
        response['location'] == reverse('index'),
        response.status_code == 302
    )
    assert all(checks)


# User avatar_url property and signals tests
def test_avatar_url_property_on_default_value(client, user):
    assert user.avatar_url == static('images/account_avatar_default.png')


def test_avatar_url_property_on_uploaded_image(client, active_user_with_avatar):
    # Since there is actually passed an image to ImageField there will be:
    # - created a dir in corresponding MEDIA_URL, so upload_to property of model and
    #   related functions form utils.common will be tested as well
    # - to delete dir user.delete method is called which will invoke post_delete signal
    #   and related functions from utils.common, so these will be tested too
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


def test_clean_phone_field_signal(client, active_user):
    phone = '380 10 200 30 40'
    active_user.phone = phone
    active_user.save()
    assert active_user.phone == phone.replace(' ', '')


def test_activation_url(client, user):
    initial_user_state = user.is_active
    activate_url = reverse('account:activate', args=(user.username,))
    response = client.get(activate_url)
    user.refresh_from_db()
    checks = (
        initial_user_state is False,
        response.status_code == 302,
        response['location'] == reverse('login'),
        user.is_active is True
    )
    assert all(checks)


# Profile form tests
def test_profile_form_on_inactive_user_login(client, user):
    client.force_login(user)
    response = client.get(reverse('account:profile'))
    checks = (
        response.status_code == 302,
        response['location'] == reverse('login') + '?next=' + reverse('account:profile')
    )
    assert all(checks)


def test_profile_form_status_code_on_active_user_login(client, active_user):
    client.force_login(active_user)
    response = client.get(reverse('account:profile'))
    assert response.status_code == 200


def test_profile_form_on_first_name_update(client, user_data, active_user):
    client.force_login(active_user)
    payload = {
        'first_name': user_data.first_name
    }
    response = client.post(reverse('account:profile'), data=payload)
    active_user.refresh_from_db()
    checks = (
        response.status_code == 302,
        response['location'] == reverse('index'),
        active_user.first_name == user_data.first_name
    )
    assert all(checks)


def test_profile_form_on_last_name_update(client, user_data, active_user):
    client.force_login(active_user)
    response = client.post(reverse('account:profile'), data={'last_name': user_data.last_name})
    active_user.refresh_from_db()
    checks = (
        response.status_code == 302,
        response['location'] == reverse('index'),
        active_user.last_name == user_data.last_name
    )
    assert all(checks)


def test_profile_form_on_avatar_update(client, active_user, active_user_with_avatar):
    client.force_login(active_user)
    user, avatar = active_user_with_avatar
    payload = {
        'avatar': user.avatar.read()
    }
    response = client.post(reverse('account:profile'), data=payload)
    active_user.refresh_from_db()
    checks = (
        response.status_code == 302,
        response['location'] == reverse('index'),
        active_user.last_name == user.last_name
    )
    # removing created files
    active_user.delete()
    assert all(checks)
