'''
Tests for all standup functions
'''
import time
import threading
import pytest
import auth
import channel
import channels
import standup
from error import InputError, AccessError
import other

@pytest.fixture
def create_owner_with_channel_and_user():
    '''
    Basic fixture that registers an owner and a user. The owner creates
    a channel and then invites the user into the channel
    '''
    other.clear()

    owner = auth.auth_register("user1@email.com", "password", "Homer", "Simpson")
    user = auth.auth_register("user2@email.com", "password", "Bart", "Simpson")

    channel_1 = channels.channels_create(owner['token'], "channel_1", False)

    channel.channel_invite(owner['token'], channel_1["channel_id"], user['u_id'])

    return {
        'owner': owner,
        'user': user,
        'channel_1': channel_1
    }

def test_standup_active_functionality(create_owner_with_channel_and_user):
    '''
    A basic test that checks standup_active will return correctly, can't test for
    when a standup is active however.
    '''

    owner = create_owner_with_channel_and_user['owner']
    channel_1 = create_owner_with_channel_and_user['channel_1']

    state = standup.standup_active(owner['token'], channel_1['channel_id'])

    assert state == {
        'is_active': False,
        'time_finish': None
    }

def test_standup_active_invalid_channel(create_owner_with_channel_and_user):
    '''
    Exception test for when an invalid channel is passed through
    '''
    owner = create_owner_with_channel_and_user['owner']

    with pytest.raises(InputError):
        standup.standup_active(owner['token'], 9999)


def test_standup_start_functionality(create_owner_with_channel_and_user):
    '''
    Tests basic functionality of standup_start and checks if it works by
    calling standup_active
    '''

    owner = create_owner_with_channel_and_user['owner']
    channel_1 = create_owner_with_channel_and_user['channel_1']

    assert channel_1['channel_id'] == 1

    standup.standup_start(owner['token'], channel_1['channel_id'], 1)
    expected_finish_time = int(time.time()) + 1

    assert standup.standup_active(owner['token'], channel_1['channel_id']) == {
        'is_active': True,
        'time_finish': expected_finish_time
    }
    time.sleep(1)

def test_standup_start_timer(create_owner_with_channel_and_user):
    '''
    Another test for standup_start to ensure it stays active for
    the time required
    '''

    owner = create_owner_with_channel_and_user['owner']
    channel_1 = create_owner_with_channel_and_user['channel_1']

    standup.standup_start(owner['token'], channel_1['channel_id'], 2)
    expected_finish_time = int(time.time()) + 2

    time.sleep(1)
    assert standup.standup_active(owner['token'], channel_1['channel_id']) == {
        'is_active': True,
        'time_finish': expected_finish_time
    }
    time.sleep(1)

def test_standup_start_invalid_channel(create_owner_with_channel_and_user):
    '''
    Exception test to check if an error is raised when an invalid channel is passed
    through
    '''

    owner = create_owner_with_channel_and_user['owner']

    with pytest.raises(InputError):
        standup.standup_start(owner['token'], 9999, 5)

def test_standup_start_when_already_active(create_owner_with_channel_and_user):
    '''
    Exception test to check if an error is raised when standup_start is called
    when another standup is already active
    '''

    owner = create_owner_with_channel_and_user['owner']
    channel_1 = create_owner_with_channel_and_user['channel_1']

    standup.standup_start(owner['token'], channel_1['channel_id'], 1)

    state = standup.standup_active(owner['token'], channel_1['channel_id'])
    assert state['is_active']

    with pytest.raises(InputError):
        standup.standup_start(owner['token'], channel_1['channel_id'], 5)

def test_standup_send_functionality(create_owner_with_channel_and_user):
    '''
    Checks that standup_send actually works correctly and sends through a
    message in the correct format
    '''

    owner = create_owner_with_channel_and_user['owner']
    channel_1 = create_owner_with_channel_and_user['channel_1']
    user = create_owner_with_channel_and_user['user']

    standup.standup_start(owner['token'], channel_1['channel_id'], 2)

    standup.standup_send(owner['token'], channel_1['channel_id'], "Message 1 sent")
    standup.standup_send(user['token'], channel_1['channel_id'], "Message 2 sent")


    expected_message = '''homersimpson: Message 1 sent\nbartsimpson: Message 2 sent'''

    time.sleep(2)

    message_list = channel.channel_messages(owner['token'], channel_1['channel_id'], 0)

    standup_message = message_list['messages'][0]

    assert standup_message['message_id'] == 1
    assert standup_message['u_id'] == owner['u_id']
    assert standup_message['message'] == expected_message

def test_standup_send_invalid_channel(create_owner_with_channel_and_user):
    '''
    Test that checks if an exception is raised when an invalid channel
    is passed through when standup_send is called
    '''

    owner = create_owner_with_channel_and_user['owner']
    channel_1 = create_owner_with_channel_and_user['channel_1']

    standup.standup_start(owner['token'], channel_1['channel_id'], 1)

    with pytest.raises(InputError):
        standup.standup_send(owner['token'], 9999, "Message123")


def test_standup_send_invalid_length(create_owner_with_channel_and_user):
    '''
    Test that checks if an exception is raised when a message over 1000
    characters is passed through with standup_send
    '''

    owner = create_owner_with_channel_and_user['owner']
    channel_1 = create_owner_with_channel_and_user['channel_1']

    standup.standup_start(owner['token'], channel_1['channel_id'], 1)

    test_message = 'a' * 1001

    with pytest.raises(InputError):
        standup.standup_send(owner['token'], channel_1['channel_id'], test_message)
    

def test_standup_send_in_non_active_standup(create_owner_with_channel_and_user):
    '''
    Test that checks if an exception is raised correctly when standup_send is
    called in a channel where a standup is not active
    '''

    owner = create_owner_with_channel_and_user['owner']
    channel_1 = create_owner_with_channel_and_user['channel_1']

    test_message = 'a' * 1000

    with pytest.raises(InputError):
        standup.standup_send(owner['token'], channel_1['channel_id'], test_message)

def test_standup_send_for_user_not_in_channel(create_owner_with_channel_and_user):
    '''
    Test that checks if an exception is raised when a user not in the channel uses
    standup_send
    '''

    owner = create_owner_with_channel_and_user['owner']
    channel_1 = create_owner_with_channel_and_user['channel_1']

    random_user = auth.auth_register('random@email.com', 'password123', 'Ned', 'Flanders')
    test_message = 'a' * 1000

    standup.standup_start(owner['token'], channel_1['channel_id'], 1)

    with pytest.raises(AccessError):
        standup.standup_send(random_user['token'], channel_1['channel_id'], test_message)

