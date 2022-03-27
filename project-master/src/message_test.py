'''
Contains all the functions that test the message functions
from message.py
'''
import pytest
import error
import other
import auth
import channel
import channels
import message
import time
import threading


def test_message_send():
    '''
    tests that message_send is working
    '''
    other.clear()
    owner = auth.auth_register("user1@email.com", "password", "Homer", "Simpson")
    channel_1 = channels.channels_create(owner['token'], "channel_1", True)
    message.message_send(owner['token'], channel_1['channel_id'],
                        'this is the first test message')

    messages = channel.channel_messages(owner['token'], channel_1['channel_id'], 0)
    assert messages['messages'][0]['message'] == 'this is the first test message'


def test_message_send_max_length():
    '''
    tests the edge cases of message_send
    '''
    other.clear()
    owner = auth.auth_register("user1@email.com", "password", "Homer", "Simpson")
    channel_1 = channels.channels_create(owner['token'], "channel_1", True)
    test_message = 'a' * 1000
    message.message_send(owner['token'], channel_1['channel_id'], test_message)
    messages = channel.channel_messages(owner['token'], channel_1['channel_id'], 0)
    assert messages['messages'][0]['message'] == test_message


def test_message_send_normal_user():
    '''
    Test that a user with no owner permissions can send a message
    '''
    other.clear()
    owner = auth.auth_register("user1@email.com", "password", "Homer", "Simpson")
    user = auth.auth_register("user2@email.com", "password", "Bart", "Simpson")
    channels.channels_create(owner['token'], "channel_1", True)
    channel_2 = channels.channels_create(owner['token'], "channel_2", True)
    channel.channel_join(user['token'], channel_2['channel_id'])
    test_message = 'a' * 1000
    message.message_send(user['token'], channel_2['channel_id'], test_message)
    messages = channel.channel_messages(user['token'], channel_2['channel_id'], 0)
    assert messages['messages'][0]['message'] == test_message 


def test_message_send_invalid_length():
    '''
    tests that only messages of length <= 1000 are accepted
    '''
    other.clear()
    owner = auth.auth_register("user1@email.com", "password", "Homer", "Simpson")
    channel_1 = channels.channels_create(owner['token'], "channel_1", True)
    test_message = 'a' * 1001
    with pytest.raises(error.InputError):
        message.message_send(owner['token'], channel_1['channel_id'], test_message)


def test_message_send_invalid_user():
    '''
    tests that message send only works for users in the channel
    '''
    other.clear()
    owner = auth.auth_register("user1@email.com", "password", "Homer", "Simpson")
    other_user = auth.auth_register("user2@email.com", "password", "Marge", "Simpson")
    channel_1 = channels.channels_create(owner['token'], "channel_1", True)
    with pytest.raises(error.AccessError):
        message.message_send(other_user['token'], channel_1['channel_id'],
                            'this is the first test message')  


def test_message_remove():
    '''
    Test that message_remove removes the specified message in the channel
    '''
    other.clear()
    owner = auth.auth_register("user1@email.com", "password", "Homer", "Simpson")
    channel_1 = channels.channels_create(owner['token'], "channel_1", True)
    message_1 = message.message_send(owner['token'], channel_1['channel_id'],
                                    'this is the first test message')

    message.message_remove(owner['token'], message_1['message_id'])
    messages = channel.channel_messages(owner['token'], channel_1['channel_id'], 0)
    assert messages['messages'] == []


def test_message_remove_two_messages():
    '''
    tests that message_remove removes the correct message in the messages list
    '''
    other.clear()
    owner = auth.auth_register("user1@email.com", "password", "Homer", "Simpson")
    channel_1 = channels.channels_create(owner['token'], "channel_1", True)
    message.message_send(owner['token'], channel_1['channel_id'], 'this is the first test message')
    message_2 = message.message_send(owner['token'], channel_1['channel_id'], 
                                    'this is the second test message')

    message.message_remove(owner['token'], message_2['message_id'])
    messages = channel.channel_messages(owner['token'], channel_1['channel_id'], 0)
    assert messages['messages'][0]['message'] == 'this is the first test message'


