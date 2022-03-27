'''
All the other functions needed for the project
'''
import jwt
import data
import error


def clear():
    '''
    Clears all the data that exists in data.py
    '''
    data.users = []
    data.channels = []
    data.num_channels = 0
    data.num_users = 0
    data.num_messages = 0
    

def users_all(token):
    '''
    Lists all users that exist on the flockr
    '''
    users_list = []

    for user in data.users:
        user_to_append = {
            'u_id' : user['u_id'],
            'email' : user['email'],
            'name_first' : user['name_first'],
            'name_last' : user['name_last'],
            'handle_str' : user['handle_str'],
            'profile_img_url' : user['profile_img_url']
        }
        users_list.append(user_to_append)
    return {'users' : users_list}

def admin_userpermission_change(token, u_id, permission_id):
    '''
    This function sets the permissions of the given user:
    permission_id 1: owner
    permission_id 2: member
    '''
    decoded_jwt = jwt.decode(token.encode('utf-8'), data.secret, algorithms=['HS256'])
    decoded_token = decoded_jwt['token']
    u_id = int(u_id)
    permission_id = int(permission_id)
    current_user = {}
    # Search for the user and get their permissions
    for user in data.users:
        if decoded_token == user['token']:
            current_user['u_id'] = user['u_id']
            current_user['permission_id'] = user['permission_id']

    # Check if the users using this function has the correct
    # permissions
    if current_user['permission_id'] != 1:
        raise error.AccessError('You do not have owner permissions')

    # Obtain the data needed to change the specified user's
    # permissions
    user_edited = {}
    member_found = False
    for user in data.users:
        if user['u_id'] == u_id:
            member_found = True
            if permission_id not in (1, 2):
                raise error.InputError
           
            user['permission_id'] = permission_id

            user_edited['name_first'] = user['name_first']
            user_edited['name_last'] = user['name_last']
            user_edited['u_id'] = user['u_id']
            user_edited['profile_img_url'] = user['profile_img_url']
        
    if not member_found:
        raise error.InputError('User with requested u_id not found')

    # Sets the user's status in the channels to owner_member in the channels they are in
    if permission_id == 1:
        for channel in data.channels:
            if user_edited not in channel['owner_members'] and user_edited in channel['all_members']:
                channel['owner_members'].append(user_edited)
    else:
        # Revoke's the user's onwer_member status for the channels they are in
        for channel in data.channels:
            if user_edited in channel['owner_members']:
                channel['owner_members'].remove(user_edited)   



def search(token, query_str):
    '''
    This function searches for messages with a query string
    '''
    decoded_jwt = jwt.decode(token.encode('utf-8'), data.secret, algorithms=['HS256'])
    decoded_token = decoded_jwt['token']
    # uses the token to find the user infomation
    current_user = {}
    for user in data.users:
        if user['token'] == decoded_token:
            current_user['u_id'] = user['u_id']
            current_user['name_first'] = user['name_first']
            current_user['name_last'] = user['name_last']
            current_user['profile_img_url'] = user['profile_img_url']

    # checks which channels the user is in and
    # searches them for messages containing the query_str
    return_list = []
    for channel in data.channels:
        if current_user in channel['all_members']:
            for message in channel['messages']:
                if query_str in message['message']:
                    return_list.append(message)
    return {
        'messages': return_list
    }
