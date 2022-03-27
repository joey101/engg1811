'''
File that tests that all the https endpoint routes
work correctly for channel functions.
'''
import re
from subprocess import Popen, PIPE
import signal
from time import sleep
import requests
import pytest

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
def registered_user_with_created_channel(url):
    user = requests.post(f"{url}/auth/register", json={
        'email' : 'example@example.com',
        'password' : 'verystrongpassword1234',
        'name_first' : 'Will',
        'name_last' : 'Smith'
    })

    user_data = user.json()

    channel_1 = requests.post(f"{url}/channels/create", json={
        'token' : user_data['token'],
        'name' : 'Test Channel',
        'is_public' : True
    })

    channel_data = channel_1.json()
    return {
        'user_data' : user_data,
        'channel_data' : channel_data

    }

def test_channel_details(url, registered_user_with_created_channel):
    '''
    Test that channel_details works on the server
    '''
    owner_data = registered_user_with_created_channel['user_data']
    channel_data = registered_user_with_created_channel['channel_data']

    owner_dict = {'u_id': owner_data['u_id'], 'name_first': 'Will', 'name_last': 'Smith', 'profile_img_url' : ""}

    r = requests.get(f"{url}/channel/details?token={owner_data['token']}&channel_id={channel_data['channel_id']}")
    details = r.json()

    assert details == {
        'name': 'Test Channel',
        'owner_members': [owner_dict],
        'all_members': [owner_dict]
    }

def test_channel_details_invalid_id(url):
    '''
    Test that the server catches an exception for invalid channel id
    '''
    owner = requests.post(f"{url}/auth/register", json={
        'email' : 'example@example.com',
        'password' : 'verystrongpassword1234',
        'name_first' : 'Homer',
        'name_last' : 'Simpson'
    })

    owner_data = owner.json()

    r = requests.get(f"{url}/channel/details?token={owner_data['token']}&channel_id=1")
    error_check = r.json()

    assert error_check['code'] == 400

def test_channels_create(url, registered_user_with_created_channel):
    '''
    Test that the user is able to create a channel on the server
    '''
    channel_data = registered_user_with_created_channel['channel_data']
    assert channel_data['channel_id'] == 1

def test_channels_create_name_too_long(url, registered_user_with_created_channel):
    '''
    Test that the server raises an error code for a channel name thats too long
    '''

    user_data = registered_user_with_created_channel['user_data']

    channel_1 = requests.post(f"{url}/channels/create", json={
        'token' : user_data['token'],
        'name' : 'veryveryveryveryveryveryveryveryvery long channel name',
        'is_public' : False
    })

    error_caught = channel_1.json()
    assert error_caught['code'] == 400

def test_channels_list(url):
    '''
    Test that the user is able to list channels on the server
    '''

    # registers a user
    user = requests.post(f"{url}/auth/register", json={
        'email' : 'example@example.com',
        'password' : 'verystrongpassword1234',
        'name_first' : 'Will',
        'name_last' : 'Smith'
    })

    user_data = user.json()

    # Creates three channels 
    requests.post(f"{url}/channels/create", json={
        'token' : user_data['token'],
        'name' : 'Test Channel',
        'is_public' : True
    })

    requests.post(f"{url}/channels/create", json={
        'token' : user_data['token'],
        'name' : 'Test Channel 2',
        'is_public' : True
    })

    requests.post(f"{url}/channels/create", json={
        'token' : user_data['token'],
        'name' : 'Test Channel 3',
        'is_public' : True
    })

    # Calls the route for channels_list to return the channels
    r = requests.get(f"{url}/channels/list?token={user_data['token']}")

    payload = r.json()
    assert payload == {
        'channels' : [
            {
                'channel_id' : 1,
                'name' : "Test Channel"
            },
            {
                'channel_id' : 2,
                'name' : "Test Channel 2"
            },
            {
                'channel_id' : 3,
                'name' : "Test Channel 3"
            }
        ]
    }

