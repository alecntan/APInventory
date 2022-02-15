from flask import request
from datetime import datetime
from urllib.parse import urlparse

def test_update_missing_item(client):

    new_item_data = [{'name' : 'name', 'value' : 'One Piece'}]

    response = client.put('/item/1', json={'data' : new_item_data})
    assert response.status_code == 404


def test_update_item_no_data(client_with_item):

    response = client_with_item.put('/item/1')
    assert response.status_code == 400

def test_update_item(client_with_storages_and_items):

    new_item_data = [{'name' : 'name', 'value' : 'xlr'}
            ,{'name' : 'identifier', 'value' : 'CABXLR02'}
            ,{'name' : 'status', 'value' : 'In usage'}
            ,{'name' : 'category', 'value' : 'Visual'}
            ,{'name' : 'notes', 'value' : 'Its an xlr not a hdmi'}
            ,{'name' : 'serialNumber', 'value' : 'ZZYY'}
            ,{'name' : 'owner', 'value' : 'music'}
            ,{'name' : 'storage', 'value' : 'box-B'}]

    response = client_with_storages_and_items.put('/item/1', json={'data' : new_item_data})
    assert response.status_code == 200
   
    response = client_with_storages_and_items.get('/item/1')
    assert response.status_code == 200
    response_json = response.get_json()

    data = response_json['collection']['items'][0]['data']

    expected_data = [{'name' : 'name', 'value' : 'xlr'}
            ,{'name' : 'date', 'value' : datetime.now().strftime('%d/%m/%Y')}
            ,{'name' : 'identifier', 'value' : 'CABXLR02'}
            ,{'name' : 'status', 'value' : 'In usage'}
            ,{'name' : 'category', 'value' : 'Visual'}
            ,{'name' : 'notes', 'value' : 'Its an xlr not a hdmi'}
            ,{'name' : 'serialNumber', 'value' : 'ZZYY'}
            ,{'name' : 'owner', 'value' : 'music'}
            ,{'name' : 'storage', 'value' : 'box-B'}]


    assert data == expected_data

    storage_href = response_json['collection']['links'][0]['href']
    assert urlparse(storage_href).path == '/storage/2'
            
def test_update_item_name(client_with_item):

    new_item_data = [{'name' : 'name', 'value' : 'xlr'}
            ,{'name' : 'identifier', 'value' : ''}
            ,{'name' : 'status', 'value' : ''}
            ,{'name' : 'category', 'value' : ''}
            ,{'name' : 'notes', 'value' : 'In good condition!'}
            ,{'name' : 'serialNumber', 'value' : ''}
            ,{'name' : 'owner', 'value' : ''}
            ,{'name' : 'storage', 'value' : ''}]

    response = client_with_item.put('/item/1', json={'data' : new_item_data})
    assert response.status_code == 200
   
    response = client_with_item.get('/item/1')
    assert response.status_code == 200
    response_json = response.get_json()
    data = response_json['collection']['items'][0]['data']

    expected_data = [{'name' : 'name', 'value' : 'xlr'}
            ,{'name' : 'date', 'value' : datetime.now().strftime('%d/%m/%Y')}
            ,{'name' : 'identifier', 'value' : 'CABHDM01'}
            ,{'name' : 'status', 'value' : 'In Storage'}
            ,{'name' : 'category', 'value' : 'Cable'}
            ,{'name' : 'notes', 'value' : 'In good condition!'}
            ,{'name' : 'serialNumber', 'value' : 'AABB'}
            ,{'name' : 'owner', 'value' : 'tech'}
            ,{'name' : 'storage', 'value' : 'box-A'}]



    assert data == expected_data

     
def test_update_item_new_identifier(client_with_item):

    new_item_data = [{'name' : 'name', 'value' : ''}
            ,{'name' : 'identifier', 'value' : 'CABHDM02'}
            ,{'name' : 'status', 'value' : ''}
            ,{'name' : 'category', 'value' : ''}
            ,{'name' : 'notes', 'value' : 'In good condition!'}
            ,{'name' : 'serialNumber', 'value' : ''}
            ,{'name' : 'owner', 'value' : ''}
            ,{'name' : 'storage', 'value' : ''}]

    response = client_with_item.put('/item/1', json={'data' : new_item_data})
    assert response.status_code == 200
   
    response = client_with_item.get('/item/1')
    assert response.status_code == 200
    response_json = response.get_json()
    data = response_json['collection']['items'][0]['data']

    expected_data = [{'name' : 'name', 'value' : 'hdmi'}
            ,{'name' : 'date', 'value' : datetime.now().strftime('%d/%m/%Y')}
            ,{'name' : 'identifier', 'value' : 'CABHDM02'}
            ,{'name' : 'status', 'value' : 'In Storage'}
            ,{'name' : 'category', 'value' : 'Cable'}
            ,{'name' : 'notes', 'value' : 'In good condition!'}
            ,{'name' : 'serialNumber', 'value' : 'AABB'}
            ,{'name' : 'owner', 'value' : 'tech'}
            ,{'name' : 'storage', 'value' : 'box-A'}]

    assert data == expected_data