def test_message_remove_non_owner():
    '''
    tests that a non-owner can remove their own message
    '''
    other.clear()
    owner = auth.auth_register("user1@email.com", "password", "Homer", "Simpson")
    other_user = auth.auth_register("user2@email.com", "password", "Marge", "Simpson")
    channel_1 = channels.channels_create(owner['token'], "channel_1", True)
    channel.channel_join(other_user['token'], channel_1['channel_id'])
    message_1 = message.message_send(other_user['token'], channel_1['channel_id'],
                                    'this is the first test message')

    message.message_remove(other_user['token'], message_1['message_id'])
    messages = channel.channel_messages(owner['token'], channel_1['channel_id'], 0)
    assert messages['messages'] == []


def test_message_remove_non_owner_invalid():
    '''
    tests that a non-owner cannot remove anothers message
    '''
    other.clear()
    owner = auth.auth_register("user1@email.com", "password", "Homer", "Simpson")
    other_user = auth.auth_register("user2@email.com", "password", "Marge", "Simpson")
    channel_1 = channels.channels_create(owner['token'], "channel_1", True)
    channel.channel_join(other_user['token'], channel_1['channel_id'])
    message_1 = message.message_send(owner['token'], channel_1['channel_id'], 
                                    'this is the first test message')
    with pytest.raises(error.AccessError):
        message.message_remove(other_user['token'], message_1['message_id'])


def test_message_remove_owner():
    '''
    tests that an owner can remove another users message
    '''
    other.clear()
    owner = auth.auth_register("user1@email.com", "password", "Homer", "Simpson")
    other_user = auth.auth_register("user2@email.com", "password", "Marge", "Simpson")
    channel_1 = channels.channels_create(owner['token'], "channel_1", True)
    channel.channel_join(other_user['token'], channel_1['channel_id'])
    message_1 = message.message_send(other_user['token'], channel_1['channel_id'], 
                                    'this is the first test message')

    message.message_remove(owner['token'], message_1['message_id'])
    messages = channel.channel_messages(owner['token'], channel_1['channel_id'], 0)
    assert messages['messages'] == []


def test_message_remove_multiple_channels():
    '''
    Test that message remove works when a user is in multiple channels
    '''
    other.clear()
    owner = auth.auth_register("user1@email.com", "password", "Homer", "Simpson")
    user = auth.auth_register("user2@email.com", "password", "Bart", "Simpson")
    channels.channels_create(owner['token'], "channel_1", True)
    channel_2 = channels.channels_create(owner['token'], "channel_2", True)
    channel.channel_join(user['token'], channel_2['channel_id'])
    message.message_send(user['token'], channel_2['channel_id'], 'test message 1')
    message_to_remove = message.message_send(user['token'], channel_2['channel_id'], 
                                            'test message 2')

    message.message_remove(user['token'], message_to_remove['message_id'])
    messages = channel.channel_messages(user['token'], channel_2['channel_id'], 0)
    assert messages['messages'][0]['message'] == 'test message 1'
    assert messages['start'] == 0
    assert messages['end'] == -1
    assert len(messages['messages']) == 1
        

def test_message_remove_error():
    '''
    Test error for trying to remove message with message_id that does not exist
    '''
    other.clear()
    owner = auth.auth_register("user1@email.com", "password", "Homer", "Simpson")
    channels.channels_create(owner['token'], "channel_1", True)
    with pytest.raises(error.InputError):
        message.message_remove(owner['token'], 1)


def test_message_remove_invalid_message_id():
    '''
    Test error for tryng to remove a message with invalid message id
    '''
    other.clear()
    owner = auth.auth_register("user1@email.com", "password", "Homer", "Simpson")
    channel_1 = channels.channels_create(owner['token'], "channel_1", True)
    message.message_send(owner['token'], channel_1['channel_id'], 'test message 1')
    with pytest.raises(error.InputError):
        message.message_remove(owner['token'], 2)


