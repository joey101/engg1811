from data_store import data_store

num = 0
user_info = data_store.get()
print(user_info['users'][0]['name'])

'''
ch_info = {
    'id': len(user_info['channels']) + 1,
    'name': "new_chan",
    'status': "public",
    'owner': user_info['users'][0]['id'],
    'members': 'jawad',
}
'''

#print(ch_info['members'])

email = 'jawad.tanana@gmail.com'
for person in user_info['channels']:
    print(person['members'][2])
    '''store_user_email = user_info['users'][person]['email']

    if email == store_user_email:
        number = user_info['users'][person]['id']'''

#channel['channels'].append(ch_info)

data_store.set(user_info)


print(number)
