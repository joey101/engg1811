import channel
import channels
import message
import pytest
import auth
import data
import other
from error import InputError
from error import AccessError

#   test channel_details for one channel with only one user
def test_channel_details_one_user():
    other.clear()

    user_1 = auth.auth_register("example@example.com", "abcd1234", "John", "Smith")
    test_channel = channels.channels_create(user_1['token'], "Test Channel", True)
    assert channel.channel_details(user_1['token'], test_channel['channel_id']) == {
        'name' : "Test Channel",
        'owner_members' : [
            {
                'u_id' : 1,
                'name_first' : "John",
                'name_last' : "Smith",
                'profile_img_url' : ""
            }
        ],
        'all_members' : [
            {
                'u_id' : 1,
                'name_first' : "John",
                'name_last' : "Smith",
                'profile_img_url' : ""
            }
        ]
    }

    other.clear()

#   test channel details for one channel with more than one user
def test_channel_details_two_users():
    other.clear()

    user_1 = auth.auth_register("example@example.com", "abcd1234", "John", "Smith")
    user_2 = auth.auth_register("example1@example.com", "abcd1234", "Will", "Smith")
    channel_1 = channels.channels_create(user_1['token'], "Test Channel", True)
    channel.channel_join(user_2['token'], channel_1['channel_id'])
    assert channel.channel_details(user_1['token'], channel_1['channel_id']) == {
        'name' : "Test Channel",
        'owner_members' : [
            {
                'u_id' : 1,
                'name_first' : "John",
                'name_last' : "Smith",
                'profile_img_url' : ""
            }
        ],
        'all_members' : [
            {
                'u_id' : 1,
                'name_first' : "John",
                'name_last' : "Smith",
                'profile_img_url' : ""
            },
            {
                'u_id' : 2,
                'name_first' : "Will",
                'name_last' : "Smith",
                'profile_img_url' : ""
            }
        ]
    }

    other.clear()

#   test channel details for a private channel
def test_channel_details_private():
    other.clear()

    user_1 = auth.auth_register("example@example.com", "abcd1234", "John", "Smith")
    channel_1 = channels.channels_create(user_1['token'], "Test Channel", False)
    assert channel.channel_details(user_1['token'], channel_1['channel_id']) == {
        'name' : "Test Channel",
        'owner_members' : [
            {
                'u_id' : 1,
                'name_first' : "John",
                'name_last' : "Smith",
                'profile_img_url' : ""
            }
        ],
        'all_members' : [
            {
                'u_id' : 1,
                'name_first' : "John",
                'name_last' : "Smith",
                'profile_img_url' : ""
            },
        ]
    }

    other.clear()

#   checks error handling of invalid channel id for channel_details
def test_channel_details_wrong_id():
    other.clear()

    user_1 = auth.auth_register("example@example.com", "abcd1234", "John", "Smith")
    channels.channels_create(user_1['token'], "Test Channel", True)
    with pytest.raises(InputError):
        channel.channel_details(user_1['token'], 2)

    other.clear()

#   checks for access error when a user uses channel_details for a
#   channel they arent a part of
def test_channel_details_access_error():
    other.clear()

    user_1 = auth.auth_register("example@example.com", "abcd1234", "John", "Smith")
    user_2 = auth.auth_register("example2@example.com", "abcd1234", "Will", "Smith")
    channel_1 = channels.channels_create(user_1['token'], "Test Channel", False)
    with pytest.raises(AccessError):
       channel.channel_details(user_2['token'], channel_1['channel_id'])

    other.clear()


# basic test for inviting a user to a channel
def test_channel_invite1():
    other.clear()

    owner = auth.auth_register("user1@email.com", "password", "Homer", "Simpson")
    inved_user = auth.auth_register("user2@email.com", "password", "Bart", "Simpson")

    channel_1 = channels.channels_create(owner['token'], "channel_1", False) #this channel will be private

    channel.channel_invite(owner['token'], channel_1["channel_id"], inved_user['u_id'])

    owner_dict = {'u_id': owner['u_id'], 'name_first': 'Homer', 'name_last': 'Simpson',
                'profile_img_url' : ""}
    inved_user_dict = {'u_id': inved_user['u_id'], 'name_first': 'Bart', 'name_last': 'Simpson',
                'profile_img_url' : ""}
    assert channel.channel_details(inved_user['token'], channel_1['channel_id']) == {
        'name': 'channel_1',
        'owner_members': [owner_dict],
        'all_members': [owner_dict, inved_user_dict]
    }


