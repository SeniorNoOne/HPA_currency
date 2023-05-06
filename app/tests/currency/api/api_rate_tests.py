# LIST GET
def test_get_rate_list_status_200(api_client):
    response = api_client.get('/api/currency/rates/')
    assert response.status_code == 200


def test_get_rate_list_empty_db(api_client):
    response = api_client.get('/api/currency/rates/')
    assert len(response.json()['results']) == 0


def test_get_rate_list_single_entity(api_client, rate):
    response = api_client.get('/api/currency/rates/')
    assert len(response.json()['results']) == 1


def test_get_rate_list_multiple_entities(api_client, rates):
    response = api_client.get('/api/currency/rates/')
    assert len(response.json()['results']) == len(rates)


def test_get_rate_list_pagination(api_client, rates):
    response = api_client.get('/api/currency/rates/')
    json = response.json()
    checks = {
        'count' in json,
        'next' in json,
        'previous' in json
    }
    assert all(checks)


# LIST POST
def test_post_rate_list_empty_payload_status_400(api_client):
    payload = {}
    response = api_client.post('/api/currency/rates/', data=payload)
    assert response.status_code == 400


def test_post_rate_list_empty_payload_errors(api_client):
    payload = {}
    response = api_client.post('/api/currency/rates/', data=payload)
    assert response.json() == {
        'buy': ['This field is required.'],
        'sell': ['This field is required.'],
        'source': ['This field is required.']
    }


def test_post_rate_list_invalid_buy_status_400(api_client, source, rate, currency):
    payload = {
        'buy': '',
        'sell': rate.sell,
        'currency': currency,
        'source': source.id
    }
    response = api_client.post('/api/currency/rates/', data=payload)
    assert response.status_code == 400


def test_post_rate_list_invalid_buy_errors(api_client, source, rate):
    payload = {
        'buy': '',
        'sell': rate.sell,
        'source': source.id
    }
    response = api_client.post('/api/currency/rates/', data=payload)
    assert response.json() == {'buy': ['A valid number is required.']}


def test_post_rate_list_empty_buy_status_400(api_client, source, rate):
    payload = {
        'sell': rate.sell,
        'source': source.id
    }
    response = api_client.post('/api/currency/rates/', data=payload)
    assert response.status_code == 400


def test_post_rate_list_empty_buy_errors(api_client, source, rate):
    payload = {
        'sell': rate.sell,
        'source': source.id
    }
    response = api_client.post('/api/currency/rates/', data=payload)
    assert response.json() == {'buy': ['This field is required.']}


def test_post_rate_list_invalid_sell_status_400(api_client, source, rate):
    payload = {
        'buy': rate.buy,
        'sell': '',
        'source': source.id
    }
    response = api_client.post('/api/currency/rates/', data=payload)
    assert response.status_code == 400


def test_post_rate_list_invalid_sell_errors(api_client, source, rate):
    payload = {
        'buy': rate.buy,
        'sell': '',
        'source': source.id
    }
    response = api_client.post('/api/currency/rates/', data=payload)
    assert response.json() == {'sell': ['A valid number is required.']}


def test_post_rate_list_empty_sell_status_400(api_client, source, rate):
    payload = {
        'buy': rate.buy,
        'source': source.id
    }
    response = api_client.post('/api/currency/rates/', data=payload)
    assert response.status_code == 400


def test_post_rate_list_empty_sell_errors(api_client, source, rate):
    payload = {
        'buy': rate.buy,
        'source': source.id
    }
    response = api_client.post('/api/currency/rates/', data=payload)
    assert response.json() == {'sell': ['This field is required.']}


def test_post_rate_list_invalid_source_status_400(api_client, source, rate):
    payload = {
        'buy': rate.buy,
        'sell': rate.sell,
        'source': ''
    }
    response = api_client.post('/api/currency/rates/', data=payload)
    assert response.status_code == 400


def test_post_rate_list_invalid_source_errors(api_client, source, rate):
    payload = {
        'buy': rate.buy,
        'sell': rate.sell,
        'source': ''
    }
    response = api_client.post('/api/currency/rates/', data=payload)
    assert response.json() == {'source': ['This field may not be null.']}


def test_post_rate_list_empty_source_status_400(api_client, source, rate):
    payload = {
        'buy': rate.buy,
        'sell': rate.sell,
    }
    response = api_client.post('/api/currency/rates/', data=payload)
    assert response.status_code == 400


def test_post_rate_list_empty_source_errors(api_client, source, rate):
    payload = {
        'buy': rate.buy,
        'sell': rate.sell,
    }
    response = api_client.post('/api/currency/rates/', data=payload)
    assert response.json() == {'source': ['This field is required.']}


def test_post_rate_list_valid_data_status_200(api_client, source, rate):
    payload = {
        'buy': rate.buy,
        'sell': rate.sell,
        'source': source.id
    }
    response = api_client.post('/api/currency/rates/', data=payload)
    assert response.status_code == 201


