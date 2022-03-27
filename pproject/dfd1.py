

#print(ds['users'][0]['name'])

'''
def find_channel(channel_id):
    for channel in ds['channels']:
        if channel_id['channel_id'] == channel['id']:
            return channel['id'], channel['name'], channel['status'], channel['owner'], channel['members'], channel['messages']
       
    return -1, 0, 0, 0, 0, 0'''

#def channels_create_v1(auth_user_id, name, is_public):
    '''
        Creates a channel and populates it with all the data.
    '''
    # Checks length of name.
    '''if len(str(name)) > 20:
        raise InputError('Invalid Name: Name is too long.')
    elif len(str(name)) < 1:
        raise InputError('Invalid Name: Name is too short.')

    ds = data_store.get()
    # Checks if same name exists.
    for channel in ds['channels']:
        if name == channel['name']:
            raise InputError('Name exists')
    '''

    ''' channel = {
        'id': len(ds['channels']),
        'name': name,
        'status': is_public,
        'owner': auth_user_id,
        'members': [auth_user_id],
        'messages': ["jawad", "HI"]
        
    }
    
    ds['channels'].append(channel)
    data_store.set(ds)

    return  {
        'channel_id': channel['id'],
    }


    '''
           

    '''
idk = channels_create_v1(0, 'jawad', True)
ch_id, ch_name, ch_status, ch_owner, ch_members, ch_messages = find_channel(idk)

print('new', ch_members, ch_messages)
    '''
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

    '''mail = 'jawad.tanana@gmail.com'
for person in user_info['channels']:
    print(person['members'][2])
    store_user_email = user_info['users'][person]['email']

    if email == store_user_email:
        number = user_info['users'][person]['id']

#channel['channels'].append(ch_info)

data_store.set(user_info)


print(number)
'''