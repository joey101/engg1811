'''
All the functions needed for standups
'''
import time
import threading
import jwt
import message
import data
import error

def token_find_user(token):
    '''Given a user's token, returns the user's info dictionary'''
    required_user = {}
    for user in data.users:
        if user['token'] == token:
            required_user = user

    return required_user

def find_channel(channel_id):
    '''
    Given a channel_id return the required channel dictionary and its index in the channels array
    '''
    required_channel = {}
    channel_not_found = True
    for channel in data.channels:
        if channel['channel_id'] == channel_id:
            required_channel = channel
            channel_not_found = False
            break

    if channel_not_found:
        raise error.InputError(f"Channel with id {channel_id} could not be found")

    return required_channel

def standup_start(token, channel_id, length):
    '''
    When standup start is called, all message sending capabilities should terminate,
    and instead standup_send will be used instead of message_send.

    - Change data.py to include a state for time_finish, an int with amount
     of time left in standup, and if zero, standup has ended

    - Starts a thread for standup end
    '''
    channel_id = int(channel_id)
    find_channel(channel_id)

    if data.channels[channel_id-1]['standup_endtime'] is not None:
        raise error.InputError("Standup is already active")

    decoded_jwt = jwt.decode(token.encode('utf-8'), data.secret, algorithms=['HS256'])
    decoded_token = decoded_jwt['token']

    token_find_user(decoded_token)

    end_time = int(time.time()) + length
    data.channels[channel_id-1]['standup_endtime'] = end_time

    t = threading.Timer(length, standup_end, args=(token, channel_id))
    t.start()

    #time_left = data.channels[channel_id-1]['standup_endtime'] - int(time.time())

    return {'time_finish': end_time}


def standup_end(token, channel_id):
    '''
    This function will send the final message string that accumulates all the individual
    standup messages and then reset all the standup variables in the channel.
    '''
    channel_id = int(channel_id)
    data.channels[channel_id-1]['standup_endtime'] = None

    message_list = data.channels[channel_id-1]['standup_conversation']

    # If no messages are sent during the standup then do nothing
    if message_list == []:
        return

    accumulated_message = ""

    for messages in message_list[:-1]:
        accumulated_message += f"{messages['handle_str']}: {messages['message']}\n"
    accumulated_message += f"{message_list[-1]['handle_str']}: {message_list[-1]['message']}"

    message.message_send(token, channel_id, accumulated_message)

    data.channels[channel_id-1]['standup_conversation'].clear()

def standup_active(token, channel_id):
    '''
    Checks the value in data.py is_standup, if its not zero then its active
    and returns the time_finish
    '''
    decoded_jwt = jwt.decode(token.encode('utf-8'), data.secret, algorithms=['HS256'])
    decoded_token = decoded_jwt['token']

    channel_id = int(channel_id)
    find_channel(channel_id)
    token_find_user(decoded_token)

    if data.channels[channel_id-1]['standup_endtime'] is not None:
        return {
            'is_active': True,
            'time_finish': data.channels[channel_id-1]['standup_endtime']
        }

    return {
        'is_active': False,
        'time_finish': None
    }


def standup_send(token, channel_id, message):
    '''
    Uses standup_active to check if its working, and appends to the standup_message_list
    '''

    decoded_jwt = jwt.decode(token.encode('utf-8'), data.secret, algorithms=['HS256'])
    decoded_token = decoded_jwt['token']

    channel_id = int(channel_id)
    find_channel(channel_id)
    state = standup_active(token, channel_id)

    if len(message) > 1000:
        raise error.InputError("Message too long")

    if not state['is_active']:
        raise error.InputError("A standup is not currently active")

    user = token_find_user(decoded_token)

    is_member = False
    for member in data.channels[channel_id-1]['all_members']:
        if member['u_id'] == user['u_id']:
            is_member = True

    if not is_member:
        raise error.AccessError("User is not in channel")

    data.channels[channel_id-1]['standup_conversation'].append({'handle_str': user['handle_str'], 'message': message})

    return {}
