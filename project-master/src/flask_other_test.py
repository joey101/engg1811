'''

'''
import re
from subprocess import Popen, PIPE
import signal
from time import sleep
import pytest
import requests

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
    '''
    pytest fixture that registers the first user
    and creates the first channel
    '''
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
        'is_public' : False
    })

    channel_data = channel_1.json()
    return {
        'user_data' : user_data,
        'channel_data' : channel_data
    
    }

def test_users_all(url):
    '''
    Test that users_all works on the server
    '''
    user1_dict = {
        'u_id' : 1,
        'email' : 'example@example.com',
        'name_first' : 'Will',
        'name_last' : 'Smith',
        'handle_str' : 'willsmith',
        'profile_img_url' : ""
    }
    
    user2_dict = {
        'u_id' : 2,
        'email' : 'example2@example.com',
        'name_first' : 'Carlton',
        'name_last' : 'Banks',
        'handle_str' : 'carltonbanks',
        'profile_img_url' : ""     
    }

    user3_dict = {
        'u_id' : 3,
        'email' : 'example3@example.com',
        'name_first' : 'Homer',
        'name_last' : 'Simpson',
        'handle_str' : 'homersimpson',
        'profile_img_url' : ""     
    }

    user1 = requests.post(f"{url}/auth/register", json={
        'email' : 'example@example.com',
        'password' : 'verystrongpassword1234',
        'name_first' : 'Will',
        'name_last' : 'Smith'
    })

    user1_data = user1.json()

    requests.post(f"{url}/auth/register", json={
        'email' : 'example2@example.com',
        'password' : 'verystrongpassword1234',
        'name_first' : 'Carlton',
        'name_last' : 'Banks'
    })

    requests.post(f"{url}/auth/register", json={
        'email' : 'example3@example.com',
        'password' : 'verystrongpassword1234',
        'name_first' : 'Homer',
        'name_last' : 'Simpson'
    })

    # Test that the users registered return in in the users_all list
    r = requests.get(f"{url}/users/all?token={user1_data['token']}")
    all_users = r.json()

    assert all_users['users'][0] == user1_dict
    assert all_users['users'][1] == user2_dict
    assert all_users['users'][2] == user3_dict


def test_admin_userpermission_change_failure(url, registered_user_with_created_channel):
    '''
    Test that server returns an error code when user_id is not found
    '''
    owner_data = registered_user_with_created_channel['user_data']

    # Should return an error code since u_id 2 is invalid
    r = requests.post(f"{url}/admin/userpermission/change", json={
        'token' : owner_data['token'],
        'u_id' : 2,
        'permission_id' : 1
    })

    error_check = r.json()
    assert error_check['code'] == 400

def test_admin_userpermission_change_functionality(url, registered_user_with_created_channel):
    '''
    Test that the admin userpermission change functions correctly on the
    server
    '''
    owner_data = registered_user_with_created_channel['user_data']
    channel_data = registered_user_with_created_channel['channel_data']

    # Register a second user
    user = requests.post(f"{url}/auth/register", json={
        'email' : 'example2@example.com',
        'password' : 'verystrongpassword1234',
        'name_first' : 'Bart',
        'name_last' : 'Simpson'
    })

    user_data = user.json()

    # Invite the second user to the channel
    requests.post(f"{url}/channel/invite", json={
        'token' : owner_data['token'],
        'channel_id' : channel_data['channel_id'],
        'u_id' : user_data['u_id']
    })

    # Change the second user's permission to owner
    requests.post(f"{url}/admin/userpermission/change", json={
        'token' : owner_data['token'],
        'u_id' : user_data['u_id'],
        'permission_id' : 1
    })

    owner_dict = {'u_id': owner_data['u_id'], 'name_first': 'Will', 'name_last': 'Smith',
        'profile_img_url' : ""}
    user_dict = {'u_id': user_data['u_id'], 'name_first': 'Bart', 'name_last': 'Simpson',
        'profile_img_url' : ""}
    r = requests.get(f"{url}/channel/details?token={user_data['token']}&channel_id={channel_data['channel_id']}")
    details = r.json()

    # Check that that the user is part of owner_members
    assert details == {        
        'name': 'Test Channel',
        'owner_members': [owner_dict, user_dict],
        'all_members': [owner_dict, user_dict]
    }


def test_clear_for_users_functionality(url):
    '''
    This test is used to ensure that the data associated in the running of the
    flask server gets cleared once called.
    ''' 
    requests.post(f"{url}/auth/register", json={
        'email' : 'john.smith@gmail.com',
        'password' : 'verystrongpassword1234',
        'name_first' : 'John',
        'name_last' : 'Smith'
    })

    requests.post(f"{url}/auth/register", json={
        'email' : 'jon.snow@gmail.com',
        'password' : 'verystrongpassword4567',
        'name_first' : 'Jon',
        'name_last' : 'Snow'
    })

    requests.post(f"{url}/auth/register", json={
        'email' : 'james.bond007@gmail.com',
        'password' : 'CasinoRoyale2006',
        'name_first' : 'James',
        'name_last' : 'Bond'
    })

    requests.post(f"{url}/auth/register", json={
        'email' : 'darth.vader@gmail.com',
        'password' : 'DeathStar2020',
        'name_first' : 'Darth',
        'name_last' : 'Vader'
    })

    requests.post(f"{url}/auth/register", json={
        'email' : 'mike.myers@gmail.com',
        'password' : 'Halloween2020',
        'name_first' : 'Mike',
        'name_last' : 'Myers'
    })

    # Call the clear function
    requests.delete(f"{url}/clear")

    new_user = requests.post(f"{url}/auth/register", json={
        'email' : 'tommy.shelby@gmail.com',
        'password' : 'PeakyBlinders1234',
        'name_first' : 'Tommy',
        'name_last' : 'Shelby'
    })

    new_user_data = new_user.json()

    # Check that the new user is the only user in the users_all return
    r = requests.get(f"{url}/users/all?token={new_user_data['token']}")
    all_users = r.json()

    assert all_users == {
        'users' : [{
            'u_id': 1,
            'email': 'tommy.shelby@gmail.com',
            'name_first': 'Tommy',
            'name_last' : 'Shelby',
            'handle_str' : 'tommyshelby',
            'profile_img_url' : ""
        }]
    }
    

def test_search_functionality(url, registered_user_with_created_channel):
    '''
    Tests that the search function works on the server
    '''
    messages_test = [
        'test message 1',
        'test message 2',
        'test message 3'
    ]

    user = registered_user_with_created_channel['user_data']
    channel_1 = registered_user_with_created_channel['channel_data']

    # Send messages to the channel
    requests.post(f"{url}/message/send", json={
        'token': user['token'],
        'channel_id': channel_1['channel_id'],
        'message': 'test message 1'
    })
    requests.post(f"{url}/message/send", json={
        'token': user['token'],
        'channel_id': channel_1['channel_id'],
        'message': 'test message 2'
    })
    requests.post(f"{url}/message/send", json={
        'token': user['token'],
        'channel_id': channel_1['channel_id'],
        'message': 'test message 3'
    })
    requests.post(f"{url}/message/send", json={
        'token': user['token'],
        'channel_id': channel_1['channel_id'],
        'message': 'random message'
    })

    r = requests.get(f"{url}/search?token={user['token']}&query_str=test")
    query_messages = r.json()

    # Check that the correct mesasges are returned in the list
    # and that the length of the messages list is 3 for the
    # 3 messages with the query string 'test'
    i = 0
    for messages_found in query_messages['messages']:
        assert messages_found['message'] == messages_test[i]
        i += 1
    assert len(query_messages['messages']) == 3
