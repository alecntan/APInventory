from flask import Blueprint, current_app, request, Response, redirect, url_for, make_response
from sqlalchemy import or_
from datetime import datetime

from .collection import *
from .database import *
from .url_builder import *

CONTENT_TYPE='application/vnd.collection+json'

inventory = Blueprint('inventory', __name__)

@inventory.route('/', methods=['GET'])
def index():

    domain = request.url_root

    # Build urls
    inventory_href = request.url_root
    search_inventory_href = build_search_storage_url(request.url_root)
    response = CollectionOfStorage(request.base_url, inventory_href)
    response.set_storage_queries(search_inventory_href)
    response.set_storage_template()

    all_storages = Storage.query.all()

    for s in all_storages:

        storage_url = build_storage_url(request.url_root, s.id)
        items_url = build_storage_items_url(request.url_root, s.id)
        response.add_storage(storage_url, s.name, datetime.now(), s.location, s.notes, items_url)

    return get_collection_response(response.get_json(), '200')

@inventory.route('/', methods=['POST'])
def add_new_storage():

    request_data = request.get_json()

    code = '400'
    title = 'Bad Request'

    if request_data == None or request_data['data'] == None:
        message = 'Null object was sent, or no data was given'
        return make_response('', code, {'error' : title, 'message' : message})

    data_arr = request_data['data']

    if len(data_arr) != 3:
        message = 'Incorrect number of data items sent. Ensure that you use the template provided.'
        return make_response('', code, {'error' : title, 'message' : message})

    name = ''
    loc = ''
    notes = ''

    for data_pair in data_arr:

        if data_pair['name'] == 'name':
            name = data_pair['value']

        elif data_pair['name'] == 'location':
            loc = data_pair['value']

        elif data_pair['name'] == 'notes':
            notes = data_pair['value']

        else:
            message = 'Unexpected data given - {}'.format(data_pair['name'])
            return make_response('', code, {'error' : title, 'message' : message})

    if name == '' or loc == '':
        message = 'No name or location was given'
        return make_response('', code, {'error' : title, 'message' : message})


    code = '409'
    title = 'Conflict'

    if  Storage.query.filter_by(name=name).first():
        message = 'The name {} already exists.'.format(name)
        return make_response('', code, {'error' : title, 'message' : message})
   
    # Create new storage      
   
    try:
        new_storage = Storage(date=datetime.now(), name=name, location=loc, notes=notes)
        db.session.add(new_storage)
        db.session.commit()
    except:
        code = '500'
        title = 'Internal Server Error'
        message = 'Failed to create new storage'
        return make_response('', code, {'error' : title, 'message' : message})

    storage_id = Storage.query.filter_by(name=name).first().id
    new_storage_href = build_storage_url(request.url_root, storage_id)
    return make_response('', '201', {'Location' : new_storage_href})


@inventory.route('/storage/search', methods=['GET'])
def search_storage():
    
    href = request.base_url
    response = CollectionOfStorage(href, request.url_root)
    response.set_storage_queries(request.base_url)

    storage_query = Storage.query
    if request.query_string:

        name = request.args.get('name')
        loc  = request.args.get('location')
        notes = request.args.get('notes')

        if name:
            storage_query = storage_query.filter_by(name=name)
        if loc:
            storage_query = storage_query.filter_by(location=loc)
        if notes:
            storage_query = storage_query.filter_by(notes=notes)

    all_storages = storage_query.all()
    if not all_storages:
        return make_response('', '404', {'error' : 'NOT FOUND' , 'message' : 'Could not find any Storage that matched search parameters'})

    for s in all_storages:

        storage_href = build_storage_url(request.url_root, s.id)
        items_url = build_storage_items_url(request.url_root, s.id)

        response.add_storage(storage_href, s.name, s.date, s.location, s.notes, items_url)

    return get_collection_response(response.get_json(), '200')


@inventory.route('/storage/<id>', methods=['GET'])
def get_storage(id):

    storage = Storage.query.filter_by(id=id).first()
    items_href = build_storage_items_url(request.url_root, id)

    response = CollectionOfStorage(request.base_url, request.url_root)
    response.add_storage(request.base_url, storage.name, datetime.now(), storage.location, storage.notes, items_href)

    return get_collection_response(response.get_json(), '200')


@inventory.route('/storage/<id>', methods=['DELETE'])
def delete_storage(id):

    try:
        Item.query.filter_by(storage_id=id).delete()
        Storage.query.filter_by(id=id).delete()
        db.session.commit()
    except:
        return make_response('', '500', {'error' : 'Internal Server Error', 'message' : 'Database failed to delete storage'})

    return make_response('', '204')


