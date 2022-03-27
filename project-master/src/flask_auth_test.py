'''
This file contains all the tests to make sure that the
auth functions work through the server routes
'''
import re
from subprocess import Popen, PIPE
import signal
from time import sleep
import pytest
import requests
import data


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
        'email': 'example@example.com',
        'password': 'verystrongpassword1234',
        'name_first': 'Will',
        'name_last': 'Smith'
    })

    return user.json()

def test_register_valid(url, registered_user):
    '''
    Test that auth_register functions on the server
    '''
    
    user_data = registered_user

    # Check the user has registered by getting their profile information
    user_details = requests.get(f"{url}/user/profile?token={user_data['token']}&u_id={user_data['u_id']}")

    user_profile = user_details.json()

    assert user_profile['user']['u_id'] == user_data['u_id']
    assert user_profile['user']['email'] == "example@example.com"
    assert user_profile['user']['name_first'] == 'Will'
    assert user_profile['user']['name_last'] == 'Smith'

def test_auth_register_failure(url):
    '''
    Test that the server returns an error code when auth_register raises an error
    '''

    # invalid email, error code 400 should be returned
    r = requests.post(f"{url}/auth/register", json={
        'email': 'example.com',
        'password': 'verystrongpassword1234',
        'name_first': 'Will',
        'name_last': 'Smith'
    })

    error_check = r.json()
    assert error_check['code'] == 400


def test_logout_valid(url, registered_user):
    '''
    Test that auth_logout functions on the server
    '''

    user_data = registered_user
    logout = requests.post(f"{url}/auth/logout", json={
        'token': user_data['token']
    })

    # Check if the user can logout
    logout_check = logout.json()
    assert logout_check['is_success'] is True


def test_login_valid(url, registered_user):
    '''
    Test that auth login functions on the server
    '''

    user_data = registered_user

    logout = requests.post(f"{url}/auth/logout", json={
        'token': user_data['token']
    })
    
    # Check the user has logged out
    logout_check = logout.json()
    assert logout_check['is_success'] is True

    # Check if the user can log back in
    login = requests.post(f"{url}/auth/login", json={
        'email': 'example@example.com',
        'password': 'verystrongpassword1234'
    })

    login_check = login.json()

    assert login_check['u_id'] == user_data['u_id']
    assert login_check['token'] is not None

def test_auth_login_failure(url, registered_user):
    '''
    Test that auth login returns an error code when auth_login raises an error
    '''

    user_data = registered_user

    logout = requests.post(f"{url}/auth/logout", json={
        'token': user_data['token']
    })
    
    # Checks if the user has successfully logged out
    logout_check = logout.json()
    assert logout_check['is_success'] is True

    # Error code 400 should be returned for incorrect password
    login = requests.post(f"{url}/auth/login", json={
        'email': 'example@example.com',
        'password': 'thewrongpassword'
    })

    error_check = login.json()

    assert error_check['code'] == 400


def test_auth_passwordreset_reset_failure_reset_code(url, registered_user):
    '''
    Test that the server returns an error code when reset_code is not a valid code.
    '''
    registered_user
    
    requests.post(f"{url}/auth/passwordreset/request", json={
        'email': "example@example.com"
    })

    # Using invalid reset code         
    r = requests.post(f"{url}/auth/passwordreset/reset", json={
        'reset_code': '???????',
        'new_password': 'verystrongpassword1234'
    })

    error_check = r.json()
    assert error_check['code'] == 400

def test_auth_passwordreset_reset_failure_invalid_password(url, registered_user):
    '''
    This is test to ensure that an error code is returned when new_password
    is invalid due to it not meeting the required specification.
    '''
    user_data = registered_user
    
    requests.post(f"{url}/auth/passwordreset/request", json={
        'email': "example@example.com"
    })
    
    code = ''
    for reset_code in data.reset_codes:
        if user_data['u_id'] == reset_code['u_id']:
            code = reset_code['reset_code']

    user_data = registered_user
    r = requests.post(f"{url}/auth/passwordreset/reset", json={
        'reset_code': code,
        'new_password': 'pword'
    })

    error_check = r.json()
    assert error_check['code'] == 400

# Success case might be an issue --> white box method might be the way.
def test_auth_passwordreset_reset_success_case(url, registered_user):
    '''
    This is a success case, that requests for a password reset, allows the user to 
    set the new password, logs out the user and logs them back in to ensure the new password
    has been correctly stored.
    '''
    user_data = registered_user
    
    requests.post(f"{url}/auth/passwordreset/request", json={
        'email': "example@example.com"
    })

    code = ''
    for reset_code in data.reset_codes:
        if user_data['u_id'] == reset_code['u_id']:
            code = reset_code['reset_code']

    requests.post(f"{url}/auth/passwordreset/reset", json={
        'reset_code': code,
        'new_password': 'verystrongpassword1234'
    })

    logout = requests.post(f"{url}/auth/logout", json={
        'token': user_data['token']
    })
    
    # Check the user has logged out
    logout_check = logout.json()
    assert logout_check['is_success'] is True

    # Check if the user can log back in
    login = requests.post(f"{url}/auth/login", json={
        'email': "example@example.com",
        'password': 'verystrongpassword1234'
    })

    login_check = login.json()

    assert login_check['u_id'] == user_data['u_id']
    assert login_check['token'] is not None