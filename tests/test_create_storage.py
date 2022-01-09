from flask import request, jsonify
from urllib.parse import urlparse
from datetime import datetime

def test_add_storage(client):
    new_storage_data = [
            {'name' : 'name', 'value' : 'box-A'},
            {'name' : 'location', 'value' : 'stage right'},
            {'name' : 'notes', 'value' : 'good!'}]

    response = client.post('/', json={'data' : new_storage_data})
    assert response.status_code == 201
    url =  response.headers['Location']
    assert urlparse(url).path == '/storage/1'

def test_none_error(client):

    new_storage_data = None
    response = client.post('/', json={'data' : new_storage_data})
    assert response.status_code == 400
    assert response.headers['error'] == 'Bad Request'
    assert response.headers['message'] == 'Null object was sent'

    response = client.post('/', json=None)
    assert response.status_code == 400
    assert response.headers['error'] == 'Bad Request'
    assert response.headers['message'] == 'Null object was sent'


def test_send_less_data(client):

    less_data = [{'name' : 'name', 'value' : 'box-A'}]
    response = client.post('/', json={'data' : less_data})
    assert response.status_code == 400
    assert response.headers['error'] == 'Bad Request'
    assert response.headers['message'] == 'Incorrect number of data items sent. Ensure that you use the template provided.'

def test_send_more_data(client):

    more_data = [
            {'name' : 'name', 'value' : 'box-A'},
            {'name' : 'location', 'value' : 'stage right'},
            {'name' : 'notes', 'value' : 'contains cables'},
            {'name' : 'date', 'value' : '01-01-2022'}]

    response = client.post('/', json={'data' : more_data})
    assert response.status_code == 400
    assert response.headers['error'] == 'Bad Request'
    assert response.headers['message'] == 'Incorrect number of data items sent. Ensure that you use the template provided.'
    
def test_unexpected_data(client):
    
    unexpected_data = [
            {'name' : 'id', 'value' : 'box-A'},
            {'name' : 'location', 'value' : 'stage right'},
            {'name' : 'notes', 'value' : 'contains cables'}]

    response = client.post('/', json={'data' : unexpected_data})
    assert response.status_code == 400
    assert response.headers['error'] == 'Bad Request'
    assert response.headers['message'] == 'Unexpected data given - id'

def test_empty_name(client):

    empty_name = [
            {'name' : 'name', 'value' : ''},
            {'name' : 'location', 'value' : 'stage right'},
            {'name' : 'notes', 'value' : 'contains cables'}]

    response = client.post('/', json={'data' : empty_name})
    assert response.status_code == 400
    assert response.headers['error'] == 'Bad Request'
    assert response.headers['message'] == 'No name or location was given'


def test_empty_loc(client):

    empty_loc = [
            {'name' : 'name', 'value' : 'box-A'},
            {'name' : 'location', 'value' : ''},
            {'name' : 'notes', 'value' : 'contains cables'}]

    response = client.post('/', json={'data' : empty_loc})
    assert response.status_code == 400
    assert response.headers['error'] == 'Bad Request'
    assert response.headers['message'] == 'No name or location was given'

def test_conflict_storage(client):
    new_storage_data = [
            {'name' : 'name', 'value' : 'box-A'},
            {'name' : 'location', 'value' : 'stage right'},
            {'name' : 'notes', 'value' : 'good!'}]

    response = client.post('/', json={'data' : new_storage_data})
    assert response.status_code == 201
    url =  response.headers['Location']
    assert urlparse(url).path == '/storage/1'

    response = client.post('/', json={'data' : new_storage_data})
    assert response.status_code == 409
    assert response.headers['error'] == 'Conflict'
    assert response.headers['message'] == 'The name box-A already exists.'