def test_post_rate_list_valid_data_return_obj(api_client, source, rate):
    payload = {
        'buy': str(rate.buy),
        'sell': str(rate.sell),
        'source': source.id
    }
    response = api_client.post('/api/currency/rates/', data=payload)
    json = response.json()
    json['created'] = json['created'][:-11]
    payload['id'] = rate.id + 1
    payload['created'] = rate.created.strftime("%Y-%m-%dT%H:%M")
    assert json == payload


# DETAILS GET
def test_get_rate_details_status_200(api_client, rate):
    response = api_client.get(f'/api/currency/rates/{rate.id}/')
    assert response.status_code == 200


def test_get_rate_details_status_404(api_client):
    response = api_client.get(f'/api/currency/rates/{-1}/')
    assert response.status_code == 404


# Really strange behaviour for test_get_rate_details_data(api_client, source, rate)
def test_get_rate_details_data(api_client, rate):
    response = api_client.get(f'/api/currency/rates/{rate.id}/')
    json = response.json()
    json['created'] = json['created'][:-11]
    assert json == {
        'id': rate.id,
        'buy': str(rate.buy),
        'sell': str(rate.sell),
        'created': rate.created.strftime("%Y-%m-%dT%H:%M"),
        'source': 1
    }


# DETAILS PUT
def test_put_rate_details_same_rate_status_200(api_client, rate):
    payload = {
        'id': rate.id,
        'buy': str(rate.buy),
        'sell': str(rate.sell),
        'source': rate.source.id
    }
    response = api_client.put(f'/api/currency/rates/{rate.id}/', data=payload)
    assert response.status_code == 200


def test_put_rate_details_same_rate_data(api_client, rate):
    payload = {
        'id': rate.id,
        'buy': str(rate.buy),
        'sell': str(rate.sell),
        'source': rate.source.id
    }
    response = api_client.put(f'/api/currency/rates/{rate.id}/', data=payload)
    json = response.json()
    json['created'] = json['created'][:-11]
    payload['created'] = rate.created.strftime("%Y-%m-%dT%H:%M")
    assert json == payload


def test_put_rate_details_empty_payload_status_400(api_client, rate):
    payload = {}
    response = api_client.put(f'/api/currency/rates/{rate.id}/', data=payload)
    assert response.status_code == 400


def test_put_rate_details_empty_payload_data(api_client, rate):
    payload = {}
    response = api_client.put(f'/api/currency/rates/{rate.id}/', data=payload)
    assert response.json() == {
        'buy': ['This field is required.'],
        'sell': ['This field is required.'],
        'source': ['This field is required.']
    }


def test_put_rate_details_alter_buy_status_200(api_client, rate):
    payload = {
        'id': rate.id,
        'buy': str(rate.buy + 1),
        'sell': str(rate.sell),
        'source': rate.source.id
    }
    response = api_client.put(f'/api/currency/rates/{rate.id}/', data=payload)
    assert response.status_code == 200


def test_put_rate_details_alter_buy_data(api_client, rate):
    payload = {
        'id': rate.id,
        'buy': str(rate.buy + 1),
        'sell': str(rate.sell),
        'source': rate.source.id
    }
    response = api_client.put(f'/api/currency/rates/{rate.id}/', data=payload)
    json = response.json()
    json['created'] = json['created'][:-11]
    payload['created'] = rate.created.strftime("%Y-%m-%dT%H:%M")
    assert response.json() == payload


def test_put_rate_details_alter_sell_status_200(api_client, rate):
    payload = {
        'id': rate.id,
        'buy': str(rate.buy),
        'sell': str(rate.sell + 1),
        'source': rate.source.id
    }
    response = api_client.put(f'/api/currency/rates/{rate.id}/', data=payload)
    assert response.status_code == 200


def test_put_rate_details_alter_sell_data(api_client, rate):
    payload = {
        'id': rate.id,
        'buy': str(rate.buy),
        'sell': str(rate.sell + 1),
        'source': rate.source.id
    }
    response = api_client.put(f'/api/currency/rates/{rate.id}/', data=payload)
    json = response.json()
    json['created'] = json['created'][:-11]
    payload['created'] = rate.created.strftime("%Y-%m-%dT%H:%M")
    assert response.json() == payload


def test_put_rate_details_alter_source_status_200(api_client, source, rate):
    payload = {
        'id': rate.id,
        'buy': str(rate.buy),
        'sell': str(rate.sell),
        'source': source.id
    }
    response = api_client.put(f'/api/currency/rates/{rate.id}/', data=payload)
    assert response.status_code == 200


def test_put_rate_details_alter_source_data(api_client, source, rate):
    payload = {
        'id': rate.id,
        'buy': str(rate.buy),
        'sell': str(rate.sell),
        'source': source.id
    }
    response = api_client.put(f'/api/currency/rates/{rate.id}/', data=payload)
    json = response.json()
    json['created'] = json['created'][:-11]
    payload['created'] = rate.created.strftime("%Y-%m-%dT%H:%M")
    assert response.json() == payload


# DETAILS DELETE
def test_delete_rate_details_status_204(api_client, rate):
    response = api_client.delete(f'/api/currency/rates/{rate.id}/')
    assert response.status_code == 204
