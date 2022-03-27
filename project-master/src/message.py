'''
All the message functions needed for the project
'''
import time
import jwt
import data
import error
import threading


def message_send(token, channel_id, message):
    '''
    Check for the user and gets their details from the data,
    Then checks if they are in the channel
    and then sends the message
    '''
    channel_id = int(channel_id)
    decoded_jwt = jwt.decode(token.encode('utf-8'), data.secret, algorithms=['HS256'])
    decoded_token = decoded_jwt['token']
    if len(message) > 1000:
        raise error.InputError("Message too long")
    current_user = {}
    # Check if a user exists with thier token
    for user in data.users:
        if user['token'] == decoded_token:
            current_user['u_id'] = user['u_id']
            current_user['name_first'] = user['name_first']
            current_user['name_last'] = user['name_last']
        
    new_message_id = 0
    found = False
    #Check if the user exists in the channel
    for channel in data.channels:
        if channel['channel_id'] == channel_id:
            for member in channel['all_members']:
                if member['u_id'] == current_user['u_id']:
                    new_message_id = data.num_messages + 1
                    data.num_messages += 1
                    found = True
                    break
            if not found:
                raise error.AccessError("User could not be found")

    #Get all the data needed for the message dict and append it
    current_time = int(time.time())
    new_message = {
        'message_id' : new_message_id,
        'u_id' : current_user['u_id'],
        'message' : message,
        'time_created' : current_time,
        'reacts' : [],
        'is_pinned' : False,
    }
    if 'messages' not in data.channels[channel_id - 1]:
        data.channels[channel_id - 1]['messages'] = []
        data.channels[channel_id - 1]['messages'].append(new_message)
    else:
        data.channels[channel_id - 1]['messages'].append(new_message)

    return {
        'message_id': new_message_id,
    }


def message_remove(token, message_id):
    '''
    Checks for the message in the messages list,
    and checks the permissions of the user (if they sent the message or they are in 
    owner_members) and then removes the message from the list
    '''
    decoded_jwt = jwt.decode(token.encode('utf-8'), data.secret, algorithms=['HS256'])
    decoded_token = decoded_jwt['token']
    current_user = {}
    user_valid = False
    for user in data.users:
        if user['token'] == decoded_token:
            current_user['u_id'] = user['u_id']
            current_user['name_first'] = user['name_first']
            current_user['name_last'] = user['name_last']


    
    message_found = False
    for channel in data.channels:
        # check if user is an owner
        for owner_members in channel['owner_members']:
            if owner_members['u_id'] == current_user['u_id']:
                user_valid = True

        # check if there are any messages in the channel
        if 'messages' not in channel:
            if data.channels[data.num_channels - 1] == channel:
                raise error.InputError('No messages exist in any channels')
        
        #check for the message, and remove it if found
        if 'messages' in channel:
            for message in channel['messages']:
                if message['message_id'] == message_id:
                    message_found = True
                    if user_valid:
                        channel['messages'].remove(message)
                    elif message['u_id'] == current_user['u_id']:
                        user_valid = True
                        channel['messages'].remove(message)
                    break
        
    if not user_valid:
        raise error.AccessError('You do not have the required permissions')

    if not message_found:
        raise error.InputError('Message was not found')
                
    return {
    }

def message_edit(token, message_id, message):
    '''
    - get the user from their token
    - get message from the message_id
    - check if the user is either an owner or mesasge creator
    - edit the message
    - put back into the data dictionary
    '''
    decoded_jwt = jwt.decode(token.encode('utf-8'), data.secret, algorithms=['HS256'])
    decoded_token = decoded_jwt['token']
    user_valid = False
    current_user = {}
    for user in data.users:
        if user['token'] == decoded_token:
            current_user['u_id'] = user['u_id']
            current_user['name_first'] = user['name_first']
            current_user['name_last'] = user['name_last']


    for channel in data.channels:
        # check if user is an owner
        for owner_members in channel['owner_members']:
            if owner_members['u_id'] == current_user['u_id']:
                user_valid = True

        # Check if the user is valid and then edit the message in the messages list
        for current_message in channel['messages']:
            if current_message['message_id'] == message_id:
                if not user_valid:
                    if current_message['u_id'] == current_user['u_id']:
                        user_valid = True
                        current_message['message'] = message
                else:
                    if message == "":
                        message_remove(token, message_id)
                    else:
                        current_message['message'] = message

    if not user_valid:
        raise error.AccessError
    return {
    }

def message_react(token, message_id, react_id):
    '''
    Find user via token,
    Check if react_id is valid
    search for message via message_id
    set react fields in message dict
    '''
    decoded_jwt = jwt.decode(token.encode('utf-8'), data.secret, algorithms=['HS256'])
    decoded_token = decoded_jwt['token']
    current_user = {}
    message_found = False
    react_id = int(react_id)
    message_id = int(message_id)
    for user in data.users:
        if user['token'] == decoded_token:
            current_user['u_id'] = user['u_id']
            current_user['name_first'] = user['name_first']
            current_user['name_last'] = user['name_last']
            current_user['profile_img_url'] = user['profile_img_url']
    
    if react_id != 1:
        raise error.InputError("Invalid react id")


    for channel in data.channels:
        for current_message in channel['messages']:
            if current_message['message_id'] == message_id:
                message_found = True
                if current_message['reacts'] == []:
                    react_to_append = {
                        'react_id' : react_id,
                        'u_ids' : [],
                        'is_this_user_reacted' : False
                    }
                    react_to_append['u_ids'].append(current_user['u_id'])
                    current_message['reacts'].append(react_to_append)
                else:
                    if current_user['u_id'] in current_message['reacts'][0]['u_ids']:
                        raise error.InputError("User already reacted")
                    current_message['reacts'][0]['u_ids'].append(current_user['u_id'])
        if not message_found:
            raise error.InputError("Invalid message id")

    return