def test_channels_listall(url):
    '''
    Test that the user is able to list all channels in the server
    '''
    

    # Registers a user
    user = requests.post(f"{url}/auth/register", json={
        'email' : 'example@example.com',
        'password' : 'verystrongpassword1234',
        'name_first' : 'Will',
        'name_last' : 'Smith'
    })

    user_data = user.json()

    # Creates multiple channels using the post request for channel_create
    requests.post(f"{url}/channels/create", json={
        'token' : user_data['token'],
        'name' : 'Test Channel',
        'is_public' : True
    })

    requests.post(f"{url}/channels/create", json={
        'token' : user_data['token'],
        'name' : 'Test Channel 2',
        'is_public' : True
    })

    requests.post(f"{url}/channels/create", json={
        'token' : user_data['token'],
        'name' : 'Test Channel 3',
        'is_public' : True
    })

    requests.post(f"{url}/channels/create", json={
        'token' : user_data['token'],
        'name' : 'Private Channel',
        'is_public' : False
    })

    # Uses the flask route for channels_list to receive all available channels
    r = requests.get(f"{url}/channels/list?token={user_data['token']}")

    payload = r.json()
    assert payload == {
        'channels' : [
            {
                'channel_id' : 1,
                'name' : "Test Channel"
            },
            {
                'channel_id' : 2,
                'name' : "Test Channel 2"
            },
            {
                'channel_id' : 3,
                'name' : "Test Channel 3"
            },
            {
                'channel_id' : 4,
                'name' : "Private Channel"
            }
        ]
    }

def test_channel_invite(url, registered_user_with_created_channel):
    '''
    Test that channel_invite works on the server
    '''
    

    owner_data = registered_user_with_created_channel['user_data']
    channel_data = registered_user_with_created_channel['channel_data']

    # Register a second user to be invited
    user = requests.post(f"{url}/auth/register", json={
        'email' : 'example2@example.com',
        'password' : 'verystrongpassword1234',
        'name_first' : 'Bart',
        'name_last' : 'Simpson'
    })

    user_data = user.json()

    owner_dict = {'u_id': owner_data['u_id'], 'name_first': 'Will', 'name_last': 'Smith', 'profile_img_url' : ""}
    inved_user_dict = {'u_id': user_data['u_id'], 'name_first': 'Bart', 'name_last': 'Simpson', 'profile_img_url' : ""}

    # Invite the second user using the flask route for channel_invite
    requests.post(f"{url}/channel/invite", json={
        'token' : owner_data['token'],
        'channel_id' : channel_data['channel_id'],
        'u_id' : user_data['u_id']
    })

    # Get the channel details for that server to assert 2nd user was invited successfully
    r = requests.get(f"{url}/channel/details?token={user_data['token']}&channel_id={channel_data['channel_id']}")
    details = r.json()

    assert details == {
        'name': 'Test Channel',
        'owner_members': [owner_dict],
        'all_members': [owner_dict, inved_user_dict]
    }


def test_channel_addowner_functionality(url, registered_user_with_created_channel):
    '''
    Test that adding a owner works on the server
    '''
    # Register a user that will be the original owner of the channel
    

    # Register a user that will be added as an owner of a channel
    user1 = requests.post(f"{url}/auth/register", json={
        'email' : 'user1@example.com',
        'password' : 'verystrongpassword1234',
        'name_first' : 'Bart',
        'name_last' : 'Simpson'
    })

    owner_data = registered_user_with_created_channel['user_data']
    user1_data = user1.json()

    # Create a channel
    channel_data = registered_user_with_created_channel['channel_data']

    owner_dict = {'u_id': owner_data['u_id'], 'name_first': 'Will', 'name_last': 'Smith', 'profile_img_url' : ""}
    user1_dict = {'u_id': user1_data['u_id'], 'name_first': 'Bart', 'name_last': 'Simpson', 'profile_img_url' : ""}

    # Invite user to the channel first
    requests.post(f"{url}/channel/invite", json={
        'token' : owner_data['token'],
        'channel_id' : channel_data['channel_id'],
        'u_id' : user1_data['u_id']
    })

    # Add the user as an owner
    requests.post(f"{url}/channel/addowner", json={
        'token': owner_data['token'],
        'channel_id': channel_data['channel_id'],
        'u_id': user1_data['u_id']
    })

    # Get the details of the channel to assert the user was added as an owner successfully
    r = requests.get(f"{url}/channel/details?token={user1_data['token']}&channel_id={channel_data['channel_id']}")

    details = r.json()

    assert details == {
        'name': 'Test Channel',
        'owner_members': [owner_dict, user1_dict],
        'all_members': [owner_dict, user1_dict]
    }