def test_message_remove_empty_channels():
    '''
    Check that an exception InputError is raised when a user tries to remove
    a message from channels that have no mesasges
    '''
    other.clear()
    owner = auth.auth_register("user1@email.com", "password", "Homer", "Simpson")
    channels.channels_create(owner['token'], "channel_1", True)
    channels.channels_create(owner['token'], "channel_2", True)
    channels.channels_create(owner['token'], "channel_3", True)
    with pytest.raises(error.InputError):
        message.message_remove(owner['token'], 1)    
    

def test_message_edit():
    '''
    test that message_edit edits a message
    '''
    other.clear()
    owner = auth.auth_register("user1@email.com", "password", "Homer", "Simpson")
    channel_1 = channels.channels_create(owner['token'], "channel_1", True)
    message_1 = message.message_send(owner['token'], channel_1['channel_id'], 
                                    'this is the first test message')

    message.message_edit(owner['token'], message_1['message_id'], 'this is edited')
    messages = channel.channel_messages(owner['token'], channel_1['channel_id'], 0)
    assert messages['messages'][0]['message'] == 'this is edited'

def test_message_edit_remove_message():
    '''
    test that message_edit edits a message
    '''
    other.clear()
    owner = auth.auth_register("user1@email.com", "password", "Homer", "Simpson")
    channel_1 = channels.channels_create(owner['token'], "channel_1", True)
    message_1 = message.message_send(owner['token'], channel_1['channel_id'], 
                                    'this is the first test message')

    message.message_edit(owner['token'], message_1['message_id'], '')
    messages = channel.channel_messages(owner['token'], channel_1['channel_id'], 0)
    assert messages['messages'] == []



def test_message_edit_after_multiple_messages():
    '''
    test that message_edit works on editing a random message in a channel
    '''
    other.clear()
    owner = auth.auth_register("user1@email.com", "password", "Homer", "Simpson")
    channel_1 = channels.channels_create(owner['token'], "channel_1", True)
    message.message_send(owner['token'], channel_1['channel_id'], 'first message')
    message_2 = message.message_send(owner['token'], channel_1['channel_id'], 'second message')
    message.message_send(owner['token'], channel_1['channel_id'], 'third message')
    message.message_edit(owner['token'], message_2['message_id'], 'second message is edited')

    messages = channel.channel_messages(owner['token'], channel_1['channel_id'], 0)
    assert messages['messages'][1]['message'] == 'second message is edited'



def test_message_edit_other_user_by_owner():
    '''
    test if the owner of the channel can edit the message of another user
    '''
    other.clear()
    owner = auth.auth_register("user1@email.com", "password", "John", "Smith")
    channel_1 = channels.channels_create(owner['token'], "channel_1", True)
    user1 = auth.auth_register("user2@email.com", "password", "Will", "Smith")
    user2 = auth.auth_register("user3@email.com", "password", "Carlton", "Banks")
    channel.channel_join(user1['token'], channel_1['channel_id'])
    channel.channel_join(user2['token'], channel_1['channel_id'])
    message.message_send(user1['token'], channel_1['channel_id'], 'user1 message')
    message_to_edit = message.message_send(user2['token'], channel_1['channel_id'], 'user2 message')
    message.message_edit(owner['token'], message_to_edit['message_id'], 'user2 message is edited')

    messages = channel.channel_messages(owner['token'], channel_1['channel_id'], 0)
    assert messages['messages'][0]['message'] == 'user2 message is edited'



