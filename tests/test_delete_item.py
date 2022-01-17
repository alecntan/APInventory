from flask import request

def test_delete_item(client_with_item):
    
    response = client_with_item.delete('/item/1')
    assert response.status_code == 204

def test_delete_missing_item(client):

    response = client.delete('/item/1')
    assert response.status_code == 404