# exception testing for inviting to an invalid channel (invalid channel_id)
def test_channel_invite_invalid_channel():
    other.clear()
    # "owner" will invite a user to a channel that does not exist
    owner = auth.auth_register("user1@email.com", "password", "Homer", "Simpson")
    inved_user = auth.auth_register("user2@email.com", "password", "Bart", "Simpson")

    with pytest.raises(InputError):
        channel.channel_invite(owner['token'], 9999, inved_user['u_id']) #invalid channel_id


# exception testing for inviting a user that does not exist (invalid u_id)
def test_channel_invite_invalid_user():

    other.clear()
    # owner will invite a user that does not exist to a channel
    owner = auth.auth_register("user1@email.com", "password", "Homer", "Simpson")
    #inved_user = auth.auth_register("user2@email.com", "password", "Bart", "Simpson")
    channel_1 = channels.channels_create(owner['token'], "channel_1", False)

    with pytest.raises(InputError):
        channel.channel_invite(owner['token'], channel_1['channel_id'], 9999) #invalid userID


# exception testing for an unauthorised user trying to invite users to a channel
def test_channel_invite_unauthorised_user():

    other.clear()
    # owner will have a channel in which random_user1 and random_user2 are not a part of
    # and random_user1 will try to invite random_user2 to the owner's channel

    owner = auth.auth_register("user1@email.com", "password", "Homer", "Simpson")
    random_user1 = auth.auth_register("user2@email.com", "password", "Bart", "Simpson")
    random_user2 = auth.auth_register("user3@email.com", "password", "Lisa", "Simpson")

    channel_1 = channels.channels_create(owner['token'], "channel_1", False)

    with pytest.raises(AccessError):
        channel.channel_invite(random_user1['token'], channel_1['channel_id'], random_user2['u_id'])

# exception testing for an unauthorised user trying to invite users to a public channel
def test_channel_invite_unauthorised_user_public_channel():

    other.clear()
    # owner will have a channel in which random_user1 and random_user2 are not a part of
    # and random_user1 will try to invite random_user2 to the public channel

    owner = auth.auth_register("user1@email.com", "password", "Homer", "Simpson")
    random_user1 = auth.auth_register("user2@email.com", "password", "Bart", "Simpson")
    random_user2 = auth.auth_register("user3@email.com", "password", "Lisa", "Simpson")

    channel_1 = channels.channels_create(owner['token'], "channel_1", True)

    with pytest.raises(AccessError):
        channel.channel_invite(random_user1['token'], channel_1['channel_id'], random_user2['u_id'])

# test that user with their permissions changed is able to be invited to a channel
def test_channel_invite_user_permission_changed():
    other.clear()
    owner = auth.auth_register("user1@email.com", "password", "Homer", "Simpson")
    random_user1 = auth.auth_register("user2@email.com", "password", "Bart", "Simpson")

    channel_1 = channels.channels_create(owner['token'], "channel_1", True)
    other.admin_userpermission_change(owner['token'], random_user1['u_id'], 1)

    channel.channel_invite(owner['token'], channel_1['channel_id'], random_user1['u_id'])


def test_channel_invite_user_already_in_channel():
    '''
    Test that an AccessError is raised when a user attempts to invite another user
    that is already in the channel
    '''
    other.clear()
    owner = auth.auth_register("user1@email.com", "password", "Homer", "Simpson")
    random_user1 = auth.auth_register("user2@email.com", "password", "Bart", "Simpson")

    channel_1 = channels.channels_create(owner['token'], "channel_1", True)
    
    channel.channel_invite(owner['token'], channel_1['channel_id'], random_user1['u_id'])

    with pytest.raises(AccessError):
        channel.channel_invite(owner['token'], channel_1['channel_id'], random_user1['u_id'])


# tests channel_messages with an invalid channel id
def test_channel_messages_invalid_id():
    other.clear()

    user1 = auth.auth_register("example@example.com", "abcd1234", "John", "Smith")
    # checks that what channel_messages returns is equal to the expected return
    with pytest.raises(InputError):
        channel.channel_messages(user1['token'], 1, 1)

    other.clear()


