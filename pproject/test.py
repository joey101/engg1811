from data_store import data_store

num = 0
channel = data_store.get()
number = channel['users'][0]['id']

ch_info = {
    'id': len(channel['channels']) + 1,
    'name': "new_chan",
    'status': "public",
    'owner': channel['users'][0]['id'],
    'members': '',
}

channel['channels'].append(ch_info)

data_store.set(channel)


print(channel)