def test_message_edit_by_normal_user():
    '''
    test if a normal user in a channel can edit their own message
    '''
    other.clear()
    owner = auth.auth_register("user1@email.com", "password", "John", "Smith")
    channel_1 = channels.channels_create(owner['token'], "channel_1", True)
    user1 = auth.auth_register("user2@email.com", "password", "Will", "Smith")
    channel.channel_join(user1['token'], channel_1['channel_id'])
    message_to_edit = message.message_send(user1['token'], channel_1['channel_id'], 'user1 message')
    message.message_edit(user1['token'], message_to_edit['message_id'], 'user1 message is edited')

    messages = channel.channel_messages(owner['token'], channel_1['channel_id'], 0)
    assert messages['messages'][0]['message'] == 'user1 message is edited'



def test_message_edit_unauthorised_user():
    '''
    test for InputError raised when a normal user tries to edit another user's message
    '''
    other.clear()
    owner = auth.auth_register("user1@email.com", "password", "John", "Smith")
    channel_1 = channels.channels_create(owner['token'], "channel_1", True)
    user1 = auth.auth_register("user2@email.com", "password", "Will", "Smith")
    channel.channel_join(user1['token'], channel_1['channel_id'])
    message_to_edit = message.message_send(owner['token'], channel_1['channel_id'], 'owner message')
    
    with pytest.raises(error.AccessError):
        message.message_edit(user1['token'], message_to_edit['message_id'], 
                            'trying to edit owner message')


def test_message_react():
    '''
    test that a user can react to a mesasge
    '''
    other.clear()
    owner = auth.auth_register("user1@email.com", "password", "John", "Smith")
    channel_1 = channels.channels_create(owner['token'], "channel_1", True)
    message_sent = message.message_send(owner['token'], channel_1['channel_id'], 'owner message')
    message.message_react(owner['token'], message_sent['message_id'], 1)

    messages = channel.channel_messages(owner['token'], channel_1['channel_id'], 0)
    assert messages['messages'][0]['reacts'][0]['react_id'] == 1
    assert owner['u_id'] in messages['messages'][0]['reacts'][0]['u_ids']

def test_message_react_two_users():
    '''
    test that two users can react to a mesasge
    '''
    other.clear()
    owner = auth.auth_register("user1@email.com", "password", "John", "Smith")
    user = auth.auth_register("user2@email.com", "password", "Will", "Smith")
    channel_1 = channels.channels_create(owner['token'], "channel_1", True)
    channel.channel_join(user['token'], channel_1['channel_id'])
    message_sent = message.message_send(owner['token'], channel_1['channel_id'], 'owner message')
    message.message_react(owner['token'], message_sent['message_id'], 1)
    message.message_react(user['token'], message_sent['message_id'], 1)

    messages = channel.channel_messages(owner['token'], channel_1['channel_id'], 0)
    assert messages['messages'][0]['reacts'][0]['react_id'] == 1
    assert owner['u_id'] in messages['messages'][0]['reacts'][0]['u_ids']
    assert user['u_id'] in messages['messages'][0]['reacts'][0]['u_ids']

def test_message_react_invalid_message_id():
    '''
    test that an InputError is raised when an invalid message_id is given 
    '''
    other.clear()
    owner = auth.auth_register("user1@email.com", "password", "John", "Smith")
    channel_1 = channels.channels_create(owner['token'], "channel_1", True)
    message.message_send(owner['token'], channel_1['channel_id'], 'owner message')
    
    with pytest.raises(error.InputError):
        message.message_react(owner['token'], 2, 1)

def test_message_react_invalid_react_id():
    '''
    test that an InputError is raised when an invalid react_id is given 
    '''
    other.clear()
    owner = auth.auth_register("user1@email.com", "password", "John", "Smith")
    channel_1 = channels.channels_create(owner['token'], "channel_1", True)
    message_sent = message.message_send(owner['token'], channel_1['channel_id'], 'owner message')

    with pytest.raises(error.InputError):
        message.message_react(owner['token'], message_sent['message_id'], 2)


def test_message_react_message_already_reacted():
    '''
    test that an InputError is raised when a user reacts to a message that they
    have already reacted to
    '''
    other.clear()
    owner = auth.auth_register("user1@email.com", "password", "John", "Smith")
    channel_1 = channels.channels_create(owner['token'], "channel_1", True)
    message_sent = message.message_send(owner['token'], channel_1['channel_id'], 'owner message')
    message.message_react(owner['token'], message_sent['message_id'], 1)

    with pytest.raises(error.InputError):
        message.message_react(owner['token'], message_sent['message_id'], 1)

