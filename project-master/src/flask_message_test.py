'''
This file contains all the tests to make sure that the
message functions work through the server routes
'''
import re
from subprocess import Popen, PIPE
import signal
from time import sleep
import pytest
import requests
import time



# Use this fixture to get the URL of the server. It starts the server for you,
# so you don't need to.
@pytest.fixture
def url():
    url_re = re.compile(r' \* Running on ([^ ]*)')
    server = Popen(["python3", "src/server.py"], stderr=PIPE, stdout=PIPE)
    line = server.stderr.readline()
    local_url = url_re.match(line.decode())
    if local_url:
        yield local_url.group(1)
        # Terminate the server
        server.send_signal(signal.SIGINT)
        waited = 0
        while server.poll() is None and waited < 5:
            sleep(0.1)
            waited += 0.1
        if server.poll() is None:
            server.kill()
    else:
        server.kill()
        raise Exception("Couldn't get URL from local server")

@pytest.fixture
def registered_user(url):
    '''
    pytest fixture that registers the first user
    to be used in the tests
    '''
    user = requests.post(f"{url}/auth/register", json={
        'email' : 'example@example.com',
        'password' : 'verystrongpassword1234',
        'name_first' : 'Will',
        'name_last' : 'Smith'
    })

    user_data = user.json()

    return user_data

def test_message_send_functionality(url, registered_user):
    '''
    Tests that mesasge_send works on the flask server
    '''

    user_data = registered_user

    # creates a channel
    channel_1 = requests.post(f"{url}/channels/create", json={
        'token' : user_data['token'],
        'name' : 'Test Channel',
        'is_public' : True
    })

    channel_data = channel_1.json()

    # sends a message to the channel
    r = requests.post(f"{url}/message/send", json={
        'token' : user_data['token'],
        'channel_id' : channel_data['channel_id'],
        'message' : 'test message'
    })

    # check if the correct message_id is returned
    payload = r.json()
    assert payload == {
        'message_id' : 1
    }


def test_mesasge_send_message_too_long(url, registered_user):
    '''
    Tests that message_send raises an InputError for the server if a message is
    too long
    '''

    user_data = registered_user
   
    channel_1 = requests.post(f"{url}/channels/create", json={
        'token' : user_data['token'],
        'name' : 'Test Channel',
        'is_public' : True
    })

    channel_data = channel_1.json()

    test_message = 'a' * 1001

    # should return an error code since the message is one
    # character too long
    r = requests.post(f"{url}/message/send", json={
        'token' : user_data['token'],
        'channel_id' : channel_data['channel_id'],
        'message' : test_message
    })

    error_check = r.json()
    assert error_check['code'] == 400


def test_message_remove_functionality(url, registered_user):
    '''
    Tests that message_remove works on the flask server
    '''

    owner = registered_user

    channel_1 = requests.post(f"{url}/channels/create", json={
        'token' : owner['token'],
        'name' : 'Test Channel',
        'is_public' : True
    })
    channel1 = channel_1.json()
    
    message_sent = requests.post(f"{url}/message/send", json={
        'token' : owner['token'],
        'channel_id' : channel1['channel_id'],
        'message' : 'test message'
    })

    message_data = message_sent.json()

    # remove the specified message
    requests.delete(f"{url}/message/remove", json={
        'token' : owner['token'],
        'message_id' : message_data['message_id']
    })

    # Check in the channel if the message has been removed by using channel_messages
    r = requests.get(f"{url}/channel/messages?token={owner['token']}&channel_id={channel1['channel_id']}&start=0")

    messages_channel = r.json()
    # assert that there is no mesasges in the channel since 
    # the message got removed
    assert messages_channel == {
        'messages': [], 
        'start': 0, 
        'end': -1
        }