def message_unreact(token, message_id, react_id):
    '''
    Find user via token
    Check if react_id is valid
    search for message via message_id
    search for react via react_id
    remove the user's u_id from the uids list in the react
    '''
    decoded_jwt = jwt.decode(token.encode('utf-8'), data.secret, algorithms=['HS256'])
    decoded_token = decoded_jwt['token']
    current_user = {}
    message_found = False
    react_found = False
    react_id = int(react_id)
    message_id = int(message_id)
    for user in data.users:
        if user['token'] == decoded_token:
            current_user['u_id'] = user['u_id']
            current_user['name_first'] = user['name_first']
            current_user['name_last'] = user['name_last']
            current_user['profile_img_url'] = user['profile_img_url']



    for channel in data.channels:

        for current_message in channel['messages']:
            if current_message['message_id'] == message_id:
                message_found = True
                for react in current_message['reacts']:
                    if react['react_id'] == react_id:
                        react_found = True
                        if current_user['u_id'] in react['u_ids']:
                            react['u_ids'].remove(current_user['u_id'])
                        else:
                            raise error.InputError("User did not react to this message")

        if not message_found:
            raise error.InputError("Invalid message id")
        
        if not react_found:
            raise error.InputError("React id not found")
        

    
    return


def message_pin(token, message_id):
    '''
    given a particular message_id, if the user is an owner of the channel,
    changes the message data to is_pinned = true
    '''
    # decodes the token
    decoded_jwt = jwt.decode(token.encode('utf-8'), data.secret, algorithms=['HS256'])
    decoded_token = decoded_jwt['token']
    current_user = {}
    
    # finds the users information
    for user in data.users:
        if user['token'] == decoded_token:
            current_user['u_id'] = user['u_id']
            current_user['name_first'] = user['name_first']
            current_user['name_last'] = user['name_last']
            current_user['profile_img_url'] = user['profile_img_url']


    for channel in data.channels:
        for message in channel['messages']:
            if message['message_id'] == message_id:
                if current_user in channel['owner_members']:
                    if not message['is_pinned']:
                        message['is_pinned'] = True
                        return {}
                    else:
                        raise error.InputError('Message is already pinned')
                else:
                    raise error.AccessError('User is not an owner')
    raise error.InputError('Message does not exist')

def message_unpin(token, message_id):
    '''
    given a particular message_id, if the user is an owner of the channel,
    changes the message data to is_pinned = false
    '''
    # decodes the token
    decoded_jwt = jwt.decode(token.encode('utf-8'), data.secret, algorithms=['HS256'])
    decoded_token = decoded_jwt['token']
    current_user = {}
    
    # finds the users information
    for user in data.users:
        if user['token'] == decoded_token:
            current_user['u_id'] = user['u_id']
            current_user['name_first'] = user['name_first']
            current_user['name_last'] = user['name_last']
            current_user['profile_img_url'] = user['profile_img_url']


    for channel in data.channels:
        for message in channel['messages']:
            if message['message_id'] == message_id:
                if current_user in channel['owner_members']:
                    if message['is_pinned']:
                        message['is_pinned'] = False
                        return {}
                    else:
                        raise error.InputError('Message is already unpinned')
                else:
                    raise error.AccessError('User is not an owner')
    raise error.InputError('Message does not exist')


def message_sendlater(token, channel_id, message, time_sent):
    current_time = int(time.time())
    if time_sent < current_time:
        raise error.InputError('Time is in the past')
    time_until_send = int(time_sent - current_time)

    channel_id = int(channel_id)
    decoded_jwt = jwt.decode(token.encode('utf-8'), data.secret, algorithms=['HS256'])
    decoded_token = decoded_jwt['token']
    if len(message) > 1000:
        raise error.InputError("Message too long")
    current_user = {}
    # Check if a user exists with thier token
    for user in data.users:
        if user['token'] == decoded_token:
            current_user['u_id'] = user['u_id']
            current_user['name_first'] = user['name_first']
            current_user['name_last'] = user['name_last']
            current_user['profile_img_url'] = user['profile_img_url']
    new_message_id = 0
    user_found = False
    channel_found = False
    #Check if the user exists in the channel
    for channel in data.channels:
        if channel['channel_id'] == channel_id:
            channel_found = True
            for member in channel['all_members']:
                if member['u_id'] == current_user['u_id']:
                    new_message_id = data.num_messages + 1
                    data.num_messages += 1
                    user_found = True
                    break
            if not user_found:
                raise error.AccessError("User could not be found")
    if not channel_found:
        raise error.InputError("Channel could not be found")

    new_message = {
        'message_id' : new_message_id,
        'u_id' : current_user['u_id'],
        'message' : message,
        'time_created' : time_sent,
        'reacts' : [],
        'is_pinned' : False,
    }
    
    t = threading.Timer(time_until_send, thread_message_send, args=(channel_id, new_message))
    t.start()

    return new_message_id


def thread_message_send(channel_id, new_message):
    if 'messages' not in data.channels[channel_id - 1]:
        data.channels[channel_id - 1]['messages'] = []
        data.channels[channel_id - 1]['messages'].append(new_message)
    else:
        data.channels[channel_id - 1]['messages'].append(new_message)
    return