# Testing for if another owner is added succesfully after calling channel_addowner for a private channel
def test_channel_addowner_private_channel():
    other.clear()

    # we assume that the user that is being added as an owner is already a part of the channel

    # The owner creates a private channel and invites user1 to the channel and then adds them as a owner

    owner = auth.auth_register("howner@email.com", "password", "Homer", "Simpson")
    user1 = auth.auth_register("user1@email.com", "password", "Bart", "Simpson")

    channel_1 = channels.channels_create(owner['token'], "channel_1", False)
    channel.channel_invite(owner['token'], channel_1["channel_id"], user1['u_id']) #assumes channel_invite works

    channel.channel_addowner(owner['token'], channel_1['channel_id'], user1['u_id'])

    owner_dict = {'u_id': owner['u_id'], 'name_first': 'Homer', 'name_last': 'Simpson',
                'profile_img_url' : ""}
    user1_dict = {'u_id': user1['u_id'], 'name_first': 'Bart', 'name_last': 'Simpson',
                'profile_img_url' : ""}
    assert channel.channel_details(user1['token'], channel_1['channel_id']) == {
        'name': 'channel_1',
        'owner_members': [owner_dict, user1_dict],
        'all_members': [owner_dict, user1_dict]
    }

    other.clear()

# Testing for if another owner is added succesfully after calling channel_addowner for a public channel
def test_channel_addowner_public_channel():
    other.clear()
    # we assume that the user that is being added as an owner is already a part of the channel

    # The owner creates a public channel and invites user1 to the channel and then adds them as a owner

    owner = auth.auth_register("howner@email.com", "password", "Homer", "Simpson")
    user1 = auth.auth_register("user1@email.com", "password", "Bart", "Simpson")

    channel_1 = channels.channels_create(owner['token'], "channel_1", True)
    channel.channel_invite(owner['token'], channel_1["channel_id"], user1['u_id']) #assumes channel_invite works

    channel.channel_addowner(owner['token'], channel_1['channel_id'], user1['u_id'])

    owner_dict = {'u_id': owner['u_id'], 'name_first': 'Homer', 'name_last': 'Simpson',
                'profile_img_url' : ""}
    user1_dict = {'u_id': user1['u_id'], 'name_first': 'Bart', 'name_last': 'Simpson',
                'profile_img_url' : ""}
    assert channel.channel_details(user1['token'], channel_1['channel_id']) == {
        'name': 'channel_1',
        'owner_members': [owner_dict, user1_dict],
        'all_members': [owner_dict, user1_dict]
    }

    other.clear()

# Exception testing for if an user is being added as an owner in an invalid channel (channel that doesn't exist)
def test_channel_addowner_invalid_channel():
    other.clear()

    owner = auth.auth_register("howner@email.com", "password", "Homer", "Simpson")
    user1 = auth.auth_register("user1@email.com", "password", "Bart", "Simpson")

    channel_1 = channels.channels_create(owner['token'], "channel_1", False)
    channel.channel_invite(owner['token'], channel_1["channel_id"], user1['u_id']) # Assumes channel_invite works

    with pytest.raises(InputError):
        channel.channel_addowner(owner['token'], 9999, user1['u_id']) #invalid channel_id (9999)

    other.clear()

# Exception testing for if an user being added as owner is not in channel
def test_channel_addowner_user_not_in_channel():
    other.clear()

    owner = auth.auth_register("howner@email.com", "password", "Homer", "Simpson")
    user1 = auth.auth_register("user1@email.com", "password", "Bart", "Simpson")

    channel_1 = channels.channels_create(owner['token'], "channel_1", False)

    with pytest.raises(AccessError):
        channel.channel_addowner(owner['token'], channel_1['channel_id'], user1['u_id']) #invalid channel_id (9999)

    other.clear()

# Exception testing for adding a user as owner if they are already an owner
def test_channel_addowner_already_owner():
    other.clear()

    owner = auth.auth_register("howner@email.com", "password", "Homer", "Simpson")
    user1 = auth.auth_register("user1@email.com", "password", "Bart", "Simpson")

    channel_1 = channels.channels_create(owner['token'], "channel_1", False)
    channel.channel_invite(owner['token'], channel_1["channel_id"], user1['u_id']) # Assumes channel_invite works

    channel.channel_addowner(owner['token'], channel_1['channel_id'], user1['u_id'])

    with pytest.raises(InputError):
        channel.channel_addowner(owner['token'], channel_1['channel_id'], user1['u_id'])

    other.clear()

