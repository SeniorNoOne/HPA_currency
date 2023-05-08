from currency.models import Rate
from currency.tasks import parse_privatbank, parse_monobank, parse_nbu


def test_privatbank_parser_empty_db(mocker, privatbank_parser_data, monkeypatch):
    initial_count = Rate.objects.all().count()
    mocker.patch(
        'currency.tasks.get_response',
        return_value=privatbank_parser_data
    )
    parse_privatbank()
    assert Rate.objects.all().count() == initial_count + 2


def test_privatbank_parser_two_runs(mocker, privatbank_parser_data):
    initial_count = Rate.objects.all().count()
    mocker.patch(
        'currency.tasks.get_response',
        return_value=privatbank_parser_data
    )
    parse_privatbank()
    parse_privatbank()
    assert Rate.objects.all().count() == initial_count + 2


def test_monobank_parser_empty_db(mocker, monobank_parser_data):
    initial_count = Rate.objects.all().count()
    mocker.patch(
        'currency.tasks.get_response',
        return_value=monobank_parser_data
    )
    parse_monobank()
    assert Rate.objects.all().count() == initial_count + 4


def test_monobank_parser_two_runs(mocker, monobank_parser_data):
    initial_count = Rate.objects.all().count()
    mocker.patch(
        'currency.tasks.get_response',
        return_value=monobank_parser_data
    )
    parse_monobank()
    parse_monobank()
    assert Rate.objects.all().count() == initial_count + 4


def test_nbu_parser_empty_db(mocker, nbu_parser_data):
    initial_count = Rate.objects.all().count()
    mocker.patch(
        'currency.tasks.get_response',
        return_value=nbu_parser_data
    )
    parse_nbu()
    assert Rate.objects.all().count() == initial_count + 4


def test_nbu_parser_empty_two_runs(mocker, nbu_parser_data):
    initial_count = Rate.objects.all().count()
    mocker.patch(
        'currency.tasks.get_response',
        return_value=nbu_parser_data
    )
    parse_nbu()
    parse_nbu()
    assert Rate.objects.all().count() == initial_count + 4