def test_channel_addowner_on_an_invalid_channel(url, registered_user_with_created_channel):
    '''
    Test to check that an error is raised if an invalid channel is passed in add owner
    '''
    user1 = requests.post(f"{url}/auth/register", json={
        'email' : 'user1@example.com',
        'password' : 'verystrongpassword1234',
        'name_first' : 'Bart',
        'name_last' : 'Simpson'
    })

    owner_data = registered_user_with_created_channel['user_data']
    user1_data = user1.json()

    # Create a channel
    channel_data = registered_user_with_created_channel['channel_data']

    # Invite user to the channel first
    requests.post(f"{url}/channel/invite", json={
        'token' : owner_data['token'],
        'channel_id' : channel_data['channel_id'],
        'u_id' : user1_data['u_id']
    })

    # Add the user as an owner
    error = requests.post(f"{url}/channel/addowner", json={
        'token': owner_data['token'],
        'channel_id': 9999,
        'u_id': user1_data['u_id']
    })

    error_check = error.json()
    assert error_check['code'] == 400

def test_channel_removeowner_functionality(url, registered_user_with_created_channel):
    '''
    Test for checking removeowner works on the server
    '''

    # Register an owner that will be added as an owner and then removed
    user1 = requests.post(f"{url}/auth/register", json={
        'email' : 'user1@example.com',
        'password' : 'verystrongpassword1234',
        'name_first' : 'Bart',
        'name_last' : 'Simpson'
    })

    owner_data = registered_user_with_created_channel['user_data']
    channel_data = registered_user_with_created_channel['channel_data']
    user1_data = user1.json()

    owner_dict = {'u_id': owner_data['u_id'], 'name_first': 'Will', 'name_last': 'Smith', 'profile_img_url' : ""}
    user1_dict = {'u_id': user1_data['u_id'], 'name_first': 'Bart', 'name_last': 'Simpson', 'profile_img_url' : ""}

    # Invite user to the channel first
    requests.post(f"{url}/channel/invite", json={
        'token' : owner_data['token'],
        'channel_id' : channel_data['channel_id'],
        'u_id' : user1_data['u_id']
    })

    # Add the user as an owner
    requests.post(f"{url}/channel/addowner", json={
        'token': owner_data['token'],
        'channel_id': channel_data['channel_id'],
        'u_id': user1_data['u_id']
    })

    # Then remove the same user from being an owner
    requests.post(f"{url}/channel/removeowner", json={
        'token': owner_data['token'],
        'channel_id': channel_data['channel_id'],
        'u_id': user1_data['u_id']
    })

    # Get the details of the channel to assert the owners list is correct
    r = requests.get(f"{url}/channel/details?token={user1_data['token']}&channel_id={channel_data['channel_id']}")

    details = r.json()

    assert details == {
        'name': 'Test Channel',
        'owner_members': [owner_dict],
        'all_members': [owner_dict, user1_dict]
    }

