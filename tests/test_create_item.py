from flask import request
from urllib.parse import urlparse
from datetime import datetime


def test_add_item(client_with_storage):
   
    new_item_data = [{'name' : 'name', 'value' : 'xlr'},
                     {'name' : 'identifier', 'value' : 'CABXLR01'},
                     {'name' : 'status', 'value' : 'In storage'},
                     {'name' : 'category', 'value' : 'Cable'},
                     {'name' : 'notes', 'value' : 'In good condition!'},
                     {'name' : 'serialNumber', 'value' : 'AABBCC001'},
                     {'name' : 'owner', 'value' : 'Tech Team'}]

    response = client_with_storage.post('/storage/1/items', json={'data' : new_item_data})
    assert response.status_code == 201
    assert urlparse(response.headers['Location']).path == '/item/1'
 
    item_response = client_with_storage.get('/item/1').get_json()
    item_data = item_response['collection']['items'][0]['data']
    expected_data = [{'name' : 'name', 'value' : 'xlr'},
                     {'name' : 'date', 'value' : datetime.now().strftime('%d/%m/%Y')},
                     {'name' : 'identifier', 'value' : 'CABXLR01'},
                     {'name' : 'status', 'value' : 'In storage'},
                     {'name' : 'category', 'value' : 'Cable'},
                     {'name' : 'notes', 'value' : 'In good condition!'},
                     {'name' : 'serialNumber', 'value' : 'AABBCC001'},
                     {'name' : 'owner', 'value' : 'Tech Team'},
                     {'name' : 'storage', 'value' : 'box-A'}]

    assert item_data == expected_data
    
    

    

    