def test_message_remove_input_error(url, registered_user):
    '''
    Tests that message_remove raises an input error when there is no message with that id
    '''

    owner = registered_user
    
    channel_1 = requests.post(f"{url}/channels/create", json={
        'token' : owner['token'],
        'name' : 'Test Channel',
        'is_public' : True
    })
    channel1 = channel_1.json()
    
    message_sent = requests.post(f"{url}/message/send", json={
        'token' : owner['token'],
        'channel_id' : channel1['channel_id'],
        'message' : 'test message'
    })
    message_data = message_sent.json()
    
    requests.delete(f"{url}/message/remove", json={
        'token' : owner['token'],
        'message_id' : message_data['message_id']
    })

    # should return a dictionary with error code 400
    r = requests.delete(f"{url}/message/remove", json={
        'token' : owner['token'],
        'message_id' : message_data['message_id']
    })

    error_check = r.json()
    assert error_check['code'] == 400


def test_message_remove_non_owner_remove_access_error(url, registered_user):
    '''
    Tests that message_remove raises an access error when remover is not an owner
    '''

    owner = registered_user

    user2 = requests.post(f"{url}/auth/register", json={
        'email' : 'example2@example.com',
        'password' : 'verystrongpassword1234',
        'name_first' : 'John',
        'name_last' : 'Smith'
    })
    member = user2.json()

    channel_1 = requests.post(f"{url}/channels/create", json={
        'token' : owner['token'],
        'name' : 'Test Channel',
        'is_public' : True
    })
    channel1 = channel_1.json()

    requests.post(f"{url}/channel/join", json={
        'token' : member['token'],
        'channel_id' : channel1['channel_id']
    })

    message_sent = requests.post(f"{url}/message/send", json={
        'token' : owner['token'],
        'channel_id' : channel1['channel_id'],
        'message' : 'test message'
    })
    message_data = message_sent.json()

    # Should return a dictionary with error code 400 as the user cannot
    # remove a message sent by the owner
    r = requests.delete(f"{url}/message/remove", json={
        'token' : member['token'],
        'message_id' : message_data['message_id']
    })
    error_caught = r.json()
    assert error_caught['code'] == 400


def test_message_edit_functionality(url, registered_user):
    '''
    Test that a message can be edited in the server
    '''

    user1_data = registered_user

    channel_1 = requests.post(f"{url}/channels/create", json={
        'token' : user1_data['token'],
        'name' : 'Test Channel',
        'is_public' : True
    })

    channel_data = channel_1.json()

    message_sent = requests.post(f"{url}/message/send", json={
        'token' : user1_data['token'],
        'channel_id' : channel_data['channel_id'],
        'message' : 'Test message'
    })
    
    message_data = message_sent.json()

    requests.put(f"{url}/message/edit", json={
        'token' : user1_data['token'],
        'message_id' : message_data['message_id'],
        'message' : 'edited message'
    })

    # Use channel_messages to check if the mesasge has been edited
    r = requests.get(f"{url}/channel/messages?token={user1_data['token']}&channel_id={channel_data['channel_id']}&start=0")

    messages_channel = r.json()

    assert messages_channel['messages'][0]['message'] == 'edited message'

def test_message_edit_failure(url, registered_user):
    '''
    Test that a message can be edited in the server
    '''

    user1_data = registered_user

    user2 = requests.post(f"{url}/auth/register", json={
        'email' : 'example2@example.com',
        'password' : 'verystrongpassword1234',
        'name_first' : 'John',
        'name_last' : 'Smith'
    })

    user2_data = user2.json()


    channel_1 = requests.post(f"{url}/channels/create", json={
        'token' : user1_data['token'],
        'name' : 'Test Channel',
        'is_public' : True
    })

    channel_data = channel_1.json()

    requests.post(f"{url}/channel/join", json={
        'token' : user2_data['token'],
        'channel_id' : channel_data['channel_id']
    })

    message_sent = requests.post(f"{url}/message/send", json={
        'token' : user1_data['token'],
        'channel_id' : channel_data['channel_id'],
        'message' : 'Test message'
    })
    
    message_data = message_sent.json()

    # Should return a dictionary with error code as user2 cannot 
    # edit user1's message
    r = requests.put(f"{url}/message/edit", json={
        'token' : user2_data['token'],
        'message_id' : message_data['message_id'],
        'message' : 'edited message'
    })

    error_check = r.json()

    assert error_check['code'] == 400

