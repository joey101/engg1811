import re
import signal
from subprocess import Popen, PIPE
from time import sleep, time
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
def registered_owner_and_user_in_channel(url):
    '''
    Basic fixture that registers an owner and a user. The owner creates
    a channel and then invites the user into the channel
    '''
    r = requests.post(f"{url}/auth/register", json={
        'email': "homer.simpson@gmail.com",
        'password': "abcd1081$#",
        'name_first': "Homer",
        'name_last': "Simpson",
    })
    owner = r.json()

    s = requests.post(f"{url}/auth/register", json={
        'email': "bart.simpson@gmail.com",
        'password': "abcd1081$#",
        'name_first': "Bart",
        'name_last': "Simpson",
    })
    user = s.json()

    c = requests.post(f"{url}/channels/create", json={
        'token': owner['token'],
        'name': "channel_1",
        'is_public': False
    })
    channel_1 = c.json()
    
    requests.post(f"{url}/channel/invite", json={
        'token': owner['token'],
        'channel_id': channel_1['channel_id'],
        'u_id': user['u_id']
    })

    return {
        'owner': owner,
        'user': user,
        'channel_1': channel_1
    }

def test_standup_active_functionality(url, registered_owner_and_user_in_channel):
    '''
    Will test that the standup_active http endpoint works correctly
    '''
    owner = registered_owner_and_user_in_channel['owner']
    channel_1 = registered_owner_and_user_in_channel['channel_1']

    assert owner['u_id'] == 1

    r = requests.get(f"{url}/standup/active?token={owner['token']}&channel_id={channel_1['channel_id']}")
    state = r.json()

    assert state == {
        'is_active': False,
        'time_finish': None
    }

def test_standup_active_invalid_channel(url, registered_owner_and_user_in_channel):
    '''
    Exception test for when an invalid channel is passed through
    '''

    owner = registered_owner_and_user_in_channel['owner']

    r = requests.get(f"{url}/standup/active?token={owner['token']}&channel_id=9999")
    error_caught = r.json()

    assert error_caught['code'] == 400

def test_standup_start_functionality(url, registered_owner_and_user_in_channel):
    '''
    Tests if the http endpoint for standup_start functions correctly
    '''
    owner = registered_owner_and_user_in_channel['owner']
    channel_1 = registered_owner_and_user_in_channel['channel_1']

    requests.post(f"{url}/standup/start", json={
        'token': owner['token'],
        'channel_id': channel_1['channel_id'],
        'length': 1
    })

    expected_finish_time = int(time()) + 1

    s = requests.get(f"{url}/standup/active?token={owner['token']}&channel_id={channel_1['channel_id']}")
    state = s.json()

    assert state == {
        'is_active': True,
        'time_finish': expected_finish_time
    }

    sleep(1)

def test_standup_start_timer(url, registered_owner_and_user_in_channel):
    '''
    Another test for standup_start to ensure it stays active for
    the time required
    '''

    owner = registered_owner_and_user_in_channel['owner']
    channel_1 = registered_owner_and_user_in_channel['channel_1']

    requests.post(f"{url}/standup/start", json={
        'token': owner['token'],
        'channel_id': channel_1['channel_id'],
        'length': 2
    })
    expected_finish_time = int(time()) + 2

    sleep(1)
    s = requests.get(f"{url}/standup/active?token={owner['token']}&channel_id={channel_1['channel_id']}")
    state = s.json()

    assert state == {
        'is_active': True,
        'time_finish': expected_finish_time
    }

    sleep(1)

def test_standup_active_start_channel(url, registered_owner_and_user_in_channel):
    '''
    Exception test for when an invalid channel is passed through
    '''
    owner = registered_owner_and_user_in_channel['owner']
    r = requests.post(f"{url}/standup/start", json={
        'token': owner['token'],
        'channel_id': 9999,
        'length': 1
    })
    error_caught = r.json()
    assert error_caught['code'] == 400

def test_standup_start_when_already_active(url, registered_owner_and_user_in_channel):
    '''
    Test that the correct error is returned when standup_start is called
    when a standup is already active
    '''
    owner = registered_owner_and_user_in_channel['owner']
    channel_1 = registered_owner_and_user_in_channel['channel_1']

    requests.post(f"{url}/standup/start", json={
        'token': owner['token'],
        'channel_id': channel_1['channel_id'],
        'length': 1
    })

    s = requests.post(f"{url}/standup/start", json={
        'token': owner['token'],
        'channel_id': channel_1['channel_id'],
        'length': 1
    })
    error_caught = s.json()
    assert error_caught['code'] == 400