def test_message_unreact():
    '''
    test that a user can unreact a message they have reacted to
    '''
    other.clear()
    owner = auth.auth_register("user1@email.com", "password", "John", "Smith")
    channel_1 = channels.channels_create(owner['token'], "channel_1", True)
    message_sent = message.message_send(owner['token'], channel_1['channel_id'], 'owner message')
    message.message_react(owner['token'], message_sent['message_id'], 1)

    messages = channel.channel_messages(owner['token'], channel_1['channel_id'], 0)
    assert messages['messages'][0]['reacts'][0]['react_id'] == 1

    message.message_unreact(owner['token'], message_sent['message_id'], 1)

    messages = channel.channel_messages(owner['token'], channel_1['channel_id'], 0)
    assert messages['messages'][0]['reacts'][0]['u_ids'] == []

def test_message_unreact_two_users():
    '''
    test that multiple users can unreact a message they have reacted to
    '''
    other.clear()
    owner = auth.auth_register("user1@email.com", "password", "John", "Smith")
    user = auth.auth_register("user2@email.com", "password", "Will", "Smith")
    channel_1 = channels.channels_create(owner['token'], "channel_1", True)
    channel.channel_join(user['token'], channel_1['channel_id'])
    message_sent = message.message_send(owner['token'], channel_1['channel_id'], 'owner message')
    message.message_react(owner['token'], message_sent['message_id'], 1)
    message.message_react(user['token'], message_sent['message_id'], 1)

    message.message_unreact(user['token'], message_sent['message_id'], 1)

    messages = channel.channel_messages(owner['token'], channel_1['channel_id'], 0)
    assert messages['messages'][0]['reacts'][0]['u_ids'] == [owner['u_id']]

def test_message_unreact_invalid_message_id():
    '''
    test that an InputError is raised when an invalid message id is given
    '''
    other.clear()
    owner = auth.auth_register("user1@email.com", "password", "John", "Smith")
    channel_1 = channels.channels_create(owner['token'], "channel_1", True)
    message_sent = message.message_send(owner['token'], channel_1['channel_id'], 'owner message')
    message.message_react(owner['token'], message_sent['message_id'], 1)

    messages = channel.channel_messages(owner['token'], channel_1['channel_id'], 0)
    assert messages['messages'][0]['reacts'][0]['react_id'] == 1

    with pytest.raises(error.InputError):
        message.message_unreact(owner['token'], 10, 1)

def test_message_unreact_invalid_react_id():
    '''
    test that an InputError is raised when an invalid react id is given
    '''
    other.clear()
    owner = auth.auth_register("user1@email.com", "password", "John", "Smith")
    channel_1 = channels.channels_create(owner['token'], "channel_1", True)
    message_sent = message.message_send(owner['token'], channel_1['channel_id'], 'owner message')
    message.message_react(owner['token'], message_sent['message_id'], 1)

    messages = channel.channel_messages(owner['token'], channel_1['channel_id'], 0)
    assert messages['messages'][0]['reacts'][0]['react_id'] == 1

    with pytest.raises(error.InputError):
        message.message_unreact(owner['token'], message_sent['message_id'], 2)

def test_message_unreact_user_did_not_react():
    '''
    test that an InputError is raised when the user unreacts to a message
    they did not react to
    '''
    other.clear()
    owner = auth.auth_register("user1@email.com", "password", "John", "Smith")
    user = auth.auth_register("user2@email.com", "password", "Will", "Smith")
    channel_1 = channels.channels_create(owner['token'], "channel_1", True)
    channel.channel_join(user['token'], channel_1['channel_id'])
    message_sent = message.message_send(owner['token'], channel_1['channel_id'], 'owner message')
    message.message_react(owner['token'], message_sent['message_id'], 1) 

    with pytest.raises(error.InputError):
        message.message_unreact(user['token'], message_sent['message_id'], 1)


