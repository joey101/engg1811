import data
import error
import jwt

# Given a channel_id return the required channel dictionary and its index in the channels array
def find_channel(channel_id):
    required_channel = {}
    channel_not_found = True
    for channel in data.channels:
        if channel['channel_id'] == channel_id:
            required_channel = channel
            #channel_is_public = channel['is_public']
            channel_not_found = False
            break

    if channel_not_found:
        raise error.InputError("Channel could not be found")

    return required_channel

# Given a u_id, returns the user's info dictionary
def find_user(u_id):
    user_not_found = True
    required_user = {}
    for user in data.users:
        if user['u_id'] == u_id:
            required_user = user
            user_not_found = False
            break

    if user_not_found:
        raise error.InputError("User could not be found")

    return required_user

# Given a user's token, returns the user's info dictionary
def token_find_user(token):
    required_user = {}
    for user in data.users:
        if user['token'] == token:
            required_user = user

    return required_user

# A user with a token invites a user with a certain u_id to join a channel with a certain channel_id
def channel_invite(token, channel_id, u_id):
    # The user with id :u_id will be added to the server
    channel_id = int(channel_id)
    u_id = int(u_id)
    decoded_jwt = jwt.decode(token.encode('utf-8'), data.secret, algorithms=['HS256'])
    decoded_token = decoded_jwt['token']
    inviter = token_find_user(decoded_token)
    required_channel = find_channel(channel_id)

    invited_user = {}
    invited_user_dict = find_user(u_id)

    #
    invited_user['u_id'] = u_id
    invited_user['name_first'] = invited_user_dict['name_first']
    invited_user['name_last'] = invited_user_dict['name_last']
    invited_user['profile_img_url'] = invited_user_dict['profile_img_url']
    permission = invited_user_dict['permission_id']

    if not required_channel['is_public']: # If channel is private
        # Find the u_id of the owner and ensure the u_id is a part of the owned members field
        is_owner = False
        for owned_member in required_channel['owner_members']:
            if owned_member['u_id'] == inviter['u_id']: #if owner is found in owned_members
                is_owner = True

        if not is_owner: # If the inviter is not an owner of the private channel
            raise error.AccessError(description="Inviter is not owner of private channel")
    else:  # if channel is public
        is_part_of_channel = False
        # Check if the user is part of the all_members in the channel
        for member in required_channel['all_members']:
            if member['u_id'] == inviter['u_id']:
                is_part_of_channel = True

        
        if not is_part_of_channel:
            raise error.AccessError(description="Inviter is not owner of public channel")


    # Check if user is in channel
    for member in required_channel['all_members']:
        if member['u_id'] == u_id:
            raise error.AccessError(description="Invited user is already part of channel")


    required_channel['all_members'].append(invited_user)
    if permission == 1:
        required_channel['owner_members'].append(invited_user)
    return

# Will return details about the channel including name, owner_members and all members
def channel_details(token, channel_id):
    decoded_jwt = jwt.decode(token.encode('utf-8'), data.secret, algorithms=['HS256'])
    decoded_token = decoded_jwt['token']
    channel_id = int(channel_id)
    current_user = token_find_user(decoded_token)
    returned_channel = {}
    channel = find_channel(channel_id)
    user_found = False
    for user in channel['all_members']:
        if user['u_id'] == current_user['u_id']:
            user_found = True

    if user_found == False:
        raise error.AccessError(description='User not found in channel')
    
    returned_channel['name'] = channel['name']
    returned_channel['owner_members'] = channel['owner_members']
    returned_channel['all_members'] = channel['all_members']

    return returned_channel

# searches through the messages in the channel and returns up to 50 messages
def channel_messages(token, channel_id, start):

    decoded_jwt = jwt.decode(token.encode('utf-8'), data.secret, algorithms=['HS256'])
    decoded_token = decoded_jwt['token']
    channel_id = int(channel_id)
    start = int(start)
    # Checks if the token and channel_id are correct
    messages_in_channel = []
    check_user = False
    channel_found = False
    messages_exist = False
    user_id = 0
    for channel in data.channels:
        if channel_id == channel['channel_id']:
            channel_found = True
            # check if there are any in the channel
            if 'messages' in channel:
                messages_in_channel = channel['messages']
                messages_exist = True
            for member in channel['all_members']:
                if member['u_id'] == decoded_token:
                    check_user = True
                    user_id = member['u_id']
            break

    # raises InputError if no channel exists at the channel_id
    if not channel_found:
        raise error.InputError(description="Specified channel does not exist")

    # raises AccessError if token is not in the channel
    if not check_user:
        raise error.AccessError(description="user is not part of the channel")

    # check if the messages do not exist in the channel
    if not messages_exist:
        return {
                'messages' : [],
                'start' : start,
                'end' : -1
            }
    # start is to large for the number of messages
    if len(messages_in_channel) - start <= 0:

        # messages list in channel is empty, hence return empty list
        if len(messages_in_channel) - start == 0 and start == 0:
            return {
                'messages' : [],
                'start' : start,
                'end' : -1
            }
        raise error.InputError(description="Start num too large")

    messages = []
    end = start + 50
    length = len(messages_in_channel)
    i = 1
    # adds each message from start to start+50 to messages[] 
    while i < 51:
        messages.append(messages_in_channel[length - start - i])
        if i + start >= length:
            break
        i = i + 1
    if len(messages) == 50:
        if (len(messages_in_channel) - end == 0):
            end = -1
        else:
            end = start + 50
    else:
        end = -1

    # set is_this_user_reacted flag for messages user has reacted to
    for message in messages:
        for react in message['reacts']:
            if user_id in react['u_ids']:
                react['is_this_user_reacted'] = True
            else:
                react['is_this_user_reacted'] = False
    
    # creates dictionary for return
    message_list = {
        'messages' : messages,
        'start' : start,
        'end' : end
    }
    return message_list