# Exception testing for if a user that is not an owner, is attempting to add another user as an owner
def test_channel_addowner_non_owner_adding():
    other.clear()

    owner = auth.auth_register("howner@email.com", "password", "Homer", "Simpson")
    user1 = auth.auth_register("user1@email.com", "password", "Bart", "Simpson")
    user2 = auth.auth_register("user2@email.com", "password", "Lisa", "Simpson")

    # owner will create a channel and add two users to the channel
    channel_1 = channels.channels_create(owner['token'], "channel_1", False)
    channel.channel_invite(owner['token'], channel_1["channel_id"], user1['u_id']) # Assumes channel_invite works
    channel.channel_invite(owner['token'], channel_1["channel_id"], user2['u_id'])

    # User1 will attempt to add user2 as an owner which should raise an exception
    with pytest.raises(AccessError):
        channel.channel_addowner(user1['token'], channel_1["channel_id"], user2['u_id'])

    other.clear()

# Testing if an owner can be removed from a private channel using channel_removeowner
def test_channel_removeowner_private_channel():
    other.clear()


    # The owner creates a private channel and invites user1 to the channel and then adds them as a owner
    owner = auth.auth_register("howner@email.com", "password", "Homer", "Simpson")
    user1 = auth.auth_register("user1@email.com", "password", "Bart", "Simpson")

    channel_1 = channels.channels_create(owner['token'], "channel_1", False)
    channel.channel_invite(owner['token'], channel_1["channel_id"], user1['u_id']) #assumes channel_invite works

    #user 1 is added as an owner
    channel.channel_addowner(owner['token'], channel_1['channel_id'], user1['u_id'])

    owner_dict = {'u_id': owner['u_id'], 'name_first': 'Homer', 'name_last': 'Simpson',
                'profile_img_url' : ""}
    user1_dict = {'u_id': user1['u_id'], 'name_first': 'Bart', 'name_last': 'Simpson',
                'profile_img_url' : ""}
    assert channel.channel_details(user1['token'], channel_1['channel_id']) == {
        'name': 'channel_1',
        'owner_members': [owner_dict, user1_dict],
        'all_members': [owner_dict, user1_dict]
    }

    #user 1 is then removed as being an owner
    channel.channel_removeowner(owner['token'], channel_1['channel_id'], user1['u_id'])

    owner_dict = {'u_id': owner['u_id'], 'name_first': 'Homer', 'name_last': 'Simpson',
                'profile_img_url' : ""}
    user1_dict = {'u_id': user1['u_id'], 'name_first': 'Bart', 'name_last': 'Simpson',
                'profile_img_url' : ""}
    assert channel.channel_details(user1['token'], channel_1['channel_id']) == {
        'name': 'channel_1',
        'owner_members': [owner_dict],
        'all_members': [owner_dict, user1_dict]
    }

    other.clear()

# Testing if an owner can be removed from a public channel using channel_removeowner
def test_channel_removeowner_public_channel():
    other.clear()

    # The owner creates a public channel and invites user1 to the channel and then adds them as a owner
    owner = auth.auth_register("howner@email.com", "password", "Homer", "Simpson")
    user1 = auth.auth_register("user1@email.com", "password", "Bart", "Simpson")

    channel_1 = channels.channels_create(owner['token'], "channel_1", True)
    channel.channel_invite(owner['token'], channel_1["channel_id"], user1['u_id']) #assumes channel_invite works

    #user 1 is added as an owner
    channel.channel_addowner(owner['token'], channel_1['channel_id'], user1['u_id'])

    owner_dict = {'u_id': owner['u_id'], 'name_first': 'Homer', 'name_last': 'Simpson',
                'profile_img_url' : ""}
    user1_dict = {'u_id': user1['u_id'], 'name_first': 'Bart', 'name_last': 'Simpson',
                'profile_img_url' : ""}
    assert channel.channel_details(user1['token'], channel_1['channel_id']) == {
        'name': 'channel_1',
        'owner_members': [owner_dict, user1_dict],
        'all_members': [owner_dict, user1_dict]
    }

    #user 1 is then removed as being an owner
    channel.channel_removeowner(owner['token'], channel_1['channel_id'], user1['u_id'])

    owner_dict = {'u_id': owner['u_id'], 'name_first': 'Homer', 'name_last': 'Simpson',
                'profile_img_url' : ""}
    user1_dict = {'u_id': user1['u_id'], 'name_first': 'Bart', 'name_last': 'Simpson',
                'profile_img_url' : ""}
    assert channel.channel_details(user1['token'], channel_1['channel_id']) == {
        'name': 'channel_1',
        'owner_members': [owner_dict],
        'all_members': [owner_dict, user1_dict]
    }

    other.clear()