def test_update_item_existing_identifier(client_with_item):

    new_item_data = [{'name' : 'name', 'value' : ''}
            ,{'name' : 'identifier', 'value' : 'CABXLR01'}
            ,{'name' : 'status', 'value' : ''}
            ,{'name' : 'category', 'value' : ''}
            ,{'name' : 'notes', 'value' : 'In good condition!'}
            ,{'name' : 'serialNumber', 'value' : ''}
            ,{'name' : 'owner', 'value' : ''}]

    response = client_with_item.put('/item/1', json={'data' : new_item_data})
    assert response.status_code == 409
    assert response.headers['error'] == 'Conflict'


def test_update_item_status(client_with_item):

    new_item_data = [{'name' : 'name', 'value' : ''}
            ,{'name' : 'identifier', 'value' : ''}
            ,{'name' : 'status', 'value' : 'In Usage'}
            ,{'name' : 'category', 'value' : ''}
            ,{'name' : 'notes', 'value' : 'In good condition!'}
            ,{'name' : 'serialNumber', 'value' : ''}
            ,{'name' : 'owner', 'value' : ''}
            ,{'name' : 'storage', 'value' : ''}]

    response = client_with_item.put('/item/1', json={'data' : new_item_data})
    assert response.status_code == 200
   
    response = client_with_item.get('/item/1')
    assert response.status_code == 200
    response_json = response.get_json()
    data = response_json['collection']['items'][0]['data']

    expected_data = [{'name' : 'name', 'value' : 'hdmi'}
            ,{'name' : 'date', 'value' : datetime.now().strftime('%d/%m/%Y')}
            ,{'name' : 'identifier', 'value' : 'CABHDM01'}
            ,{'name' : 'status', 'value' : 'In Usage'}
            ,{'name' : 'category', 'value' : 'Cable'}
            ,{'name' : 'notes', 'value' : 'In good condition!'}
            ,{'name' : 'serialNumber', 'value' : 'AABB'}
            ,{'name' : 'owner', 'value' : 'tech'}
            ,{'name' : 'storage', 'value' : 'box-A'}]


    assert data == expected_data

def test_update_item_category(client_with_item):

    new_item_data = [{'name' : 'name', 'value' : ''}
            ,{'name' : 'identifier', 'value' : ''}
            ,{'name' : 'status', 'value' : ''}
            ,{'name' : 'category', 'value' : 'Visual'}
            ,{'name' : 'notes', 'value' : 'In good condition!'}
            ,{'name' : 'serialNumber', 'value' : ''}
            ,{'name' : 'owner', 'value' : ''}
            ,{'name' : 'storage', 'value' : ''}]

    response = client_with_item.put('/item/1', json={'data' : new_item_data})
    assert response.status_code == 200
   
    response = client_with_item.get('/item/1')
    assert response.status_code == 200
    response_json = response.get_json()
    data = response_json['collection']['items'][0]['data']

    expected_data = [{'name' : 'name', 'value' : 'hdmi'}
            ,{'name' : 'date', 'value' : datetime.now().strftime('%d/%m/%Y')}
            ,{'name' : 'identifier', 'value' : 'CABHDM01'}
            ,{'name' : 'status', 'value' : 'In Storage'}
            ,{'name' : 'category', 'value' : 'Visual'}
            ,{'name' : 'notes', 'value' : 'In good condition!'}
            ,{'name' : 'serialNumber', 'value' : 'AABB'}
            ,{'name' : 'owner', 'value' : 'tech'}
            ,{'name' : 'storage', 'value' : 'box-A'}]


    assert data == expected_data


def test_update_item_owner(client_with_item):

    new_item_data = [{'name' : 'name', 'value' : ''}
            ,{'name' : 'identifier', 'value' : ''}
            ,{'name' : 'status', 'value' : ''}
            ,{'name' : 'category', 'value' : ''}
            ,{'name' : 'notes', 'value' : 'In good condition!'}
            ,{'name' : 'serialNumber', 'value' : ''}
            ,{'name' : 'owner', 'value' : 'music'}
            ,{'name' : 'storage', 'value' : ''}]

    response = client_with_item.put('/item/1', json={'data' : new_item_data})
    assert response.status_code == 200
   
    response = client_with_item.get('/item/1')
    assert response.status_code == 200
    response_json = response.get_json()
    data = response_json['collection']['items'][0]['data']

    expected_data = [{'name' : 'name', 'value' : 'hdmi'}
            ,{'name' : 'date', 'value' : datetime.now().strftime('%d/%m/%Y')}
            ,{'name' : 'identifier', 'value' : 'CABHDM01'}
            ,{'name' : 'status', 'value' : 'In Storage'}
            ,{'name' : 'category', 'value' : 'Cable'}
            ,{'name' : 'notes', 'value' : 'In good condition!'}
            ,{'name' : 'serialNumber', 'value' : 'AABB'}
            ,{'name' : 'owner', 'value' : 'music'}
            ,{'name' : 'storage', 'value' : 'box-A'}]


    assert data == expected_data

