from flask import request, jsonify
from urllib.parse import urlparse

def test_empty_db(client):

    content = client.get('/').get_json()['collection']
   
    # Test url of collection
    assert urlparse(content['href']).path == '/'

    # Test Links array
    assert len(content['links']) == 1

    link = content['links'][0]
    assert urlparse(link['href']).path == '/'
    assert link['rel'] == 'inventory'
    assert link['render'] == 'link'

    # Test items
    assert len(content['items']) == 0

    # Test queries
    queries_arr = content['queries']

    assert len(queries_arr) == 1

    search_query = queries_arr[0]
    assert urlparse(search_query['href']).path == '/storage/search'
    assert urlparse(search_query['rel']).path == 'search'

    query_data = search_query['data']

    assert {'name' : 'name', 'value' : ''} in query_data
    assert {'name' : 'location', 'value' : ''} in query_data
    assert {'name' : 'notes', 'value' : '' } in query_data

    # Test template 
    template_vals = content['template']['data']
    assert len(template_vals) == 4
    assert {'name' : 'name', 'value' : ''} in template_vals 
    assert {'name' : 'date', 'value' : ''} in template_vals
    assert {'name' : 'location', 'value' : ''} in template_vals 
    assert {'name' : 'notes', 'value' : '' } in template_vals


    # Test error
    error_val = content['error']
    assert error_val == None

