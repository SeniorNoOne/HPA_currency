from django.urls import reverse

req_resp_log_list_url = reverse('currency:log-list')


# List
def test_req_resp_log_list_status_code_on_get(client):
    response = client.get(req_resp_log_list_url)
    assert response.status_code == 200


def test_req_resp_log_list_on_get_with_empty_db(client):
    response = client.get(req_resp_log_list_url)
    assert not response.context_data['object_list'].exists()


def test_req_resp_log_list_on_get_with_one_record(client, req_resp_log):
    response = client.get(req_resp_log_list_url)
    assert response.context_data['object_list'].count() == 1


def test_req_resp_log_list_on_get_with_multiple_record(client, req_resp_logs):
    response = client.get(req_resp_log_list_url)
    assert response.context_data['object_list'].count() == len(req_resp_logs)


# List pagination tests
def test_req_resp_log_list_pagination_on_get(client, req_resp_logs):
    response = client.get(req_resp_log_list_url)
    context = response.context_data
    checks = (
        'is_paginated' in context,
        'page_obj' in context,
        'paginator' in context
    )
    assert all(checks)