# Exception testing for removing an owner from a channel with an invalid channel_ID (channel doesn't exist)
def test_channel_removeowner_invalid_channelID():
    other.clear()

    owner = auth.auth_register("howner@email.com", "password", "Homer", "Simpson")
    user1 = auth.auth_register("user1@email.com", "password", "Bart", "Simpson")

    channel_1 = channels.channels_create(owner['token'], "channel_1", False)
    channel.channel_invite(owner['token'], channel_1["channel_id"], user1['u_id']) # Assumes channel_invite works

    channel.channel_addowner(owner['token'], channel_1['channel_id'], user1['u_id'])

    with pytest.raises(InputError):
        channel.channel_removeowner(owner['token'], 9999, user1['u_id'])

    other.clear()

# Exception testing for removing an owner from a channel that isn't an owner
def test_channel_removeowner_removing_non_owner():
    other.clear()

    owner = auth.auth_register("howner@email.com", "password", "Homer", "Simpson")
    user1 = auth.auth_register("user1@email.com", "password", "Bart", "Simpson")

    channel_1 = channels.channels_create(owner['token'], "channel_1", False)
    channel.channel_invite(owner['token'], channel_1["channel_id"], user1['u_id']) # Assumes channel_invite works

    with pytest.raises(InputError):
        channel.channel_removeowner(owner['token'], channel_1['channel_id'], user1['u_id'])

    other.clear()

# Exception testing for a user that is not an owner trying to remove an owner from the channel
def test_channel_removeowner_non_owner_removing_owners():
    other.clear()

    owner = auth.auth_register("howner@email.com", "password", "Homer", "Simpson")
    user1 = auth.auth_register("user1@email.com", "password", "Bart", "Simpson")

    channel_1 = channels.channels_create(owner['token'], "channel_1", False)
    channel.channel_invite(owner['token'], channel_1["channel_id"], user1['u_id']) # Assumes channel_invite works

    # User 1 will attempt to remove ownership from 'owner' where user1 is not an owner themself
    with pytest.raises(AccessError):
        channel.channel_removeowner(user1['token'], channel_1['channel_id'], owner['u_id'])

    other.clear()

# Test if a user can join a public channel
def test_channel_join_public_channel():
    other.clear()

    user1 = auth.auth_register("user1@email.com", "password", "John", "Smith")
    user2 = auth.auth_register("user2@email.com", "password", "Will", "Smith")

    channel_1 = channels.channels_create(user1['token'], "channel_1", True)
    channel.channel_join(user2['token'], channel_1['channel_id'])

    user1_dict = {'u_id': user1['u_id'], 'name_first': 'John', 'name_last': 'Smith',
                'profile_img_url' : ""}
    user2_dict = {'u_id': user2['u_id'], 'name_first': 'Will', 'name_last': 'Smith',
                'profile_img_url' : ""}
    assert channel.channel_details(user2['token'], channel_1['channel_id']) == {
        'name': 'channel_1',
        'owner_members': [user1_dict],
        'all_members': [user1_dict, user2_dict]
    }

# test that user with their permissions changed is able to be join a channel
def test_channel_join_user_permission_changed():
    other.clear()
    owner = auth.auth_register("user1@email.com", "password", "Homer", "Simpson")
    random_user1 = auth.auth_register("user2@email.com", "password", "Bart", "Simpson")

    channel_1 = channels.channels_create(owner['token'], "channel_1", True)
    other.admin_userpermission_change(owner['token'], random_user1['u_id'], 1)

    channel.channel_join(random_user1['token'], channel_1['channel_id'])

# Test for exception if a user tries to join an invalid channel
def test_channel_join_invalid_channel():
    other.clear()

    user1 = auth.auth_register("user1@email.com", "password", "John", "Smith")
    user2 = auth.auth_register("user2@email.com", "password", "Will", "Smith")
    channels.channels_create(user1['token'], "channel_1", True)

    with pytest.raises(InputError):
        channel.channel_join(user2['token'], 100000)
    
