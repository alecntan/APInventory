"""
A set of classes that can be used to create collection+json representations of storages and things.
Media Type: https://github.com/collection-json/spec

By: Alec Tan
"""

CONTENT_TYPE='application/vnd.collection+json'



import json
from flask import Response

class GenericCollection:

    def __init__(self, href, links=None, items=None, queries=None, template=None, error=None):

        self.href = href
        self.version = "1.0"
        self.links = links if links else []
        self.items = items if items else []
        self.queries = queries if queries else []
        self.template = template
        self.error = error
        

    def add_link(self, href, rel, prompt, name, render='link'):

        new_link = {'href'   : href,
                    'rel'    : rel,
                    'prompt' : prompt,
                    'name'   : name,
                    'render' : render
                   }

        if self.links == None:
            self.links = list()

        self.links.append(new_link)


    def add_item(self, href, data=[], links=[]):

        new_item = {'href'  : href,
                    'data'  : data,
                    'links' : links 
                   }

        if self.items == None:
            self.items = list()

        self.items.append(new_item)


    def add_query_template(self, href, rel, prompt, name, data=[]):

        new_query = {'href'   : href,
                     'rel'    : rel,
                     'prompt' : prompt,
                     'name'   : name,
                     'data'   : data
                    }

        if self.queries == None:
            self.queries = list()

        self.queries.append(new_query)
                    

    def set_error(self, title, code, message):

        new_error = {'title'   : title,
                     'code'    : code,
                     'message' : message
                    }

        self.error = new_error


    def set_template(self, data):

        new_template = {'data' : data}

        self.template = new_template


    def get_json(self):

        response = {'collection' : 

                        {
                            'version'  : self.version,
                            'href'     : self.href,
                            'links'    : self.links,
                            'items'    : self.items,
                            'queries'  : self.queries,
                            'template' : self.template,
                            'error'    : self.error 
                        }
                    }

        return json.dumps(response)


class CollectionOfStorage(GenericCollection):

    def __init__(self, href, inventory_href):

        super().__init__(href)
        self.add_link(inventory_href, 'inventory', 'All Storages', 'Inventory')
        
    def add_storage(self, href, name, date, location, notes, things_href):

        data = [{'name' : 'name'    , 'value' : name},
                {'name' : 'date'    , 'value' : date.strftime('%d/%m/%Y')},
                {'name' : 'location', 'value' : location},
                {'name' : 'notes'   , 'value' : notes}]

        links = [{'href'   : things_href,
        
                  'rel'    : 'contains',
                  'prompt' : 'Things stored in this storage',
                  'name'   : 'Collection of Things',
                  'render' : 'link'}]
   
        self.add_item(href, data, links)

    def set_storage_queries(self, search_href):

        queries_data  = [{'name' : 'name'    , 'value' : ''},
                         {'name' : 'location', 'value' : ''},
                         {'name' : 'notes'   , 'value' :''}]

        self.add_query_template(search_href, 'search', 'Search Storage', 'Search', queries_data)

    def set_storage_template(self):

        template_data = [{'name' : 'name'    , 'value' : ''},
                         {'name' : 'date'    , 'value' : ''},
                         {'name' : 'location', 'value' : ''},
                         {'name' : 'notes'   , 'value' : ''}]
                        
        self.set_template(template_data)
        


class CollectionOfItem(GenericCollection):

    def store_item(self, href, storage_href, name, date, identifier, status, category, notes, serialNumber, owner, storage):
        
        data = [{'name' : 'name'        , 'value' : name},
                {'name' : 'date'        , 'value' : date.strftime('%d/%m/%Y')},
                {'name' : 'identifier'  , 'value' : identifier},
                {'name' : 'status'      , 'value' : status},
                {'name' : 'category'    , 'value' : category},
                {'name' : 'notes'       , 'value' : notes },
                {'name' : 'serialNumber', 'value' : serialNumber},
                {'name' : 'owner'       , 'value' : owner},
                {'name' : 'storage'     , 'value' : storage}]

        links = [{'href'   : storage_href,
                  'rel'    : 'stored_by',
                  'prompt' : 'Storage by',
                  'name'   : 'Storage',
                  'render' : 'link'}]

        self.add_item(href, data=data, links=links)

    def set_storage_link(self, storage_href):

        self.add_link(storage_href, 'stored by', 'Storage holding these items', 'Storage')

    def set_item_template(self):
        
        template_data = [{'name' : 'name'    , 'value' : ''},
                         {'name' : 'identifier', 'value' : ''},
                         {'name' : 'status', 'value' : ''},
                         {'name' : 'category', 'value' : ''},
                         {'name' : 'notes'   , 'value' : ''},
                         {'name' : 'serialNumber', 'value' : ''},
                         {'name' : 'owner', 'value' : ''},
                         {'name' : 'storage', 'value' : ''}
                        ]
 
        self.set_template(template_data)

    def set_item_queries(self, search_href):

        item_queries_data  = [{'name' : 'name'    , 'value' : ''},
                              {'name' : 'identifier', 'value' : ''},
                              {'name' : 'status', 'value' : ''},
                              {'name' : 'category', 'value' : ''},
                              {'name' : 'notes', 'value' : ''},
                              {'name' : 'serialNumber', 'value' : ''},
                              {'name' : 'owner', 'value' : ''},
                              {'name' : 'storage', 'value' : ''}
                             ]

        self.add_query_template(search_href, 'search', 'Search for Thing', 'Search', item_queries_data)



def get_collection_response(val, code):
    return Response(val, mimetype=CONTENT_TYPE, content_type=CONTENT_TYPE)



