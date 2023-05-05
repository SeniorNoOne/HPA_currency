import pytest
from model_bakery import baker
from random import choice, randint
from rest_framework.test import APIClient

from currency.choices import RateCurrencyChoices


@pytest.fixture(autouse=True, scope='function')
def enable_db_access_for_all_tests(db):
    yield


@pytest.fixture(scope='function')
def api_client():
    client = APIClient()
    yield client


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
def rates(db):
    rates = baker.make('currency.Rate', _quantity=10)
    yield rates


@pytest.fixture(scope='function')
def user(db):
    user = baker.make('account.User')
    user.is_active = False
    user.save()
    yield user


@pytest.fixture(scope='function')
def active_user(user):
    user.is_active = True
    user.save()
    yield user


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