@inventory.route('/storage/<id>', methods=['PUT'])
def update_storage(id):
    
    new_val_json = request.get_json()
    current_storage = Storage.query.filter_by(id=id).first()

    if not new_val_json or not new_val_json['data']:
        return make_response('', '400', {'error' : 'Bad Request', 'message' : 'Null object was sent, or no data was given'})

    for new_val_obj in new_val_json['data']:

        if new_val_obj['name'] == 'name' and new_val_obj['value']:
            new_name = new_val_obj['value']
            if new_name != current_storage.name and Storage.query.filter_by(name=new_name).first():
                return make_response('', '409', {'error' : 'Conflict', 'message' : 'New name already exists'})

            current_storage.name = new_name

        elif new_val_obj['name'] == 'location' and new_val_obj['value']:
            current_storage.location = new_val_obj['value']

        elif new_val_obj['name'] == 'notes' and new_val_obj['value']:
            current_storage.notes = new_val_obj['value']

    try:
        db.session.commit() 
    except:
        return make_response('', '500', {'error' : 'Internal Server Error', 'message' : 'Failed to update storage details'})

    return make_response('', '200')
   

@inventory.route('/storage/<id>/items', methods=['GET'])
def get_storage_items(id):

        items = Item.query.filter_by(storage_id=id).all()
        storage_href = build_storage_url(request.url_root, id)
        response = CollectionOfItem(request.base_url)
        response.set_storage_link(storage_href)
        response.set_item_template()
        response.set_item_queries(build_search_item_url(request.url_root))
        
        for i in items:

            item_href = build_item_url(request.url_root, i.id)
            response.store_item(item_href, storage_href, i.name, datetime.now(), i.identifier, i.status, i.category.name, i.notes, i.serialNumber, i.owner)

        return get_collection_response(response.get_json(), '200')

@inventory.route('/storage/<id>/items', methods=['POST'])
def add_item_to_storage(id):

    response = request.get_json()

    if not response or not response['data']:
        return make_response('', '400', {'error' : 'Bad Request', 'message' : 'Null object was sent, or no data was given'})
  
    item_name = ''
    item_identifier = ''
    item_status = ''
    item_category = ''
    item_serialNumber = ''
    item_owner = ''
    item_notes = ''

    for data in response['data']:

        if data['name'] == 'name' and data['value']:
            item_name = data['value']

        elif data['name'] == 'identifier' and data['value']:
            item_identifier = data['value']

        elif data['name'] == 'status' and data['value']:
            item_status = data['value']

        elif data['name'] == 'category' and data['value']:
            item_category = data['value']

        elif data['name'] == 'serialNumber' and data['value']:
            item_serialNumber = data['value']

        elif data['name'] == 'owner' and data['value']:
            item_owner = data['value']

        elif data['name'] == 'notes' and data['value']:
            item_notes = data['value']

    message = ''
    has_error = False
    if not item_name:
        message ='No item name was given'
        has_error = True
    elif not item_status:
        message = 'No item status was given'
        has_error = True
    elif not item_identifier:
        message = 'No item identifier was given'
        has_error = True
    elif not item_category:
        message = 'No item category was given'
        has_error = True
    elif not item_serialNumber:
        message = 'No item serial number was given'
        has_error = True
    elif not item_owner:
        message = 'No item owner was given'
        has_error = True

    if has_error:
        return make_response('', '400', {'error' : 'Bad request', 'message' : message})

    if Item.query.filter_by(identifier=item_identifier).first():
        return make_response('', '409', {'error' : 'Conflict', 'message' : 'Item with identifier {} already exists'.format(item_identifier)})

    try:
    
        category = Category.query.filter_by(name=item_category).first()
        if not category: 
            new_category = Category(name=item_category)
            db.session.add(new_category)
            db.session.commit()
       
        category = Category.query.filter_by(name=item_category).first()
        new_item = Item(date=datetime.now()
                       ,name=item_name
                       ,identifier=item_identifier
                       ,status=item_status
                       ,category_id=category.id
                       ,owner=item_owner
                       ,serialNumber=item_serialNumber
                       ,notes=item_notes
                       ,storage_id=id)

        db.session.add(new_item)
        db.session.commit()

    except:
        return make_response('', '500', {'error' : 'Internal Server Error', 'message' : 'Failed to add new item'}) 

     
    new_item = Item.query.filter_by(identifier=item_identifier).first()
    return make_response('', '201', {'Location' : build_item_url(request.url_root, new_item.id)})

    