def test_channel_removeowner_on_an_invalid_channel(url, registered_user_with_created_channel):
    '''
    Test to check that an error is raised if an invalid channel is passed in add owner
    '''
    user1 = requests.post(f"{url}/auth/register", json={
        'email' : 'user1@example.com',
        'password' : 'verystrongpassword1234',
        'name_first' : 'Bart',
        'name_last' : 'Simpson'
    })

    owner_data = registered_user_with_created_channel['user_data']
    user1_data = user1.json()

    # Create a channel
    channel_data = registered_user_with_created_channel['channel_data']

    # Invite user to the channel first
    requests.post(f"{url}/channel/invite", json={
        'token' : owner_data['token'],
        'channel_id' : channel_data['channel_id'],
        'u_id' : user1_data['u_id']
    })

    # Add the user as an owner
    requests.post(f"{url}/channel/addowner", json={
        'token': owner_data['token'],
        'channel_id': 9999,
        'u_id': user1_data['u_id']
    })

    # Then remove the same user from being an owner
    error = requests.post(f"{url}/channel/removeowner", json={
        'token': owner_data['token'],
        'channel_id': 9999,
        'u_id': user1_data['u_id']
    })

    error_check = error.json()
    assert error_check['code'] == 400

def test_channel_invite_invalid_user(url, registered_user_with_created_channel):
    '''
    Test that an invalid user expection is caught by the server
    '''
    owner_data = registered_user_with_created_channel['user_data']

    channel_data = registered_user_with_created_channel['channel_data']

    error = requests.post(f"{url}/channel/invite", json={
        'token' : owner_data['token'],
        'channel_id' : channel_data['channel_id'],
        'u_id' : 2
    })

    error_check = error.json()
    assert error_check['code'] == 400

def test_channel_messages_fifty_messages(url, registered_user_with_created_channel):
    '''
    Test that channel_messages returns 50 messages
    '''
    message_list = {
        'messages': [],
        'start' : 0,
        'end' : -1
    }
    i = 0
    while i < 50:
        message_list['messages'].append('message {}'.format(50 - i))
        i += 1

    user_data = registered_user_with_created_channel['user_data']
    channel_data = registered_user_with_created_channel['channel_data']

    i = 0
    while i < 50:
        requests.post(f"{url}/message/send", json={
        'token' : user_data['token'],
        'channel_id' : channel_data['channel_id'],
        'message' : f"message {i + 1}"
        })
        i += 1

    r = requests.get(f"{url}/channel/messages?token={user_data['token']}&channel_id={channel_data['channel_id']}&start=0")

    messages_channel = r.json()
    i = 0
    while i < 50:
        assert messages_channel['messages'][i]['message'] == message_list['messages'][i]
        i += 1
    assert messages_channel['start'] == 0
    assert messages_channel['end'] == -1


def test_channel_messages_failure_invalid_start(url, registered_user_with_created_channel):
    '''
    Test that an exception for an invalid start is caught by the server
    '''
    user_data = registered_user_with_created_channel['user_data']
    channel_data = registered_user_with_created_channel['channel_data']

    requests.post(f"{url}/message/send", json={
        'token' : user_data['token'],
        'channel_id' : channel_data['channel_id'],
        'message' : "message 1"
    })

    r = requests.get(f"{url}/channel/messages?token={user_data['token']}&channel_id={channel_data['channel_id']}&start=10")

    error_check = r.json()
    assert error_check['code'] == 400


