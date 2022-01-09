from flask import request

def test_delete_single_storage(client):

    new_storage_data = [
            {'name' : 'name', 'value' : 'box-A'},
            {'name' : 'location', 'value' : 'strage-right'},
            {'name' : 'notes', 'value' : 'good!'}]

    response = client.post('/', json={'data' : new_storage_data})
    assert response.status_code == 201

    response = client.get('/')
    response_data = response.get_json()
    assert len(response_data['collection']['items']) == 1

    response = client.delete('/storage/1')
    assert response.status_code == 204

    response = client.get('/')
    response_data = response.get_json()
    assert len(response_data['collection']['items']) == 0


def test_delete_storages(client):

    new_storage_A = [
            {'name' : 'name', 'value' : 'box-A'},
            {'name' : 'location', 'value' : 'strage-right'},
            {'name' : 'notes', 'value' : 'good!'}]
  
    new_storage_B = [
            {'name' : 'name', 'value' : 'box-B'},
            {'name' : 'location', 'value' : 'strage-right'},
            {'name' : 'notes', 'value' : 'good!'}]
  

    response = client.post('/', json={'data' : new_storage_A})
    response = client.post('/', json={'data' : new_storage_B})

    response = client.get('/')
    response_data = response.get_json()
    assert len(response_data['collection']['items']) == 2

    response = client.delete('/storage/1')
    assert response.status_code == 204

    
    response = client.get('/')
    response_data = response.get_json()
    assert len(response_data['collection']['items']) == 1
    items = response_data['collection']['items']
    storage_b_data = items[0]['data']
    assert storage_b_data[0]['value'] == 'box-B'