# Test for exception if a user tries to join a private channel
def test_channel_join_unauthorised():
    other.clear()

    user1 = auth.auth_register("user1@email.com", "password", "John", "Smith")
    user2 = auth.auth_register("user2@email.com", "password", "Will", "Smith")
    channel_1 = channels.channels_create(user1['token'], "channel_1", False)

    with pytest.raises(AccessError):
        channel.channel_join(user2['token'], channel_1['channel_id'])

# Test if a user can leave a public channel
def test_channel_leave_public_channel():
    other.clear()

    user1 = auth.auth_register("user1@email.com", "password", "John", "Smith")
    user2 = auth.auth_register("user2@email.com", "password", "Will", "Smith")

    channel_1 = channels.channels_create(user1['token'], "channel_1", True)
    channel.channel_join(user2['token'], channel_1['channel_id'])

    user1_dict = {'u_id': user1['u_id'], 'name_first': 'John', 'name_last': 'Smith',
                'profile_img_url' : ""}
    user2_dict = {'u_id': user2['u_id'], 'name_first': 'Will', 'name_last': 'Smith',
                'profile_img_url' : ""}

    assert channel.channel_details(user2['token'], channel_1['channel_id']) == {
        'name': 'channel_1',
        'owner_members': [user1_dict],
        'all_members': [user1_dict, user2_dict]
    }

    channel.channel_leave(user2['token'], channel_1['channel_id'])

    assert channel.channel_details(user1['token'], channel_1['channel_id']) == {
        'name': 'channel_1',
        'owner_members': [user1_dict],
        'all_members': [user1_dict]
    }

# Test if a user can leave another channel
def test_channel_leave_second_channel():
    other.clear()

    user1 = auth.auth_register("user1@email.com", "password", "John", "Smith")
    user2 = auth.auth_register("user2@email.com", "password", "Will", "Smith")

    channel_1 = channels.channels_create(user1['token'], "channel_1", True)
    channel_2 = channels.channels_create(user1['token'], "channel_1", True)
    channel.channel_join(user2['token'], channel_1['channel_id'])
    channel.channel_join(user2['token'], channel_2['channel_id'])

    user1_dict = {'u_id': user1['u_id'], 'name_first': 'John', 'name_last': 'Smith',
                'profile_img_url' : ""}
    user2_dict = {'u_id': user2['u_id'], 'name_first': 'Will', 'name_last': 'Smith',
                'profile_img_url' : ""}

    assert channel.channel_details(user2['token'], channel_2['channel_id']) == {
        'name': 'channel_1',
        'owner_members': [user1_dict],
        'all_members': [user1_dict, user2_dict]
    }

    channel.channel_leave(user2['token'], channel_2['channel_id'])

    assert channel.channel_details(user1['token'], channel_2['channel_id']) == {
        'name': 'channel_1',
        'owner_members': [user1_dict],
        'all_members': [user1_dict]
    }

# Test if a user can leave a private channel they have been invited to
def test_channel_leave_private_channel():
    other.clear()

    user1 = auth.auth_register("user1@email.com", "password", "John", "Smith")
    user2 = auth.auth_register("user2@email.com", "password", "Will", "Smith")

    channel_1 = channels.channels_create(user1['token'], "channel_1", False)
    channel.channel_invite(user1['token'], channel_1['channel_id'], user2['u_id'])
    channel.channel_leave(user2['token'], channel_1['channel_id'])  

# Test for exception of user tries to leave invalid channel
def test_channel_leave_invalid_channel():
    other.clear()

    user1 = auth.auth_register("user1@email.com", "password", "John", "Smith")
    user2 = auth.auth_register("user2@email.com", "password", "Will", "Smith")

    channels.channels_create(user1['token'], "channel_1", True)

    with pytest.raises(InputError):
        channel.channel_leave(user2['token'], 999999)

# Test for exception of user who tries to leave a public channel they are not in
def test_channel_leave_public_channel_exception():
    other.clear()

    user1 = auth.auth_register("user1@email.com", "password", "John", "Smith")
    user2 = auth.auth_register("user2@email.com", "password", "Will", "Smith")

    channel_1 = channels.channels_create(user1['token'], "channel_1", True)

    with pytest.raises(AccessError):
        channel.channel_leave(user2['token'], channel_1['channel_id'])