def test_channel_leave_functionality(url, registered_user_with_created_channel):
    '''
    Test that channel_leave functions on the server
    '''
    owner_data = registered_user_with_created_channel['user_data']
    channel_data = registered_user_with_created_channel['channel_data']

    # Register a second user that will be invited to a server and then leave
    user = requests.post(f"{url}/auth/register", json={
        'email' : 'example2@example.com',
        'password' : 'verystrongpassword1234',
        'name_first' : 'Bart',
        'name_last' : 'Simpson'
    })

    user_data = user.json()

    owner_dict = {'u_id': owner_data['u_id'], 'name_first': 'Will', 'name_last': 'Smith', 'profile_img_url' : ""}

    # User will be invited to the channel
    requests.post(f"{url}/channel/invite", json={
        'token' : owner_data['token'],
        'channel_id' : channel_data['channel_id'],
        'u_id' : user_data['u_id']
    })

    # User will then leave the channel
    requests.post(f"{url}/channel/leave", json={
        'token' : user_data['token'],
        'channel_id' : channel_data['channel_id']
    })

    # Get the details of the channel to assert the only member of the channel is the owner
    r = requests.get(f"{url}/channel/details?token={owner_data['token']}&channel_id={channel_data['channel_id']}")
    details = r.json()

    assert details == {
        'name': 'Test Channel',
        'owner_members': [owner_dict],
        'all_members': [owner_dict]
    }

def test_channel_leave_failure(url, registered_user_with_created_channel):
    '''
    Test that channel_leave raises an error for an invalid channel id
    '''
    owner_data = registered_user_with_created_channel['user_data']
    channel_data = registered_user_with_created_channel['channel_data']

    # Register a second user that will be invited to the channel
    user = requests.post(f"{url}/auth/register", json={
        'email' : 'example2@example.com',
        'password' : 'verystrongpassword1234',
        'name_first' : 'Bart',
        'name_last' : 'Simpson'
    })

    user_data = user.json()

    # Invite the user to the channel
    requests.post(f"{url}/channel/invite", json={
        'token' : owner_data['token'],
        'channel_id' : channel_data['channel_id'],
        'u_id' : user_data['u_id']
    })

    r = requests.get(f"{url}/channel/details?token={owner_data['token']}&channel_id=2")
    error_check = r.json()

    assert error_check['code'] == 400


def test_channel_join_functionality(url, registered_user_with_created_channel):
    '''
    Test that channel_join functions on the server
    '''
    user1_data = registered_user_with_created_channel['user_data']
    channel_data = registered_user_with_created_channel['channel_data']

    user2 = requests.post(f"{url}/auth/register", json={
        'email' : 'example2@example.com',
        'password' : 'verystrongpassword1234',
        'name_first' : 'Bart',
        'name_last' : 'Simpson'
    })

    user2_data = user2.json()

    # User2 will join the channel created by user1
    requests.post(f"{url}/channel/join", json={
        'token' : user2_data['token'],
        'channel_id' : channel_data['channel_id'],
    })

    user1_dict = {'u_id': user1_data['u_id'], 'name_first': 'Will', 'name_last': 'Smith', 'profile_img_url' : ""}
    user2_dict = {'u_id': user2_data['u_id'], 'name_first': 'Bart', 'name_last': 'Simpson', 'profile_img_url' : ""}

    r = requests.get(f"{url}/channel/details?token={user2_data['token']}&channel_id={channel_data['channel_id']}")
    details = r.json()

    assert details == {        
        'name': 'Test Channel',
        'owner_members': [user1_dict],
        'all_members': [user1_dict, user2_dict]
    }

def test_channel_join_failure(url):
    '''
    Test that an error code is returned when channel_join is given an invalid ID
    '''
    requests.post(f"{url}/auth/register", json={
        'email' : 'example@example.com',
        'password' : 'verystrongpassword1234',
        'name_first' : 'Will',
        'name_last' : 'Smith'
    })

    user2 = requests.post(f"{url}/auth/register", json={
        'email' : 'example2@example.com',
        'password' : 'verystrongpassword1234',
        'name_first' : 'Bart',
        'name_last' : 'Simpson'
    })

    user2_data = user2.json()

    requests.post(f"{url}/channel/join", json={
        'token' : user2_data['token'],
        'channel_id' : 1,
    })

    r = requests.get(f"{url}/channel/details?token={user2_data['token']}&channel_id=1")
    error_check = r.json()

    assert error_check['code'] == 400
