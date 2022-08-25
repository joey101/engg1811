data = {
    'channels': [
        {
            'id': 1,
            'name': 'name',
            'status': 'is_public',
            'owner': 'auth_user_id',
            'members': 1,
            'messages': ["jawad", "HI"]
        },
        {
            'id': 'len(ds[])',
            'name': 'name',
            'status': 'is_public',
            'owner': 'auth_user_id',
            'members': ['auth_user_id'],
            'messages': ["jawad", "HI"]
        }
    ],
    'users': []
}

## YOU ARE ALLOWED TO CHANGE THE BELOW IF YOU WISH
class Datastore:
    def __init__(self):
        self.__store = data

    def get(self):
        return self.__store

    def set(self, store):
        if not isinstance(store, dict):
            raise TypeError('store must be of type dictionary')
        self.__store = store

print('Loading Datastore...')

global data_store
data_store = Datastore()
