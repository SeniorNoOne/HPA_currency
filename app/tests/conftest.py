import pytest
import tempfile
import uuid
from random import choice, randint

from django.conf import settings
from django.contrib.auth.hashers import make_password
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.cache import cache

from model_bakery import baker
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import AccessToken

from currency.choices import RateCurrencyChoices
from currency.constants import LATEST_RATE_CACHE_KEY
from tests.fixtures import parser_data


@pytest.fixture(autouse=True, scope='function')
def enable_db_access_for_all_tests(db):
    yield


@pytest.fixture(scope='function')
def api_client():
    client = APIClient()
    yield client


@pytest.fixture(scope='function')
def api_client_authorized(api_client, active_user):
    token = AccessToken.for_user(active_user)
    api_client.force_authenticate(user=active_user, token=token)
    yield api_client


@pytest.fixture(scope='function')
def api_throttling_rate():
    yield settings.THROTTLING_RATE


@pytest.fixture(scope='function')
def source(db):
    source = baker.make('currency.Source')
    yield source


@pytest.fixture(scope='function')
def sources(db):
    sources = baker.make('currency.Source', _quantity=5)
    yield sources


@pytest.fixture(scope='module')
def currency():
    yield choice(RateCurrencyChoices.values)


@pytest.fixture(scope='module')
def invalid_currency():
    while True:
        currency = randint(0, 2 ** 15 - 1)
        if currency not in RateCurrencyChoices.values:
            break
    yield currency


@pytest.fixture(scope='function')
def rate(db):
    rate = baker.make('currency.Rate')
    yield rate


@pytest.fixture(scope='function')
def rate_data(db):
    rate = baker.prepare('currency.Rate')
    yield rate


@pytest.fixture(scope='function')
def rates(db):
    rates = baker.make('currency.Rate', _quantity=10)
    yield rates


@pytest.fixture(scope='function')
def user_data(db):
    user = baker.prepare('account.User', _fill_optional=('first_name', 'last_name'))
    user.is_active = False
    yield user


@pytest.fixture(scope='function')
def user(db):
    username = uuid.uuid4()
    user = baker.make('account.User', username=username)
    user.is_active = False
    user.save()
    yield user


@pytest.fixture(scope='function')
def active_user(user):
    user.is_active = True
    user.save()
    yield user


@pytest.fixture(scope='function')
def active_user_hashed_password(active_user):
    raw_password = active_user.password
    active_user.password = make_password(raw_password)
    active_user.raw_password = raw_password
    active_user.save()
    yield active_user


@pytest.fixture(scope='function')
def active_user_with_avatar(active_user):
    with tempfile.NamedTemporaryFile(suffix='.png') as temp_file:
        avatar = SimpleUploadedFile(temp_file.name, b'random_image_content')
        active_user.avatar = avatar
        active_user.save()
    yield active_user, avatar.name


@pytest.fixture(scope='function')
def super_user(active_user):
    active_user.is_superuser = True
    active_user.save()
    yield active_user


@pytest.fixture(scope='function')
def contact_us():
    contact_us = baker.make('currency.ContactUs')
    yield contact_us


@pytest.fixture(scope='function')
def contact_us_multiple():
    contact_us = baker.make('currency.ContactUs', _quantity=10)
    yield contact_us


@pytest.fixture()
def privatbank_parser_data():
    yield parser_data.privat_data


@pytest.fixture()
def monobank_parser_data():
    yield parser_data.mono_data


@pytest.fixture()
def nbu_parser_data():
    with open(str(settings.BASE_DIR) + '/tests/fixtures/nbu_response_content', 'rb') as f:
        content = f.read()
    yield content


@pytest.fixture(scope='function')
def rate_caching():
    yield cache, LATEST_RATE_CACHE_KEY