@inventory.route('/item/<id>', methods=['GET'])
def get_item(id):

    item = Item.query.filter_by(id=id).first()
    storage_href = build_storage_url(request.url_root, item.storage_id)
    
    response = CollectionOfItem(request.base_url)
    response.set_storage_link(storage_href)
    response.store_item(request.base_url, storage_href, item.name, datetime.now(), item.identifier, item.status, item.category.name, item.notes, item.serialNumber, item.owner)

    return get_collection_response(response.get_json(), '200')


@inventory.route('/item/<id>', methods=['PUT'])
def update_item(id):

    new_item_details = request.get_json()
    item = Item.query.filter_by(id=id).first()
    
    if not new_item_details or not item:
        return make_response('', '400', {'error' : 'Bad Request', 'message' : 'No data was sent or item does not exist'})
   

    data_arr = new_item_details['data']
    for data_obj in data_arr:

        if data_obj['name'] == 'name' and data_obj['value']:
            item.name = data_obj['value']

        elif data_obj['name'] == 'identifier' and data_obj['value']:
            new_id = data_obj['value']
            if Item.query.filter_by(identifier=new_id).first():
                return make_response('', '409', {'error' : 'Conflict', 'message' : 'Item with identifier {} already exists'.format(new_id)})
            
            item.identifier = new_id

        elif data_obj['name'] == 'status' and data_obj['value']:
            item.status = data_obj['value']

        elif data_obj['name'] == 'category' and data_obj['value']:
            new_category =  Category.query.filter_by(name=data_obj['value']).first()
            if not new_category:
                try:
                    new_category = Category(name=data_obj['value'])
                    db.session.add(new_category)
                    db.session.commit()

                except:
                    return make_response('', '500', {'error' : 'Internal Server Error', 'message' : 'Could not create new category'})

                new_category = Category.query.filter_by(name=data_obj['value']).first()

            item.category = new_category

        elif data_obj['name'] == 'owner' and data_obj['value']:
            item.owner = data_obj['value']

        elif data_obj['name'] == 'notes':
            item.notes = data_obj['value']

        elif data_obj['name'] == 'serialNumber' and data_obj['value']:
            item.serialNumber = data_obj['value']

        elif data_obj['name'] == 'storage' and data_obj['value']:
            storage_name = data_obj['value']
            storage = Storage.query.filter_by(name=storage_name).first()
            print(Storage.query.all())

            if not storage:
                return make_response('', '404', {'error' : 'Not Found', 'message' : 'New storage does not exist'})

            item.storage = storage

        try:
            db.session.add(item)
            db.session.commit()
        except:
            return make_response('', '500', {'error' : 'Internal Server Error', 'message' : 'Could not update item details'})

    return make_response('', '200')

@inventory.route('/item/<id>', methods=['DELETE'])
def delete_item(id):
    
    item = Item.query.filter_by(id=id).first()
    if not item:
        return make_response('', '404', {'error' : 'Not Found', 'message' : 'Item does not exist'})

    Item.query.filter_by(id=id).delete()
    db.session.commit()

    return make_response('', '204')

@inventory.route('/item/search', methods=['GET'])
def search_item():

    response = CollectionOfItem(request.base_url)
    response.add_link(request.url_root, 'inventory', 'All storages', 'Inventory')
    
    item_query = Item.query
    if request.query_string:

        name = request.args.get('name')
        identifier = request.args.get('identifier')
        status = request.args.get('status')
        category_name = request.args.get('category')
        notes = request.args.get('comments')
        serialNumber = request.args.get('serialNumber')
        owner = request.args.get('owner')

        if name:
            item_query = item_query.filter_by(name=name)
        if identifier:
            item_query = item_query.filter_by(identifier=identifier)
        if status:
            item_query = item_query.filter_by(status=status)
        if category_name:
            category = Category.query.filter_by(name=category_name).first() 
            if not category:
                return make_response('', '404', {'error' : 'Not Found', 'message' : 'Could not find any items that matched search parameters'})
            item_query = item_query.filter_by(category_id=category.id)
        if notes:
            item_query = item_query.filter_by(notes=notes)
        if serialNumber:
            item_query = item_query.filter_by(serialNumber=serialNumber)
        if owner:
            item_query = item_query.filter_by(owner=owner)

    items = item_query.all()
    if not items:
        return make_response('', '404', {'error' : 'Not Found', 'message' : 'Could not find any items that matched search parameters'})

        
    for i in items:

        response.store_item(build_item_url(request.url_root, i.id),
                            build_storage_url(request.url_root, i.storage_id),
                            i.name,
                            datetime.now(),
                            i.identifier, 
                            i.status,
                            i.category.name,
                            i.notes,
                            i.serialNumber,
                            i.owner) 

    return get_collection_response(response.get_json(), '200')
   