def test_standup_send_functionality(url, registered_owner_and_user_in_channel):
    '''
    Test that the http endpoint for standup_send functions correctly
    '''
    owner = registered_owner_and_user_in_channel['owner']
    channel_1 = registered_owner_and_user_in_channel['channel_1']
    user = registered_owner_and_user_in_channel['user']

    requests.post(f"{url}/standup/start", json={
        'token': owner['token'],
        'channel_id': channel_1['channel_id'],
        'length': 1
    })

    requests.post(f"{url}/standup/send", json={
        'token': owner['token'],
        'channel_id': channel_1['channel_id'],
        'message': "Message 1 sent"
    })

    requests.post(f"{url}/standup/send", json={
        'token': user['token'],
        'channel_id': channel_1['channel_id'],
        'message': "Message 2 sent"
    })

    expected_message = '''homersimpson: Message 1 sent\nbartsimpson: Message 2 sent'''
    sleep(2)

    m = requests.get(f"{url}/channel/messages?token={owner['token']}&channel_id={channel_1['channel_id']}&start=0")
    message_list = m.json()
    standup_messages = message_list['messages'][0]

    assert standup_messages['message_id'] == 1
    assert standup_messages['u_id'] == owner['u_id']
    assert standup_messages['message'] == expected_message

def test_standup_send_invalid_channel(url, registered_owner_and_user_in_channel):
    '''
    Test that checks if an exception is raised when an invalid channel
    is passed through when standup_send is called
    '''
    owner = registered_owner_and_user_in_channel['owner']
    channel_1 = registered_owner_and_user_in_channel['channel_1']

    requests.post(f"{url}/standup/start", json={
        'token': owner['token'],
        'channel_id': channel_1['channel_id'],
        'length': 1
    })

    r = requests.post(f"{url}/standup/send", json={
        'token': owner['token'],
        'channel_id': 9999,
        'message': "lol"
    })

    error_caught = r.json()
    assert error_caught['code'] == 400

def test_standup_send_invalid_length(url, registered_owner_and_user_in_channel):
    '''
    Test that checks if an exception is raised when a message over 1000
    characters is passed through with standup_send
    '''
    owner = registered_owner_and_user_in_channel['owner']
    channel_1 = registered_owner_and_user_in_channel['channel_1']

    requests.post(f"{url}/standup/start", json={
        'token': owner['token'],
        'channel_id': channel_1['channel_id'],
        'length': 1
    })

    test_message = 'a' * 1001
    r = requests.post(f"{url}/standup/send", json={
        'token': owner['token'],
        'channel_id': channel_1['channel_id'],
        'message': test_message
    })

    error_caught = r.json()
    assert error_caught['code'] == 400

def test_standup_send_in_non_active_standup(url, registered_owner_and_user_in_channel):
    '''
    Test that checks if an exception is raised correctly when standup_send is
    called in a channel where a standup is not active
    '''
    owner = registered_owner_and_user_in_channel['owner']
    channel_1 = registered_owner_and_user_in_channel['channel_1']

    test_message = 'a' * 1000
    r = requests.post(f"{url}/standup/send", json={
        'token': owner['token'],
        'channel_id': channel_1['channel_id'],
        'message': test_message
    })

    error_caught = r.json()
    assert error_caught['code'] == 400

def test_standup_send_for_user_not_in_channel(url, registered_owner_and_user_in_channel):
    '''
    Test that checks if an exception is raised when a user not in the channel uses
    standup_send
    '''
    owner = registered_owner_and_user_in_channel['owner']
    channel_1 = registered_owner_and_user_in_channel['channel_1']

    n = requests.post(f"{url}/auth/register", json={
        'email': "ned.flanders@email.com",
        'password': "abcd1081$#",
        'name_first': "Ned",
        'name_last': "Flanders",
    })
    random_user = n.json()

    requests.post(f"{url}/standup/start", json={
        'token': owner['token'],
        'channel_id': channel_1['channel_id'],
        'length': 1
    })

    r = requests.post(f"{url}/standup/send", json={
        'token': random_user['token'],
        'channel_id': channel_1['channel_id'],
        'message': 'Test'
    })
    error_caught = r.json()
    assert error_caught['code'] == 400
