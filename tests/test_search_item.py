from flask import request
from urllib.parse import urlencode

def test_search_by_category(client_with_item):

    search_params={'category' : 'Cable'}
    path = '/item/search?'
    path_url = "{}{}".format(path, urlencode(search_params))
    response = client_with_item.get(path_url)
    assert response.status_code == 200
    
    response_json = response.get_json()
    items = response_json['collection']['items']
    assert len(items) == 2

def test_search_by_missing_category(client_with_item):

    search_params={'category' : 'device'}
    path = '/item/search?'
    path_url = "{}{}".format(path, urlencode(search_params))
    print(path_url)
    response = client_with_item.get(path_url)
    assert response.status_code == 404
    assert response.headers['error'] == 'Not Found'
    assert response.headers['message'] == 'Could not find items that matched search parameters'
    

def test_search_by_name(client_with_item):

    search_params={'name' : 'hdmi'}
    path_url = "{}{}".format('/item/search?', urlencode(search_params))
    response = client_with_item.get(path_url)
    assert response.status_code == 200

    response_json = response.get_json()
    items = response_json['collection']['items']
    assert len(items) == 1
     

def test_search_by_missing_name(client_with_item):

    search_params={'name' : 'one piece'}
    path = '/item/search?'
    path_url = "{}{}".format(path, urlencode(search_params))
    print(path_url)
    response = client_with_item.get(path_url)
    assert response.status_code == 404
    assert response.headers['error'] == 'Not Found'
    assert response.headers['message'] == 'Could not find any items that matched search parameters'
 
def test_search_by_identifier(client_with_item):

    search_params={'identifier' : 'CABHDM01'}
    path = '/item/search?'
    path_url = "{}{}".format(path, urlencode(search_params))
    print(path_url)
    response = client_with_item.get(path_url)
    response.status_code == 200

    response_json = response.get_json()
    items = response_json['collection']['items']
    assert len(items) == 1
     


def search_by_missing_identifier(client_with_item):

    search_params={'identifier' : 'ONEPIECE'}
    path = '/item/search?'
    path_url = "{}{}".format(path, urlencode(search_params))
    print(path_url)
    response = client_with_item.get(path_url)
    assert response.status_code == 404
    assert response.headers['error'] == 'Not Found'
    assert response.headers['message'] == 'Could not find any items that matched search parameters'
 

def test_search_by_status(client_with_item):

    search_params={'status' : 'In Storage'}
    path = '/item/search?'
    path_url = "{}{}".format(path, urlencode(search_params))
    print(path_url)
    response = client_with_item.get(path_url)
    response.status_code == 200

    response_json = response.get_json()
    items = response_json['collection']['items']
    assert len(items) == 1
     


def search_by_missing_status(client_with_item):

    search_params={'status' : 'Stolen'}
    path = '/item/search?'
    path_url = "{}{}".format(path, urlencode(search_params))
    print(path_url)
    response = client_with_item.get(path_url)
    assert response.status_code == 404
    assert response.headers['error'] == 'Not Found'
    assert response.headers['message'] == 'Could not find any items that matched search parameters'
 

def test_search_by_serialNum(client_with_item):

    search_params={'serialNumber' : 'AABB'}
    path = '/item/search?'
    path_url = "{}{}".format(path, urlencode(search_params))
    print(path_url)
    response = client_with_item.get(path_url)
    response.status_code == 200

    response_json = response.get_json()
    items = response_json['collection']['items']
    assert len(items) == 1
     

def search_by_missing_serialNum(client_with_item):

    search_params={'serialNum' : 'QQZZ'}
    path = '/item/search?'
    path_url = "{}{}".format(path, urlencode(search_params))
    print(path_url)
    response = client_with_item.get(path_url)
    assert response.status_code == 404
    assert response.headers['error'] == 'Not Found'
    assert response.headers['message'] == 'Could not find any items that matched search parameters'


def test_search_by_owner(client_with_item):

    search_params={'owner' : 'tech'}
    path = '/item/search?'
    path_url = "{}{}".format(path, urlencode(search_params))
    print(path_url)
    response = client_with_item.get(path_url)
    response.status_code == 200

    response_json = response.get_json()
    items = response_json['collection']['items']
    assert len(items) == 2
     

def search_by_missing_owner(client_with_item):

    search_params={'owner' : 'Roger Pirates'}
    path = '/item/search?'
    path_url = "{}{}".format(path, urlencode(search_params))
    print(path_url)
    response = client_with_item.get(path_url)
    assert response.status_code == 404
    assert response.headers['error'] == 'Not Found'
    assert response.headers['message'] == 'Could not find any items that matched search parameters'
 