# Test for exception of user who tries to leave a private channel they are not in
def test_channel_leave_private_channel_exception():
    other.clear()

    user1 = auth.auth_register("user1@email.com", "password", "John", "Smith")
    user2 = auth.auth_register("user2@email.com", "password", "Will", "Smith")

    channel_1 = channels.channels_create(user1['token'], "channel_1", False)

    with pytest.raises(AccessError):
        channel.channel_leave(user2['token'], channel_1['channel_id'])


def check_message(requested_channel_id, requested_message_id):
    other.clear()

    # returns a message dictionary containing the information associated with the message
    # used to simplify processes in testing
    for channel_id in data.channels:
        if channel_id['channel_id'] == requested_channel_id:
            for current_message in channel_id['messages']:
                if current_message['message_id'] == requested_message_id:
                    return current_message

# tests channel_messages with a single message
def test_channel_messages_single_message():
    other.clear()

    # Creates a new channel owned by user1
    user1 = auth.auth_register("example@example.com", "abcd1234", "John", "Smith")
    channel_1 = channels.channels_create(user1['token'], 'Test Channel', True)
    # Adds message to channel from user1 such as 'message0'
    # Also adds the message infomation to the message_list dictionary
    message.message_send(user1['token'], channel_1['channel_id'], 'test message')
    # checks that what channel_messages returns is equal to the expected return
    messages_channel = channel.channel_messages(user1['token'], channel_1['channel_id'], 0)
    assert messages_channel['messages'][0]['message'] == 'test message'
    other.clear()

# tests channel_messages with a two messages
def test_channel_messages_two_messages():
    other.clear()

    # Creates a new channel owned by user1
    user1 = auth.auth_register("example@example.com", "abcd1234", "John", "Smith")
    channel_1 = channels.channels_create(user1['token'], 'Test Channel', True)
    # Adds message to channel from user1 such as 'message0'
    # Also adds the message infomation to the message_list dictionary
    i = 0
    while i < 2:
        message.message_send(user1['token'], channel_1['channel_id'], 'message {}'.format(i + 1))
        i += 1
    # checks that what channel_messages returns is equal to the expected return
    messages = channel.channel_messages(user1['token'], channel_1['channel_id'], 0)
    assert messages['messages'][0]['message'] == 'message 2'
    assert messages['messages'][1]['message'] == 'message 1'
    other.clear()

# tests channel_messages with a channel that has no messages at all
def test_channel_messages_empty_channel():
    other.clear()

    # Creates a new channel owned by user1
    user1 = auth.auth_register("example@example.com", "abcd1234", "John", "Smith")
    channel_1 = channels.channels_create(user1['token'], 'Test Channel', True)


    # checks that what channel_messages returns the dictionary with empty messages
    messages = channel.channel_messages(user1['token'], channel_1['channel_id'], 0)
    assert messages == {
        'start' : 0,
        'messages' : [],
        'end' : -1
    }
    other.clear()


# tests channel_messages with fifty messages
def test_channel_messages_fifty_messages():
    other.clear()

    message_list = {
        'messages': [],
        'start' : 0,
        'end' : -1
    }
    i = 0
    while i < 50:
        message_list['messages'].append('message {}'.format(50 - i))
        i += 1
    # Creates a new channel owned by user1
    user1 = auth.auth_register("example@example.com", "abcd1234", "John", "Smith")
    channel_1 = channels.channels_create(user1['token'], 'Test Channel', True)
    # Adds message to channel from user1 such as 'message0'
    # Also adds the message infomation to the message_list dictionary
    i = 0
    while i < 50:
        message.message_send(user1['token'], channel_1['channel_id'], 'message {}'.format(i + 1))
        i += 1
    # checks that what channel_messages returns is equal to the expected return
    messages_channel = channel.channel_messages(user1['token'], channel_1['channel_id'], 0)
    i = 0
    while i < 50:
        assert messages_channel['messages'][i]['message'] == message_list['messages'][i]
        i += 1
    assert messages_channel['start'] == 0
    assert messages_channel['end'] == -1
    other.clear()