def test_message_pin_working():
    '''
    test that message_pin works under the specification of the documentation
    '''
    other.clear()
    owner = auth.auth_register("user1@email.com", "password", "John", "Smith")
    channel_1 = channels.channels_create(owner['token'], "channel_1", True)
    message_1 = message.message_send(owner['token'], channel_1['channel_id'], 
                                    'this is the first test message')
    message.message_pin(owner['token'], message_1['message_id'])
    messages = channel.channel_messages(owner['token'], channel_1['channel_id'], 0)
    assert messages['messages'][0]['is_pinned']


def test_message_pin_already_pinned():
    '''
    test that message_pin returns an InputError when the message is already pinned
    '''
    other.clear()
    owner = auth.auth_register("user1@email.com", "password", "John", "Smith")
    channel_1 = channels.channels_create(owner['token'], "channel_1", True)
    message_1 = message.message_send(owner['token'], channel_1['channel_id'], 
                                    'this is the first test message')
    message.message_pin(owner['token'], message_1['message_id'])
    with pytest.raises(error.InputError):
        message.message_pin(owner['token'], message_1['message_id'])


def test_message_pin_non_member():
    '''
    test that message_pin returns InputError when no message exists at that id
    '''
    other.clear()
    owner = auth.auth_register("user1@email.com", "password", "John", "Smith")
    other_user = auth.auth_register("user2@email.com", "password2", "Mary", "Smith")
    channel_1 = channels.channels_create(owner['token'], "channel_1", True)
    message_1 = message.message_send(owner['token'], channel_1['channel_id'], 
                                    'this is the first test message')
    with pytest.raises(error.AccessError):
        message.message_pin(other_user['token'], message_1['message_id'])


def test_message_pin_non_owner():
    '''
    test that message_pin returns InputError when no message exists at that id
    '''
    other.clear()
    owner = auth.auth_register("user1@email.com", "password", "John", "Smith")
    other_user = auth.auth_register("user2@email.com", "password2", "Mary", "Smith")
    channel_1 = channels.channels_create(owner['token'], "channel_1", True)
    message_1 = message.message_send(owner['token'], channel_1['channel_id'], 
                                    'this is the first test message')
    channel.channel_join(other_user['token'], channel_1['channel_id'])
    with pytest.raises(error.AccessError):
        message.message_pin(other_user['token'], message_1['message_id'])

def test_message_pin_invalid_message_id():
    '''
    test that an InputError is raised when an invalid message_id is given
    '''
    other.clear()
    owner = auth.auth_register("user1@email.com", "password", "John", "Smith")
    channel_1 = channels.channels_create(owner['token'], "channel_1", True)
    message.message_send(owner['token'], channel_1['channel_id'], 
                                    'this is the first test message')

    message_2 = message.message_send(owner['token'], channel_1['channel_id'], 
                                    'this is the second test message')

    message.message_pin(owner['token'], message_2['message_id'])
    messages = channel.channel_messages(owner['token'], channel_1['channel_id'], 0)
    assert messages['messages'][0]['is_pinned']

    with pytest.raises(error.InputError):
        message.message_pin(owner['token'], 10)


def test_message_unpin():
    '''
    tests that message_unpin works as intended
    '''
    other.clear()
    owner = auth.auth_register("user1@email.com", "password", "John", "Smith")
    channel_1 = channels.channels_create(owner['token'], "channel_1", True)
    message_1 = message.message_send(owner['token'], channel_1['channel_id'], 
                                    'this is the first test message')
    message.message_pin(owner['token'], message_1['message_id'])
    message.message_unpin(owner['token'], message_1['message_id'])
    messages = channel.channel_messages(owner['token'], channel_1['channel_id'], 0)
    assert not messages['messages'][0]['is_pinned']

