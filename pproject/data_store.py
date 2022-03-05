data = {
    'users': [
        {
            'id': 1,
            'name' : 'john',
            'email': 'john.tanana@gmail.com',
        },
        {
            'id': 2,
            'name' : 'user2',
            'email': 'jawad.tanana@gmail.com',
        },
    ],
    'channels': [
        {
            'id': 1,
            'name' : 'channel1',
            'members': [1,2,3],
        },
        {
            'id': 2,
            'name' : 'channel2',
            'members': [1,2,3],
        },
    ],
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