# tests channel_messages with fifty messages starting at 10
def test_channel_messages_fifty_messages_start_ten():
    other.clear()

    message_list = {
        'messages': [
        ],
        'start' : 10,
        'end' : -1
    }
    i = 0
    while i < 40:
        message_list['messages'].append('message {}'.format(40 - i))
        i += 1      
    # Creates a new channel owned by user1
    user1 = auth.auth_register("example@example.com", "abcd1234", "John", "Smith")
    channel_1 = channels.channels_create(user1['token'], 'Test Channel', True)
    # Adds message to channel from user1 such as 'message0'
    # Also adds the message infomation to the message_list dictionary
    i = 0
    while i < 50:
        message.message_send(user1['token'], channel_1['channel_id'], 'message {}'.format(i + 1))
        i +=1
    # checks that what channel_messages returns is equal to the expected return
    messages_channel = channel.channel_messages(user1['token'], channel_1['channel_id'], 10)

    i = 0
    while i < 40:
        assert messages_channel['messages'][i]['message'] == message_list['messages'][i]
        i += 1

    other.clear()

# tests channel_messages with fifty one messages
def test_channel_messages_fifty_one_messages():
    other.clear()

    message_list = {
        'messages': [
        ],
        'start' : 0,
        'end' : 50
    }
    i = 0
    while i < 50:
        message_list['messages'].append('message {}'.format(51 - i))
        i += 1
    # Creates a new channel owned by user1
    user1 = auth.auth_register("example@example.com", "abcd1234", "John", "Smith")
    channel_1 = channels.channels_create(user1['token'], 'Test Channel', True)
    # Adds message to channel from user1 such as 'message0'
    # Also adds the message infomation to the message_list dictionary
    i = 0
    while i < 51:
        message.message_send(user1['token'], channel_1['channel_id'], 'message {}'.format(i + 1))
        i += 1
    # checks that what channel_messages returns is equal to the expected return
    messages_channel = channel.channel_messages(user1['token'], channel_1['channel_id'], 0)
    i = 0
    while i < 50:
        assert messages_channel['messages'][i]['message'] == message_list['messages'][i]
        i += 1
    assert messages_channel['start'] == 0
    assert messages_channel['end'] == 50
    other.clear()

# tests channel_messages with fifty one messages starting at one
def test_channel_messages_fifty_one_messages_start_one():
    other.clear()

    message_list = {
        'messages': [
        ],
        'start' : 1,
        'end' : -1
    }
    i = 0
    while i < 50:
        message_list['messages'].append('message {}'.format(51 - i))
        i += 1
    # Creates a new channel owned by user1
    user1 = auth.auth_register("example@example.com", "abcd1234", "John", "Smith")
    channel_1 = channels.channels_create(user1['token'], 'Test Channel', True)
    # Adds message to channel from user1 such as 'message0'
    # Also adds the message infomation to the message_list dictionary
    i = 0
    while i < 51:
        message.message_send(user1['token'], channel_1['channel_id'], 'message {}'.format(i + 1))
        i += 1
    # checks that what channel_messages returns is equal to the expected return
    messages_channel = channel.channel_messages(user1['token'], channel_1['channel_id'], 1)
    while i < 50:
        assert messages_channel['messages'][i]['message'] == message_list['messages'][i]
        i += 1
    assert messages_channel['start'] == 1
    assert messages_channel['end'] == -1

    other.clear()

# tests channel_messages with an invalid invalid start number
def test_channel_messages_invalid_start():
    other.clear()
    i = 0
    # Creates a new channel owned by user1
    user1 = auth.auth_register("example@example.com", "abcd1234", "John", "Smith")
    channel_1 = channels.channels_create(user1['token'], 'Test Channel', True)
    # Adds message to channel from user1 such as 'message0'
    # Also adds the message infomation to the message_list dictionary
    while i < 1:
        message.message_send(user1['token'], channel_1['channel_id'], 'message {}'.format(i + 1))
        i = i + 1
    # checks that what channel_messages returns is equal to the expected return
    with pytest.raises(InputError):
        channel.channel_messages(user1['token'], channel_1['channel_id'], 1000)

# tests channel_messages with invalid access
def test_channel_messages_invalid_access():
    other.clear()
    i = 0
    # Creates a new channel owned by user1
    user1 = auth.auth_register("example@example.com", "abcd1234", "John", "Smith")
    user2 = auth.auth_register("example2@example.com", "abcde12345", "Homer", "Simpson")
    channel_1 = channels.channels_create(user1['token'], 'Test Channel', True)
    # Adds message to channel from user1 such as 'message0'
    # Also adds the message infomation to the message_list dictionary
    message.message_send(user1['token'], channel_1['channel_id'], 'message {}'.format(i + 1))
    # checks that what channel_messages returns is equal to the expected return
    with pytest.raises(AccessError):
        channel.channel_messages(user2['token'], channel_1['channel_id'], 0)