def test_message_unpin_not_pinned():
    '''
    tests that message_unpin raises an input error when the message is not pinned
    '''
    other.clear()
    owner = auth.auth_register("user1@email.com", "password", "John", "Smith")
    channel_1 = channels.channels_create(owner['token'], "channel_1", True)
    message_1 = message.message_send(owner['token'], channel_1['channel_id'], 
                                    'this is the first test message')
    with pytest.raises(error.InputError):
        message.message_unpin(owner['token'], message_1['message_id'])

def test_message_unpin_invalid_id():
    '''
    tests that message_unpin raises an input error when the message doesn't exist
    '''
    other.clear()
    owner = auth.auth_register("user1@email.com", "password", "John", "Smith")
    with pytest.raises(error.InputError):
        message.message_unpin(owner['token'], 1)

def test_message_unpin_not_member_of_channel():
    '''
    tests that message_unpin raises an input error when the message is not pinned
    '''
    other.clear()
    owner = auth.auth_register("user1@email.com", "password", "John", "Smith")
    non_member = auth.auth_register("user2@email.com", "password2", "Jane", "Smith")
    channel_1 = channels.channels_create(owner['token'], "channel_1", True)
    message_1 = message.message_send(owner['token'], channel_1['channel_id'], 
                                    'this is the first test message')
    message.message_pin(owner['token'], message_1['message_id'])
    with pytest.raises(error.AccessError):
        message.message_unpin(non_member['token'], message_1['message_id'])

def test_message_unpin_invalid_message_id():
    '''
    test that an InputError is raised when an invalid message_id is given
    '''
    other.clear()
    owner = auth.auth_register("user1@email.com", "password", "John", "Smith")
    channel_1 = channels.channels_create(owner['token'], "channel_1", True)
    message.message_send(owner['token'], channel_1['channel_id'], 
                                    'this is the first test message')

    message_2 = message.message_send(owner['token'], channel_1['channel_id'], 
                                    'this is the second test message')

    message.message_pin(owner['token'], message_2['message_id'])
    messages = channel.channel_messages(owner['token'], channel_1['channel_id'], 0)
    assert messages['messages'][0]['is_pinned']

    with pytest.raises(error.InputError):
        message.message_unpin(owner['token'], 10)


def test_message_unpin_not_owner_of_channel():
    '''
    tests that message_unpin raises an input error when the message is not pinned
    '''
    other.clear()
    owner = auth.auth_register("user1@email.com", "password", "John", "Smith")
    non_owner = auth.auth_register("user2@email.com", "password2", "Jane", "Smith")
    channel_1 = channels.channels_create(owner['token'], "channel_1", True)
    channel.channel_join(non_owner['token'], channel_1['channel_id'])
    message_1 = message.message_send(owner['token'], channel_1['channel_id'], 
                                    'this is the first test message')
    message.message_pin(owner['token'], message_1['message_id'])
    with pytest.raises(error.AccessError):
        message.message_unpin(non_owner['token'], message_1['message_id'])

def test_message_sendlater():
    '''
    tests the message_sendlater functionality
    '''
    other.clear()
    send_time = int(time.time()) + 10
    owner = auth.auth_register("user1@email.com", "password", "Homer", "Simpson")
    channel_1 = channels.channels_create(owner['token'], "channel_1", True)
    new_message_id = message.message_sendlater(owner['token'], channel_1['channel_id'],
                        'this is the first test message', send_time)
    messages = channel.channel_messages(owner['token'], channel_1['channel_id'], 0)
    assert messages['messages'] == []
    time.sleep(11)
    later_message = channel.channel_messages(owner['token'], channel_1['channel_id'], 0)
    assert later_message['messages'][0] == {
        'message_id' : new_message_id,
        'u_id' : owner['u_id'],
        'message' : 'this is the first test message',
        'time_created' : send_time,
        'reacts' : [],
        'is_pinned' : False,
    }

