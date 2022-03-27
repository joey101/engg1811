'''
All the channels functions need to create and list channels
for the project
'''
import jwt
import data
import error



# lists all the channels the user is a part of
def channels_list(token):
    channels = {}
    list_channels = []

    # lookup the user with their token, and save that
    # in current_user
    decoded_jwt = jwt.decode(token.encode('utf-8'), data.secret, algorithms=['HS256'])
    decoded_token = decoded_jwt['token']
    current_user = {}
    for user in data.users:
        if user['token'] == decoded_token:
           current_user = user
    
    # loop through all the channels, check if the user is
    # a part of that channel (in all_members) by looking for
    # their user id, and then append that channel to the channel_list
    for channel in data.channels:
        for users in channel['all_members']:
            if current_user['u_id'] == users['u_id']:
                channel_append = {}
                channel_append['channel_id'] = channel['channel_id']
                channel_append['name'] = channel['name']
                list_channels.append(channel_append)

    channels['channels'] = list_channels

    return channels

# lists all the channels
def channels_listall(token):
    channels = {}
    channels_list = []

    # loop through all the channels and 
    # append them to the channel_list
    for channel in data.channels:
        channel_append = {}
        channel_append['channel_id'] = channel['channel_id']
        channel_append['name'] = channel['name']
        channels_list.append(channel_append)

    channels['channels'] = channels_list 

    return channels

# creates a channel
def channels_create(token, name, is_public):
    decoded_jwt = jwt.decode(token.encode('utf-8'), data.secret, algorithms=['HS256'])
    decoded_token = decoded_jwt['token']
    # check if the legnth of the channel name is above
    # 20 characters
    if len(name) > 20:
        raise error.InputError("Length of name is longer than 20 characters")

    new_channel = {}
    new_channel['channel_id'] = data.num_channels + 1
    new_channel['name'] = name
    new_channel['is_public'] = is_public
    new_channel['standup_endtime'] = None
    new_channel['standup_conversation'] = []
    data.num_channels += 1

    # look for the user's user dictionary with their
    # token and save the information needed in the
    # owner dictionary and append that to both
    # all_members and owner_members 
    # (the creator of the channel is automatically the owner)
    owner = {}
    for user in data.users:
        if user['token'] == decoded_token:
            owner['u_id'] = user['u_id']
            owner['name_first'] = user['name_first']
            owner['name_last'] = user['name_last']
            owner['profile_img_url'] = user['profile_img_url']

    new_channel['owner_members'] = [owner]
    new_channel['all_members'] = [owner]

    data.channels.append(new_channel)

    return {
        'channel_id': data.channels[data.num_channels - 1]['channel_id']
    }
