from flask import  request
from datetime import datetime

def test_update_storage(client):

    new_storage_data = [
            {'name' : 'name', 'value' : 'box-A'},
            {'name' : 'location', 'value' : 'stage right'},
            {'name' : 'notes', 'value' : 'good!'}]

    response = client.post('/', json={'data' : new_storage_data })
    assert response.status_code == 201

    response = client.get('/')
    response_json = response.get_json()
    response_data = response_json['collection']['items'][0]['data'][0]
    assert response_data['name'] == 'name' and response_data['value'] == 'box-A'

    new_storage_data = [
            {'name' : 'name', 'value' : 'box-B'},
            {'name' : 'location', 'value' : 'stage left'},
            {'name' : 'notes', 'value' : 'okay!'}]


    response = client.put('/storage/1', json={'data' : new_storage_data})
    response.status_code == 200
    
    response = client.get('/storage/1')
    response_json = response.get_json()
    response_data = response_json['collection']['items'][0]['data']
    
    expected_data = [
            {'name' : 'name', 'value' : 'box-B'},
            {'name' : 'date', 'value' : datetime.now().strftime('%d/%m/%Y')},
            {'name' : 'location', 'value' : 'stage left'},
            {'name' : 'notes', 'value' : 'okay!'}]

    assert expected_data == response_data    

def test_update_storage_none(client):

    new_storage_data = [
            {'name' : 'name', 'value' : 'box-A'},
            {'name' : 'location', 'value' : 'stage right'},
            {'name' : 'notes', 'value' : 'good!'}]

    response = client.post('/', json={'data' : new_storage_data })
    assert response.status_code == 201

    response = client.get('/')
    response_json = response.get_json()
    response_data = response_json['collection']['items'][0]['data'][0]
    assert response_data['name'] == 'name' and response_data['value'] == 'box-A'


    response = client.put('/storage/1', json={'data' : None})
    response.status_code == 400
    assert response.headers['error'] == 'Bad Request'
    assert response.headers['message'] == 'Null object was sent, or no data was given'

    response = client.put('/storage/1')
    response.status_code == 400
    assert response.headers['error'] == 'Bad Request'
    assert response.headers['message'] == 'Null object was sent, or no data was given'

def test_update_with_existing(client):

    
    new_storage_A = [
            {'name' : 'name', 'value' : 'box-A'},
            {'name' : 'location', 'value' : 'stage right'},
            {'name' : 'notes', 'value' : 'good!'}]

    new_storage_B = [
            {'name' : 'name', 'value' : 'box-B'},
            {'name' : 'location', 'value' : 'stage right'},
            {'name' : 'notes', 'value' : 'good!'}]



    response = client.post('/', json={'data' : new_storage_A })
    assert response.status_code == 201
    response = client.post('/', json={'data' : new_storage_B })
    assert response.status_code == 201

    response = client.put('/storage/1', json={'data' : [{'name' : 'name' , 'value' : 'box-B'}]})
    response.status_code == 409
    assert response.headers['error'] == 'Conflict'
    assert response.headers['message'] == 'New name already exists'