def test_message_react_functionality(url, registered_user):
    '''
    test that message react works on the flask server
    '''
    user1_data = registered_user

    channel_1 = requests.post(f"{url}/channels/create", json={
        'token' : user1_data['token'],
        'name' : 'Test Channel',
        'is_public' : True
    })

    channel_data = channel_1.json()

    message_sent = requests.post(f"{url}/message/send", json={
        'token' : user1_data['token'],
        'channel_id' : channel_data['channel_id'],
        'message' : 'Test message'
    })
    
    message_data = message_sent.json()

    requests.post(f"{url}/message/react", json={
        'token' : user1_data['token'],
        'message_id' : message_data['message_id'],
        'react_id' : 1
    })

    r = requests.get(f"{url}/channel/messages?token={user1_data['token']}&channel_id={channel_data['channel_id']}&start=0")

    messages_channel = r.json()

    assert messages_channel['messages'][0]['reacts'][0]['react_id'] == 1
    assert messages_channel['messages'][0]['reacts'][0]['is_this_user_reacted'] is True



def test_message_react_invalid_message_id(url, registered_user):
    '''
    test that message react raises InputError on the flask server
    for invalid message_id
    '''
    user1_data = registered_user

    channel_1 = requests.post(f"{url}/channels/create", json={
        'token' : user1_data['token'],
        'name' : 'Test Channel',
        'is_public' : True
    })

    channel_data = channel_1.json()

    requests.post(f"{url}/message/send", json={
        'token' : user1_data['token'],
        'channel_id' : channel_data['channel_id'],
        'message' : 'Test message'
    })

    r = requests.post(f"{url}/message/react", json={
        'token' : user1_data['token'],
        'message_id' : 10,
        'react_id' : 1
    })

    error_check = r.json()

    assert error_check['code'] == 400


def test_message_react_invalid_react_id(url, registered_user):
    '''
    test that message react raises InputError on the flask server
    for invalid message_id
    '''
    user1_data = registered_user

    channel_1 = requests.post(f"{url}/channels/create", json={
        'token' : user1_data['token'],
        'name' : 'Test Channel',
        'is_public' : True
    })

    channel_data = channel_1.json()

    message_sent = requests.post(f"{url}/message/send", json={
        'token' : user1_data['token'],
        'channel_id' : channel_data['channel_id'],
        'message' : 'Test message'
    })
    
    message_data = message_sent.json()

    r = requests.post(f"{url}/message/react", json={
        'token' : user1_data['token'],
        'message_id' : message_data['message_id'],
        'react_id' : 2
    })

    error_check = r.json()

    assert error_check['code'] == 400

def test_message_react_already_reacted(url, registered_user):
    '''
    test that message react raises InputError on the flask server
    for message that user already reacted to
    '''
    user1_data = registered_user

    channel_1 = requests.post(f"{url}/channels/create", json={
        'token' : user1_data['token'],
        'name' : 'Test Channel',
        'is_public' : True
    })

    channel_data = channel_1.json()

    message_sent = requests.post(f"{url}/message/send", json={
        'token' : user1_data['token'],
        'channel_id' : channel_data['channel_id'],
        'message' : 'Test message'
    })
    
    message_data = message_sent.json()

    requests.post(f"{url}/message/react", json={
        'token' : user1_data['token'],
        'message_id' : message_data['message_id'],
        'react_id' : 1
    })

    r = requests.post(f"{url}/message/react", json={
        'token' : user1_data['token'],
        'message_id' : message_data['message_id'],
        'react_id' : 2
    })

    error_check = r.json()

    assert error_check['code'] == 400