def test_update_item_serialNumber(client_with_item):

    new_item_data = [{'name' : 'name', 'value' : ''}
            ,{'name' : 'identifier', 'value' : ''}
            ,{'name' : 'status', 'value' : ''}
            ,{'name' : 'category', 'value' : ''}
            ,{'name' : 'notes', 'value' : 'In good condition!'}
            ,{'name' : 'serialNumber', 'value' : 'MMM'}
            ,{'name' : 'owner', 'value' : ''}
            ,{'name' : 'storage', 'value': ''}]

    response = client_with_item.put('/item/1', json={'data' : new_item_data})
    assert response.status_code == 200
   
    response = client_with_item.get('/item/1')
    assert response.status_code == 200
    response_json = response.get_json()
    data = response_json['collection']['items'][0]['data']

    expected_data = [{'name' : 'name', 'value' : 'hdmi'}
            ,{'name' : 'date', 'value' : datetime.now().strftime('%d/%m/%Y')}
            ,{'name' : 'identifier', 'value' : 'CABHDM01'}
            ,{'name' : 'status', 'value' : 'In Storage'}
            ,{'name' : 'category', 'value' : 'Cable'}
            ,{'name' : 'notes', 'value' : 'In good condition!'}
            ,{'name' : 'serialNumber', 'value' : 'MMM'}
            ,{'name' : 'owner', 'value' : 'tech'}
            ,{'name' : 'storage', 'value' : 'box-A'}]



    assert data == expected_data


def test_update_item_missing_storage(client_with_item):

    new_item_data = [{'name' : 'name', 'value' : ''}
            ,{'name' : 'identifier', 'value' : ''}
            ,{'name' : 'status', 'value' : ''}
            ,{'name' : 'category', 'value' : ''}
            ,{'name' : 'notes', 'value' : 'In good condition!'}
            ,{'name' : 'serialNumber', 'value' : ''}
            ,{'name' : 'owner', 'value' : ''}
            ,{'name' : 'storage', 'value' : 'box-b'}]

    response = client_with_item.put('/item/1', json={'data' : new_item_data})
    assert response.status_code == 404
    assert response.headers['error'] == 'Not Found'
    assert response.headers['message'] == 'New storage does not exist'

def test_update_item_storage(client_with_storages_and_items):

    response = client_with_storages_and_items.get('/item/1')
    assert response.status_code == 200
    response_json = response.get_json()
    storage_href = response_json['collection']['links'][0]['href']
    assert urlparse(storage_href).path == '/storage/1'

    new_item_data = [{'name' : 'name', 'value' : ''}
            ,{'name' : 'identifier', 'value' : ''}
            ,{'name' : 'status', 'value' : ''}
            ,{'name' : 'category', 'value' : ''}
            ,{'name' : 'notes', 'value' : 'In good condition!'}
            ,{'name' : 'serialNumber', 'value' : ''}
            ,{'name' : 'owner', 'value' : ''}
            ,{'name' : 'storage', 'value' : 'box-B'}]


    response = client_with_storages_and_items.put('/item/1', json={'data' : new_item_data})

    assert response.status_code == 200

   
    response = client_with_storages_and_items.get('/item/1')
    assert response.status_code == 200
    response_json = response.get_json()
    data = response_json['collection']['items'][0]['data']

    expected_data = [{'name' : 'name', 'value' : 'hdmi'}
            ,{'name' : 'date', 'value' : datetime.now().strftime('%d/%m/%Y')}
            ,{'name' : 'identifier', 'value' : 'CABHDM01'}
            ,{'name' : 'status', 'value' : 'In Storage'}
            ,{'name' : 'category', 'value' : 'Cable'}
            ,{'name' : 'notes', 'value' : 'In good condition!'}
            ,{'name' : 'serialNumber', 'value' : 'AABB'}
            ,{'name' : 'owner', 'value' : 'tech'}
            ,{'name' : 'storage', 'value' : 'box-B'}]


    assert data == expected_data

    storage_href = response_json['collection']['links'][0]['href']
    assert urlparse(storage_href).path == '/storage/2'