# removes a user from the given channel
def channel_leave(token, channel_id):
    channel_id = int(channel_id)
    decoded_jwt = jwt.decode(token.encode('utf-8'), data.secret, algorithms=['HS256'])
    decoded_token = decoded_jwt['token']
    user = token_find_user(decoded_token)
    # checks if user is in channel
    channel = find_channel(channel_id)
    check_user = 0
    for channel in data.channels:
        if channel['channel_id'] == channel_id:
            for member in channel['all_members']:
                if member['u_id'] == user['u_id']:
                    check_user = 1

    if check_user == 0:
        raise error.AccessError # user not part of channel
    
    # removes the user from the channel
    member_to_remove = {}
    for member in channel['all_members']:
        if member['u_id'] == user['u_id']:
            member_to_remove = member
    channel['all_members'].remove(member_to_remove)
            
    return 


# adds given user to given channel
def channel_join(token, channel_id):
    channel_id = int(channel_id)
    decoded_jwt = jwt.decode(token.encode('utf-8'), data.secret, algorithms=['HS256'])
    decoded_token = decoded_jwt['token']
    # checks if the channel exists and is public
    check = 0
    for channel in data.channels:
        if channel['channel_id'] == channel_id:
            if not channel['is_public']:
                raise error.AccessError(description="Channel is not public")
            check = 1
            break
    if check != 1:
        raise error.InputError(description="channel id is invalid")
    # adds user to channel_members
    user_data = {}
    permission = 0
    for user in data.users:
        if user['token'] == decoded_token:
            user_data['u_id'] = user['u_id']
            user_data['name_first'] = user['name_first']
            user_data['name_last'] = user['name_last']
            user_data['profile_img_url'] = user['profile_img_url']
            permission = user['permission_id']

    channel['all_members'].append(user_data)
    if permission == 1:
        channel['owner_members'].append(user_data)

    return


# An owner of a channel with a certain channel_id that has a certain token will add a user with u_id as an owner
def channel_addowner(token, channel_id, u_id):

    # ORDER OF BUSINESS:
    # 1. Find the first name and last name of the user with u_id
    # 2. Ensure that the owner with th
    # 3. Ensure the user being added as an owner is not already an owner
    # 4. Ensure that the user adding the user as an owner is an owner themself
    # 5. Ensure that the user being added as an owner is a part of the channel to begin with
    channel_id = int(channel_id)
    u_id = int(u_id)
    decoded_jwt = jwt.decode(token.encode('utf-8'), data.secret, algorithms=['HS256'])
    decoded_token = decoded_jwt['token']
    owner = token_find_user(decoded_token)
    channel = find_channel(channel_id)
    user_added_as_owner = {}
    user_added_as_owner_dict = find_user(u_id)

    user_added_as_owner['u_id'] = user_added_as_owner_dict['u_id']
    user_added_as_owner['name_first'] = user_added_as_owner_dict['name_first']
    user_added_as_owner['name_last'] = user_added_as_owner_dict['name_last']
    user_added_as_owner['profile_img_url'] = user_added_as_owner_dict['profile_img_url']

    # 3. Ensure the user being added is not already an owner
    for user in channel['owner_members']:
        if user['u_id'] == user_added_as_owner['u_id']:
            raise error.InputError(description="User is already an owner of this channel")

    # 4. Ensure that the user adding another user as an owner is an owner themself
    user_is_owner = False
    for user in channel['owner_members']:
        if user['u_id'] == owner['u_id']:
            user_is_owner = True
            #break

    if user_is_owner == False:
        raise error.AccessError(description="User attempting to add an owner is not an owner themself")


    # Ensure that the user being added as owner is in the channel
    user_in_channel = False
    for user in channel['all_members']:
        if user['u_id'] == user_added_as_owner['u_id']:
            user_in_channel = True
    if not user_in_channel:
        raise error.AccessError(description="User to be added as owner is not part of the channel")

    channel['owner_members'].append(user_added_as_owner)

    return

# Will remove an owner from the list of owned_members
def channel_removeowner(token, channel_id, u_id):

    # ORDER OF BUSINESS
    # 1. The user removing ownership from a user is an owner
    # 2. The user being removed as owner is an owner
    channel_id = int(channel_id)
    u_id = int(u_id)
    decoded_jwt = jwt.decode(token.encode('utf-8'), data.secret, algorithms=['HS256'])
    decoded_token = decoded_jwt['token']
    owner = token_find_user(decoded_token)
    channel = find_channel(channel_id)
    owner_to_remove = {}
    owner_to_remove_dict = find_user(u_id)

    owner_to_remove['u_id'] = owner_to_remove_dict['u_id']
    owner_to_remove['name_first'] = owner_to_remove_dict['name_first']
    owner_to_remove['name_last'] = owner_to_remove_dict['name_last']
    owner_to_remove['profile_img_url'] = owner_to_remove_dict['profile_img_url']
    # 1. Ensure the user doing the removing is an owner of the channel
    user_is_owner = False
    for user in channel['owner_members']:
        if user['u_id'] == owner['u_id']:
            user_is_owner = True
    if user_is_owner == False:
        raise error.AccessError(description="User attempting to remove an owner is not an owner themself")

    # 2. Ensure user being removed as owner is an owner of the channel
    user_is_owner = False
    for user in channel['owner_members']:
        if user['u_id'] == owner_to_remove['u_id']:
            user_is_owner = True
    if user_is_owner == False:
        raise error.InputError(description="User being removed as owner, is not an owner to begin with")


    channel['owner_members'].remove(owner_to_remove)

    return