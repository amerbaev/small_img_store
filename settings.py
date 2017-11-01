MONGO_HOST = 'localhost'
MONGO_PORT = 27017
MONGO_DBNAME = 'small_img'

RESOURCE_METHODS = ['GET', 'POST', 'DELETE']
ITEM_METHODS = ['GET', 'PATCH', 'PUT', 'DELETE']

schema = {
    'image': {
        'type': 'media'
    },
    'name': {
        'type': 'string'
    },
    'meta': {}
}

images = {
    'cache_control': 'max-age=10, must-revalidate',
    'cache_expires': 10,
    'schema': schema
}

DOMAIN = {
    'images': images
}
