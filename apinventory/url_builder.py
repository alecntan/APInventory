
def build_storage_url(root_url, storage_id):
    return "{}storage/{}".format(root_url, storage_id)

def build_search_storage_url(root_url):
    return "{}storage/search".format(root_url)

def build_storage_items_url(root_url, storage_id):
    return "{}storage/{}/items".format(root_url, storage_id)

def build_search_item_url(root_url):
    return "{}item/search".format(root_url)

def build_item_url(root_url, item_id):
    return "{}item/{}".format(root_url, item_id)






