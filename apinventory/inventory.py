from flask import Blueprint, current_app, request, Response, redirect, url_for
from sqlalchemy import or_

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

        response.add_storage(storage_url, s.name, s.location, s.notes, items_url)

    return get_collection_response(response.get_json(), '200')

@inventory.route('/', methods=['POST'])
def add_new_storage():
    redirect(url_for('inventory.index'))

@inventory.route('/storage/search', methods=['GET'])
def search_storage():
    
    href = request.base_url
    response = CollectionOfStorage(href, request.url_root)
    response.set_storage_queries(request.base_url)

    storage_query = Storage.query
    if request.query_string:

        name = request.args.get('name')
        loc  = request.args.get('location')
        notes = request.args.get('comments')

        if name:
            storage_query = storage_query.filter_by(name=name)
        if loc:
            storage_query = storage_query.filter_by(location=loc)
        if notes:
            storage_query = storage_query.filter_by(notes=notes)

    all_storages = storage_query.all()
    if not all_storages:

        response.set_error('Not Found', '404', 'Could not find any Storage that matched search parameters')
        return get_collection_response(response.get_json(), '404')


    for s in all_storages:

        storage_url = build_storage_url(request.url_root, s.id)
        items_url = build_storage_items_url(request.url_root, s.id)

        response.add_storage(storage_url, s.name, s.location, s.notes, items_url)

    return get_collection_response(response.get_json(), '200')


@inventory.route('/storage/<id>', methods=['GET'])
def get_storage(id):

    storage = Storage.query.filter_by(id=id).first()
    items_href = build_storage_items_url(request.url_root, id)

    response = CollectionOfStorage(request.base_url, request.url_root)
    response.add_storage(request.base_url, storage.name, storage.location, storage.notes, items_href)

    return get_collection_response(response.get_json(), '200')


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
            response.store_item(item_href, storage_href, i.name, i.identifier, i.status, i.category, i.notes, i.serialNumber, i.owner)

        return get_collection_response(response.get_json(), '200')

@inventory.route('/item/<id>', methods=['GET'])
def get_item(id):

    item = Item.query.filter_by(id=id).first()
    storage_href = build_storage_url(request.url_root, item.storage_id)
    
    response = CollectionOfItem(request.base_url)
    response.set_storage_link(storage_href)
    response.store_item(request.base_url, storage_href, item.name, item.identifier, item.status, item.category, item.notes, item.serialNumber, item.owner)

    return get_collection_response(response.get_json(), '200')
    
@inventory.route('/item/search', methods=['GET'])
def search_item():

    response = CollectionOfItem(request.base_url)
    response.add_link(request.url_root, 'inventory', 'All storages', 'Inventory')
    
    item_query = Item.query
    if request.query_string:

        name = request.args.get('name')
        identifier = request.args.get('identifier')
        status = request.args.get('status')
        category = request.args.get('category')
        notes = request.args.get('comments')
        serialNumber = request.args.get('serialNumber')
        owner = request.args.get('owner')

        if name:
            item_query = item_query.filter_by(name=name)
        if identifier:
            item_query = item_query.filter_by(identifier=identifier)
        if status:
            item_query = item_query.filter_by(status=status)
        if category:
            item_query = item_query.filter_by(category=category)
        if notes:
            item_query = item_query.filter_by(notes=notes)
        if serialNumber:
            item_query = item_query.filter_by(serialNumber=serialNumber)
        if owner:
            item_query = item_query.filter_by(owner=owner)

    items = item_query.all()

    if not items:

        response.set_error('Not Found', '404','No items found that matched the search parameters.')
        return get_collection_response(response.get_json(), '404')
        
    for i in items:

        response.store_item(build_item_url(request.url_root, i.id),
                            build_storage_url(request.url_root, i.storage_id),
                            i.name,
                            i.identifier, 
                            i.status,
                            i.category,
                            i.notes,
                            i.serialNumber,
                            i.owner)


    return get_collection_response(response.get_json(), '200')
    