def test_message_unreact_functionality(url, registered_user):
    '''
    Test that message_unreact raises an error for unreacting
    to a message with no reacts
    '''
    user1_data = registered_user

    channel_1 = requests.post(f"{url}/channels/create", json={
        'token' : user1_data['token'],
        'name' : 'Test Channel',
        'is_public' : True
    })

    channel_data = channel_1.json()

    message_sent = requests.post(f"{url}/message/send", json={
        'token' : user1_data['token'],
        'channel_id' : channel_data['channel_id'],
        'message' : 'Test message'
    })
    
    message_data = message_sent.json()

    requests.post(f"{url}/message/react", json={
        'token' : user1_data['token'],
        'message_id' : message_data['message_id'],
        'react_id' : 1
    })

    requests.post(f"{url}/message/unreact", json={
        'token' : user1_data['token'],
        'message_id' : message_data['message_id'],
        'react_id' : 1
    })

    r = requests.get(f"{url}/channel/messages?token={user1_data['token']}&channel_id={channel_data['channel_id']}&start=0")

    messages_channel = r.json()

    assert messages_channel['messages'][0]['reacts'][0]['u_ids'] == []


def test_message_unreact_no_reacts(url, registered_user):
    '''
    Test that message_unreact raises an error for unreacting
    to a message with no reacts
    '''
    user1_data = registered_user

    channel_1 = requests.post(f"{url}/channels/create", json={
        'token' : user1_data['token'],
        'name' : 'Test Channel',
        'is_public' : True
    })

    channel_data = channel_1.json()

    message_sent = requests.post(f"{url}/message/send", json={
        'token' : user1_data['token'],
        'channel_id' : channel_data['channel_id'],
        'message' : 'Test message'
    })
    
    message_data = message_sent.json()


    r = requests.post(f"{url}/message/unreact", json={
        'token' : user1_data['token'],
        'message_id' : message_data['message_id'],
        'react_id' : 1
    })

    error_check = r.json()
    assert error_check['code'] == 400

def test_message_unreact_invalid_react_id(url, registered_user):
    '''
    Test that message_unreact raises an error for unreacting
    to a message with an invalid react id
    '''
    user1_data = registered_user

    channel_1 = requests.post(f"{url}/channels/create", json={
        'token' : user1_data['token'],
        'name' : 'Test Channel',
        'is_public' : True
    })

    channel_data = channel_1.json()

    message_sent = requests.post(f"{url}/message/send", json={
        'token' : user1_data['token'],
        'channel_id' : channel_data['channel_id'],
        'message' : 'Test message'
    })
    
    message_data = message_sent.json()

    requests.post(f"{url}/message/react", json={
        'token' : user1_data['token'],
        'message_id' : message_data['message_id'],
        'react_id' : 1
    })

    r = requests.post(f"{url}/message/unreact", json={
        'token' : user1_data['token'],
        'message_id' : message_data['message_id'],
        'react_id' : 2
    })

    error_check = r.json()
    assert error_check['code'] == 400


def test_message_uneact_invalid_message_id(url, registered_user):
    '''
    Test that message_unreact raises an error for unreacting
    to a message with an invalid react id
    '''
    user1_data = registered_user

    channel_1 = requests.post(f"{url}/channels/create", json={
        'token' : user1_data['token'],
        'name' : 'Test Channel',
        'is_public' : True
    })

    channel_data = channel_1.json()

    message_sent = requests.post(f"{url}/message/send", json={
        'token' : user1_data['token'],
        'channel_id' : channel_data['channel_id'],
        'message' : 'Test message'
    })
    
    message_data = message_sent.json()

    requests.post(f"{url}/message/react", json={
        'token' : user1_data['token'],
        'message_id' : message_data['message_id'],
        'react_id' : 1
    })

    r = requests.post(f"{url}/message/unreact", json={
        'token' : user1_data['token'],
        'message_id' : 2,
        'react_id' : 1
    })

    error_check = r.json()
    assert error_check['code'] == 400

