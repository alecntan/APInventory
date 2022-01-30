from flask import request
from urllib.parse import urlencode


def test_search_storage(client_with_storage):

    search_params = {'name': 'box-A', 'location' : 'stage right'}
    path = '/storage/search?'
    path_url = "{}{}".format(path, urlencode(search_params))

    response = client_with_storage.get(path_url)
    assert response.status_code == 200

    response_json = response.get_json()
    items = response_json['collection']['items']

    print(response_json)
    assert len(items) == 1 

    item_data = items[0]['data']

    for data in item_data:
        if data['name'] == 'name':
            assert data['value'] == 'box-A'
        elif data['name'] == 'location':
            assert data['value'] == 'stage right'

        
def test_search_404(client):
    
    search_params = {'name': 'box-A', 'location' : 'stage right'}
    path = '/storage/search?'
    path_url = "{}{}".format(path, urlencode(search_params))

    response = client.get(path_url)
    assert response.status_code == 404
    assert response.headers['error'] == 'Not Found'
    assert response.headers['message'] == 'Could not find any Storage that matched search parameters'


        
 