def test_read_new_storage(client):

    new_storage_data = [
            {'name' : 'name', 'value' : 'box-A'},
            {'name' : 'location', 'value' : 'stage right'},
            {'name' : 'notes', 'value' : 'good!'}]

    response = client.post('/', json={'data' : new_storage_data})
    assert response.status_code == 201
    url =  response.headers['Location']
    assert urlparse(url).path == '/storage/1'

    response = client.get(url).get_json()
    assert response != None

    items = response['collection']['items']
    assert len(items) == 1
   
    storage = items[0]
    assert urlparse(storage['href']).path == '/storage/1'

    expected_data = [
            {'name' : 'name', 'value' : 'box-A'},
            {'name' : 'date', 'value' : datetime.now().strftime('%d/%m/%Y')},
            {'name' : 'location', 'value' : 'stage right'},
            {'name' : 'notes', 'value' : 'good!'}]

    assert storage['data'] == expected_data


    links = storage['links']
    assert len(links) == 1

    link = links[0]
    assert urlparse(link['href']).path == '/storage/1/items'
    assert link['rel'] == 'contains'

def test_new_index(client):

    new_storage_data = [
            {'name' : 'name', 'value' : 'box-A'},
            {'name' : 'location', 'value' : 'stage right'},
            {'name' : 'notes', 'value' : 'good!'}]

    response = client.post('/', json={'data' : new_storage_data})
    assert response.status_code == 201
    url =  response.headers['Location']
    assert urlparse(url).path == '/storage/1'

    response = client.get('/').get_json()
    assert response != None

    items = response['collection']['items']
    assert len(items) == 1
   
    storage = items[0]
    assert urlparse(storage['href']).path == '/storage/1'

    expected_data = [
            {'name' : 'name', 'value' : 'box-A'},
            {'name' : 'date', 'value' : datetime.now().strftime('%d/%m/%Y')},
            {'name' : 'location', 'value' : 'stage right'},
            {'name' : 'notes', 'value' : 'good!'}]

    assert storage['data'] == expected_data


    links = storage['links']
    assert len(links) == 1

    link = links[0]
    assert urlparse(link['href']).path == '/storage/1/items'
    assert link['rel'] == 'contains'

def test_create_two_storage(client):

    storage_data_1 = [
            {'name' : 'name', 'value' : 'box-A'},
            {'name' : 'location', 'value' : 'stage right'},
            {'name' : 'notes', 'value' : 'good!'}]

    storage_data_2 = [
            {'name' : 'name', 'value' : 'box-B'},
            {'name' : 'location', 'value' : 'stage left'},
            {'name' : 'notes', 'value' : 'good!'}]

    response = client.post('/', json={'data' : storage_data_1})
    assert response.status_code == 201
    response = client.post('/', json={'data' : storage_data_2})
    assert response.status_code == 201

    response = client.get('/').get_json()
    assert response != None

    items = response['collection']['items']
    assert len(items) == 2
   
    storage = items[0]
    assert urlparse(storage['href']).path == '/storage/1'

    expected_data = [
            {'name' : 'name', 'value' : 'box-A'},
            {'name' : 'date', 'value' : datetime.now().strftime('%d/%m/%Y')},
            {'name' : 'location', 'value' : 'stage right'},
            {'name' : 'notes', 'value' : 'good!'}]

    assert storage['data'] == expected_data


    links = storage['links']
    assert len(links) == 1

    link = links[0]
    assert urlparse(link['href']).path == '/storage/1/items'
    assert link['rel'] == 'contains'

    storage = items[1]
    assert urlparse(storage['href']).path == '/storage/2'

    expected_data = [
            {'name' : 'name', 'value' : 'box-B'},
            {'name' : 'date', 'value' : datetime.now().strftime('%d/%m/%Y')},
            {'name' : 'location', 'value' : 'stage left'},
            {'name' : 'notes', 'value' : 'good!'}]

    assert storage['data'] == expected_data


    links = storage['links']
    assert len(links) == 1

    link = links[0]
    assert urlparse(link['href']).path == '/storage/2/items'
    assert link['rel'] == 'contains'





    


    





   