def test_message_pin(url, registered_user):
    '''
    Test that message_pin works on the flask server
    '''
    user1_data = registered_user

    channel_1 = requests.post(f"{url}/channels/create", json={
        'token' : user1_data['token'],
        'name' : 'Test Channel',
        'is_public' : True
    })

    channel_data = channel_1.json()

    message_sent = requests.post(f"{url}/message/send", json={
        'token' : user1_data['token'],
        'channel_id' : channel_data['channel_id'],
        'message' : 'Test message'
    })
    
    message_data = message_sent.json()

    requests.post(f"{url}/message/pin", json={
        'token' : user1_data['token'],
        'message_id' : message_data['message_id']
    })

    r = requests.get(f"{url}/channel/messages?token={user1_data['token']}&channel_id={channel_data['channel_id']}&start=0")

    messages_channel = r.json()

    assert messages_channel['messages'][0]['is_pinned'] is True


def test_message_pin_invalid_message_id(url, registered_user):
    '''
    Test that the server raises an error code when a message
    with an invalid message id is attempted to be pinned
    '''
    user1_data = registered_user

    channel_1 = requests.post(f"{url}/channels/create", json={
        'token' : user1_data['token'],
        'name' : 'Test Channel',
        'is_public' : True
    })

    channel_data = channel_1.json()

    requests.post(f"{url}/message/send", json={
        'token' : user1_data['token'],
        'channel_id' : channel_data['channel_id'],
        'message' : 'Test message'
    })
    

    r = requests.post(f"{url}/message/pin", json={
        'token' : user1_data['token'],
        'message_id' : 10
    })

    error_check = r.json()

    assert error_check['code'] == 400


def test_message_pin_already_pinned(url, registered_user):
    '''
    test that the server raises an error code when
    a message already pinned is attempted to be pinned
    again
    '''
    user1_data = registered_user

    channel_1 = requests.post(f"{url}/channels/create", json={
        'token' : user1_data['token'],
        'name' : 'Test Channel',
        'is_public' : True
    })

    channel_data = channel_1.json()

    message_sent = requests.post(f"{url}/message/send", json={
        'token' : user1_data['token'],
        'channel_id' : channel_data['channel_id'],
        'message' : 'Test message'
    })
    
    message_data = message_sent.json()

    requests.post(f"{url}/message/pin", json={
        'token' : user1_data['token'],
        'message_id' : message_data['message_id']
    })

    r = requests.post(f"{url}/message/pin", json={
        'token' : user1_data['token'],
        'message_id' : message_data['message_id']
    })

    error_check = r.json()

    assert error_check['code'] == 400


def test_message_pin_no_required_permissions(url, registered_user):
    '''
    test that the server raises an error code when
    a user without the required permissions tries to pin a
    message
    '''
    user1_data = registered_user

    user2 = requests.post(f"{url}/auth/register", json={
        'email' : 'example2@example.com',
        'password' : 'verystrongpassword1234',
        'name_first' : 'Will',
        'name_last' : 'Smith'
    })

    user2_data = user2.json()

    channel_1 = requests.post(f"{url}/channels/create", json={
        'token' : user1_data['token'],
        'name' : 'Test Channel',
        'is_public' : True
    })

    channel_data = channel_1.json()

    message_sent = requests.post(f"{url}/message/send", json={
        'token' : user1_data['token'],
        'channel_id' : channel_data['channel_id'],
        'message' : 'Test message'
    })
    
    message_data = message_sent.json()

    r = requests.post(f"{url}/message/pin", json={
        'token' : user2_data['token'],
        'message_id' : message_data['message_id']
    })

    error_check = r.json()

    assert error_check['code'] == 400


