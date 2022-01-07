"""
A set of classes that can be used to create collection+json representations of storages and things.
Media Type: https://github.com/collection-json/spec

By: Alec Tan
"""

import json

class GenericCollection:

    def __init__(self, href, links=None, items=None, queries=None, template=None, error=None):

        self.href = href
        self.version = "1.0"
        self.links = links
        self.items = items
        self.queries = queries
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

    def __init__(self, href, search_href, items=[]):

        super().__init__(href, items=items)

        queries_data  = [{'name' : 'search', 'value' : ""}]
        template_data = [{'name' : 'name'    , 'value' : ''},
                         {'name' : 'location', 'value' : ''},
                         {'name' : 'comments', 'value' : ''}
                        ]
        
        self.add_link(href, 'inventory', 'All Storages', 'Inventory')
        self.add_query_template(search_href, 'search', 'Search Storage', 'Search', queries_data)
        self.set_template(template_data)

    def add_storage(self, href, name, location, comments, things_href):

        data = [{'name' : 'name'    , 'value' : name},
                {'name' : 'location', 'value' : location},
                {'name' : 'comments', 'value' : comments}]

        links = [{'href'   : things_href,
                  'rel'    : 'contains',
                  'prompt' : 'Things stored in this storage',
                  'name'   : 'Collection of Things',
                  'render' : 'link'}]
   
        self.add_item(href, data, links)



class CollectionOfThing(GenericCollection):

    def __init__(self, href, search_href, items=[]):

        super().__init__(href, items=items)

        thing_queries_data  = [{'name' : 'search', 'value' : ""}]
        template_data = [{'name' : 'name'    , 'value' : ''},
                         {'name' : 'identifier', 'value' : ''},
                         {'name' : 'status', 'value' : ''},
                         {'name' : 'category', 'value' : ''},
                         {'name' : 'comments', 'value' : ''},
                         {'name' : 'owner', 'value' : ''}
                        ]

        self.add_query_template(search_href, 'search', 'Search for Thing', 'Search', thing_queries_data)
        self.set_template(template_data)


    def add_thing(self, href, name, identifier, status, category, comments, owner):
        
        data = [{'name' : 'name'      , 'value' : name},
                {'name' : 'identifier', 'value' : identifier},
                {'name' : 'status'    , 'value' : status},
                {'name' : 'category'  , 'value' : category},
                {'name' : 'comments'  , 'value' : comments},
                {'name' : 'owner'     , 'value' : owner}]

        links = [{'href'   : storage_href,
                  'rel'    : 'stored_by',
                  'prompt' : 'Storage by',
                  'name'   : 'Storage',
                  'render' : 'link'}]

        self.add_item(href, data=data, links=links)
