from django.urls import reverse

from currency.models import RequestResponseLog

api_req_resp_log_list_url = reverse('api-currency:logs-list')


# LIST GET
def test_api_req_resp_log_list_status_code_on_get_no_auth(api_client):
    response = api_client.get(api_req_resp_log_list_url)
    assert response.status_code == 401


def test_api_req_resp_log_list_errors_on_get_no_auth(api_client):
    response = api_client.get(api_req_resp_log_list_url)
    assert response.json() == {
        'detail': 'Authentication credentials were not provided.'
    }


def test_api_req_resp_log_list_status_code_on_get(api_client_authorized):
    response = api_client_authorized.get(api_req_resp_log_list_url)
    assert response.status_code == 200


def test_api_req_resp_log_list_on_get_with_empty_db(api_client_authorized):
    response = api_client_authorized.get(api_req_resp_log_list_url)
    assert len(response.json()['results']) == 0


def test_api_req_resp_log_list_on_get_with_one_record(api_client_authorized, req_resp_log):
    response = api_client_authorized.get(api_req_resp_log_list_url)
    assert len(response.json()['results']) == 1


def test_api_req_resp_log_list_on_get_with_multiple_records(api_client_authorized, req_resp_logs):
    response = api_client_authorized.get(api_req_resp_log_list_url)
    assert len(response.json()['results']) == len(req_resp_logs)


def test_api_req_resp_log_list_pagination_on_get(api_client_authorized, req_resp_logs):
    response = api_client_authorized.get(api_req_resp_log_list_url)
    data = response.json()
    checks = {
        'count' in data,
        'next' in data,
        'previous' in data
    }
    assert all(checks)


# LIST POST
def test_api_req_resp_log_list_status_code_on_post_no_auth_empty_submission(api_client):
    payload = {}
    response = api_client.post(api_req_resp_log_list_url, data=payload)
    assert response.status_code == 401


def test_api_req_resp_log_list_errors_on_post_no_auth_empty_submission(api_client):
    payload = {}
    response = api_client.post(api_req_resp_log_list_url, data=payload)
    assert response.json() == {
        'detail': 'Authentication credentials were not provided.'
    }


def test_api_req_resp_log_list_status_code_on_post_empty_submission(api_client_authorized):
    payload = {}
    response = api_client_authorized.post(api_req_resp_log_list_url, data=payload)
    assert response.status_code == 405


def test_api_req_resp_log_list_errors_on_post_empty_submission(api_client_authorized):
    payload = {}
    response = api_client_authorized.post(api_req_resp_log_list_url, data=payload)
    assert response.json() == {
        'detail': 'Method \"POST\" not allowed.'
    }


# LIST PUT
def test_api_req_resp_log_list_status_code_on_put_no_auth(api_client):
    response = api_client.put(api_req_resp_log_list_url)
    assert response.status_code == 401


def test_api_req_resp_log_list_errors_on_put_no_auth(api_client):
    response = api_client.put(api_req_resp_log_list_url)
    assert response.json() == {
        'detail': 'Authentication credentials were not provided.'
    }


def test_api_req_resp_log_list_status_code_on_put(api_client_authorized):
    response = api_client_authorized.put(api_req_resp_log_list_url)
    assert response.status_code == 405


def test_api_req_resp_log_list_errors_on_put(api_client_authorized):
    response = api_client_authorized.put(api_req_resp_log_list_url)
    assert response.json() == {
        'detail': 'Method \"PUT\" not allowed.'
    }


# LIST DELETE
def test_api_req_resp_log_list_status_code_on_delete_no_auth(api_client):
    response = api_client.delete(api_req_resp_log_list_url)
    assert response.status_code == 401


def test_api_req_resp_log_list_errors_on_delete_no_auth(api_client):
    response = api_client.delete(api_req_resp_log_list_url)
    assert response.json() == {
        'detail': 'Authentication credentials were not provided.'
    }


def test_api_req_resp_log_list_status_code_on_delete(api_client_authorized):
    response = api_client_authorized.delete(api_req_resp_log_list_url)
    assert response.status_code == 405


def test_api_req_resp_log_list_errors_on_delete(api_client_authorized):
    response = api_client_authorized.delete(api_req_resp_log_list_url)
    assert response.json() == {
        'detail': 'Method \"DELETE\" not allowed.'
    }


# DETAILS GET
def test_api_req_resp_log_details_status_code_on_get_no_auth(api_client, req_resp_log):
    response = api_client.get(api_req_resp_log_list_url + f'{req_resp_log.id}/')
    assert response.status_code == 401


def test_api_req_resp_log_details_errors_on_get_no_auth(api_client, req_resp_log):
    response = api_client.get(api_req_resp_log_list_url + f'{req_resp_log.id}/')
    assert response.json() == {
        'detail': 'Authentication credentials were not provided.'
    }


def test_api_req_resp_log_details_status_code_on_get(api_client_authorized, req_resp_log):
    response = api_client_authorized.get(api_req_resp_log_list_url + f'{req_resp_log.id}/')
    assert response.status_code == 200


def test_api_req_resp_log_details_return_obj_on_get(api_client_authorized, req_resp_log):
    response = api_client_authorized.get(api_req_resp_log_list_url + f'{req_resp_log.id}/')
    assert response.json() == {
        'path': req_resp_log.path,
        'request_method': req_resp_log.request_method,
        'time': req_resp_log.time
    }


# DETAILS PUT
def test_api_req_resp_log_details_status_code_on_put_no_auth(api_client, req_resp_log):
    response = api_client.put(api_req_resp_log_list_url + f'{req_resp_log.id}/')
    assert response.status_code == 401


def test_api_req_resp_log_details_errors_on_put_no_auth(api_client, req_resp_log):
    response = api_client.put(api_req_resp_log_list_url + f'{req_resp_log.id}/')
    assert response.json() == {
        'detail': 'Authentication credentials were not provided.'
    }


def test_api_req_resp_log_details_status_code_on_put(api_client_authorized, req_resp_log):
    response = api_client_authorized.put(api_req_resp_log_list_url + f'{req_resp_log.id}/')
    assert response.status_code == 405


def test_api_req_resp_log_details_errors_on_put(api_client_authorized, req_resp_log):
    response = api_client_authorized.put(api_req_resp_log_list_url + f'{req_resp_log.id}/')
    assert response.json() == {
        'detail': 'Method \"PUT\" not allowed.'
    }


# DETAILS DELETE
def test_api_req_resp_log_details_status_code_on_delete_no_auth(api_client, req_resp_log):
    response = api_client.delete(api_req_resp_log_list_url + f'{req_resp_log.id}/')
    assert response.status_code == 401


def test_api_req_resp_log_details_errors_on_delete_no_auth(api_client, req_resp_log):
    response = api_client.delete(api_req_resp_log_list_url + f'{req_resp_log.id}/')
    assert response.json() == {
        'detail': 'Authentication credentials were not provided.'
    }


def test_api_req_resp_log_details_status_code_on_delete(api_client_authorized, req_resp_log):
    response = api_client_authorized.delete(api_req_resp_log_list_url + f'{req_resp_log.id}/')
    assert response.status_code == 204


def test_api_req_resp_log_details_obj_count_on_delete(api_client_authorized, req_resp_log):
    initial_count = RequestResponseLog.objects.count()
    api_client_authorized.delete(api_req_resp_log_list_url + f'{req_resp_log.id}/')
    checks = (
        # Deleting log creates another log instance, so counter does not change
        RequestResponseLog.objects.count() == initial_count,
        RequestResponseLog.objects.last().id != req_resp_log.id
    )
    assert all(checks)