def test_message_unpin(url, registered_user):
    '''
    Test that message_unpin works on the flask server
    '''
    user1_data = registered_user

    channel_1 = requests.post(f"{url}/channels/create", json={
        'token' : user1_data['token'],
        'name' : 'Test Channel',
        'is_public' : True
    })

    channel_data = channel_1.json()

    message_sent = requests.post(f"{url}/message/send", json={
        'token' : user1_data['token'],
        'channel_id' : channel_data['channel_id'],
        'message' : 'Test message'
    })
    
    message_data = message_sent.json()

    requests.post(f"{url}/message/pin", json={
        'token' : user1_data['token'],
        'message_id' : message_data['message_id']
    })

    requests.post(f"{url}/message/unpin", json={
        'token' : user1_data['token'],
        'message_id' : message_data['message_id']
    })

    r = requests.get(f"{url}/channel/messages?token={user1_data['token']}&channel_id={channel_data['channel_id']}&start=0")

    messages_channel = r.json()

    assert messages_channel['messages'][0]['is_pinned'] is False


def test_message_unpin_invalid_message_id(url, registered_user):
    '''
    Test that the server returns an error code when an invalid
    message id is given to message_unpin
    '''
    user1_data = registered_user

    channel_1 = requests.post(f"{url}/channels/create", json={
        'token' : user1_data['token'],
        'name' : 'Test Channel',
        'is_public' : True
    })

    channel_data = channel_1.json()

    message_sent = requests.post(f"{url}/message/send", json={
        'token' : user1_data['token'],
        'channel_id' : channel_data['channel_id'],
        'message' : 'Test message'
    })
    
    message_data = message_sent.json()

    requests.post(f"{url}/message/pin", json={
        'token' : user1_data['token'],
        'message_id' : message_data['message_id']
    })

    r = requests.post(f"{url}/message/unpin", json={
        'token' : user1_data['token'],
        'message_id' : 10
    })

    error_check = r.json()

    assert error_check['code'] == 400


def test_message_unpin_already_unpinned(url, registered_user):
    '''
    Test that the server returns an error code when the user tries
    to unpin a message that is already unpinned
    '''
    user1_data = registered_user

    channel_1 = requests.post(f"{url}/channels/create", json={
        'token' : user1_data['token'],
        'name' : 'Test Channel',
        'is_public' : True
    })

    channel_data = channel_1.json()

    message_sent = requests.post(f"{url}/message/send", json={
        'token' : user1_data['token'],
        'channel_id' : channel_data['channel_id'],
        'message' : 'Test message'
    })
    
    message_data = message_sent.json()

    requests.post(f"{url}/message/pin", json={
        'token' : user1_data['token'],
        'message_id' : message_data['message_id']
    })

    requests.post(f"{url}/message/unpin", json={
        'token' : user1_data['token'],
        'message_id' : message_data['message_id']
    })

    r = requests.post(f"{url}/message/unpin", json={
        'token' : user1_data['token'],
        'message_id' : message_data['message_id']
    })

    error_check = r.json()

    assert error_check['code'] == 400


def test_message_unpin_no_required_permissions(url, registered_user):
    '''
    Test that the server returns an error code when the user tries
    to unpin a message that is already unpinned
    '''
    user1_data = registered_user

    user2 = requests.post(f"{url}/auth/register", json={
        'email' : 'example2@example.com',
        'password' : 'verystrongpassword1234',
        'name_first' : 'Will',
        'name_last' : 'Smith'
    })

    user2_data = user2.json()

    channel_1 = requests.post(f"{url}/channels/create", json={
        'token' : user1_data['token'],
        'name' : 'Test Channel',
        'is_public' : True
    })

    channel_data = channel_1.json()

    message_sent = requests.post(f"{url}/message/send", json={
        'token' : user1_data['token'],
        'channel_id' : channel_data['channel_id'],
        'message' : 'Test message'
    })
    
    message_data = message_sent.json()

    r = requests.post(f"{url}/message/pin", json={
        'token' : user1_data['token'],
        'message_id' : message_data['message_id']
    })

    r = requests.post(f"{url}/message/unpin", json={
        'token' : user2_data['token'],
        'message_id' : message_data['message_id']
    })

    error_check = r.json()

    assert error_check['code'] == 400