def test_message_sendlater_another_channel():
    '''
    tests the message_sendlater functionality in another channel
    '''
    other.clear()
    send_time = int(time.time()) + 5
    owner = auth.auth_register("user1@email.com", "password", "Homer", "Simpson")
    channels.channels_create(owner['token'], "channel_1", True)
    channel_2 = channels.channels_create(owner['token'], "channel_1", True)
    new_message_id = message.message_sendlater(owner['token'], channel_2['channel_id'],
                        'this is the first test message', send_time)
    messages = channel.channel_messages(owner['token'], channel_2['channel_id'], 0)
    assert messages['messages'] == []
    time.sleep(6)
    later_message = channel.channel_messages(owner['token'], channel_2['channel_id'], 0)
    assert later_message['messages'][0] == {
        'message_id' : new_message_id,
        'u_id' : owner['u_id'],
        'message' : 'this is the first test message',
        'time_created' : send_time,
        'reacts' : [],
        'is_pinned' : False,
    }

def test_message_sendlater_with_other_messages():
    '''
    tests the message_sendlater functionality in a channel which
    already have messages
    '''
    other.clear()
    send_time = int(time.time()) + 5
    owner = auth.auth_register("user1@email.com", "password", "Homer", "Simpson")
    channels.channels_create(owner['token'], "channel_1", True)
    channel_2 = channels.channels_create(owner['token'], "channel_1", True)
    message.message_send(owner['token'], channel_2['channel_id'], "test message")
    new_message_id = message.message_sendlater(owner['token'], channel_2['channel_id'],
                        'this is the first test message', send_time)
    messages = channel.channel_messages(owner['token'], channel_2['channel_id'], 0)
    assert messages['messages'][0]['message'] == 'test message'
    time.sleep(6)
    later_message = channel.channel_messages(owner['token'], channel_2['channel_id'], 0)
    assert later_message['messages'][0] == {
        'message_id' : new_message_id,
        'u_id' : owner['u_id'],
        'message' : 'this is the first test message',
        'time_created' : send_time,
        'reacts' : [],
        'is_pinned' : False,
    }


def test_message_sendlater_invalid_channel():
    '''
    tests the message_sendlater functionality with invalid channel ids
    '''
    other.clear()
    send_time = int(time.time()) + 10
    owner = auth.auth_register("user1@email.com", "password", "Homer", "Simpson")
    with pytest.raises(error.InputError):
        message.message_sendlater(owner['token'], 1, 'this is the first test message', send_time)

def test_message_sendlater_message_too_long():
    '''
    tests that message_sendlater rejects messages longer than 1000 chars
    '''
    other.clear()
    send_time = int(time.time()) + 10
    message_for_sending = 'a' * 1001
    owner = auth.auth_register("user1@email.com", "password", "Homer", "Simpson")
    channel_1 = channels.channels_create(owner['token'], "channel_1", True)
    with pytest.raises(error.InputError):
        message.message_sendlater(owner['token'], channel_1['channel_id'],
                        message_for_sending, send_time)


def test_message_sendlater_invalid_time():
    '''
    tests the message_sendlater functionality
    '''
    other.clear()
    send_time = int(time.time()) - 1000
    owner = auth.auth_register("user1@email.com", "password", "Homer", "Simpson")
    channel_1 = channels.channels_create(owner['token'], "channel_1", True)
    with pytest.raises (error.InputError):
        message.message_sendlater(owner['token'], channel_1['channel_id'],
                        'this is the first test message', send_time)
    
def test_message_sendlater_not_a_member():
    '''
    tests the message_sendlater functionality
    '''
    other.clear()
    send_time = int(time.time()) + 10
    owner = auth.auth_register("user1@email.com", "password", "Homer", "Simpson")
    user = auth.auth_register("user2@email.com", "password2", "Marge", "Simpson")
    channel_1 = channels.channels_create(owner['token'], "channel_1", True)
    with pytest.raises (error.AccessError):
        message.message_sendlater(user['token'], channel_1['channel_id'],
                        'this is the first test message', send_time)