def test_message_sendlater(url, registered_user):
    '''
    test that message_sendlater functions on the server
    '''

    user1_data = registered_user

    channel_1 = requests.post(f"{url}/channels/create", json={
        'token' : user1_data['token'],
        'name' : 'Test Channel',
        'is_public' : True
    })

    channel_data = channel_1.json()

    requests.post(f"{url}/message/sendlater", json={
        'token' : user1_data['token'],
        'channel_id' : channel_data['channel_id'],
        'message' : 'Test message',
        'time_sent' : int(time.time()) + 5
    })


    r = requests.get(f"{url}/channel/messages?token={user1_data['token']}&channel_id={channel_data['channel_id']}&start=0")

    messages_channel = r.json()

    assert messages_channel['messages'] == []

    time.sleep(5)

    r = requests.get(f"{url}/channel/messages?token={user1_data['token']}&channel_id={channel_data['channel_id']}&start=0")

    messages_channel = r.json()

    assert messages_channel['messages'][0]['message'] == 'Test message'


def test_message_sendlater_invalid_channel_id(url, registered_user):
    '''
    test that message_sendlater returns an error code when
    an invalid chanel_id is given
    '''

    user1_data = registered_user

    requests.post(f"{url}/channels/create", json={
        'token' : user1_data['token'],
        'name' : 'Test Channel',
        'is_public' : True
    })


    r = requests.post(f"{url}/message/sendlater", json={
        'token' : user1_data['token'],
        'channel_id' : 2,
        'message' : 'Test message',
        'time_sent' : int(time.time()) + 5
    })

    error_check = r.json()

    assert error_check['code'] == 400


def test_message_sendlater_message_too_long(url, registered_user):
    '''
    test that message_sendlater returns an error code when
    a message is too long
    '''

    user1_data = registered_user

    channel_1 = requests.post(f"{url}/channels/create", json={
        'token' : user1_data['token'],
        'name' : 'Test Channel',
        'is_public' : True
    })

    channel_data = channel_1.json()

    message_for_sending = 'a' * 1001
    
    r = requests.post(f"{url}/message/sendlater", json={
        'token' : user1_data['token'],
        'channel_id' : channel_data['channel_id'],
        'message' : message_for_sending,
        'time_sent' : int(time.time()) + 5
    })

    error_check = r.json()

    assert error_check['code'] == 400


def test_message_sendlater_invalid_time(url, registered_user):
    '''
    test that message_sendlater returns an error code when
    an invalid time is given
    '''

    user1_data = registered_user

    channel_1 = requests.post(f"{url}/channels/create", json={
        'token' : user1_data['token'],
        'name' : 'Test Channel',
        'is_public' : True
    })

    channel_data = channel_1.json()

    r = requests.post(f"{url}/message/sendlater", json={
        'token' : user1_data['token'],
        'channel_id' : channel_data['channel_id'],
        'message' : 'Test message',
        'time_sent' : int(time.time()) - 5
    })

    error_check = r.json()

    assert error_check['code'] == 400

def test_message_sendlater_unauthorised_user(url, registered_user):
    '''
    test that message_sendlater returns an error code when
    an unauthorised user tries to send a message
    '''

    user1_data = registered_user

    channel_1 = requests.post(f"{url}/channels/create", json={
        'token' : user1_data['token'],
        'name' : 'Test Channel',
        'is_public' : True
    })

    channel_data = channel_1.json()

    user2 = requests.post(f"{url}/auth/register", json={
        'email' : 'example2@example.com',
        'password' : 'verystrongpassword1234',
        'name_first' : 'John',
        'name_last' : 'Smith'
    })

    user2_data = user2.json()

    r = requests.post(f"{url}/message/sendlater", json={
        'token' : user2_data['token'],
        'channel_id' : channel_data['channel_id'],
        'message' : 'Test message',
        'time_sent' : int(time.time()) + 5
    })

    error_check = r.json()

    assert error_check['code'] == 400