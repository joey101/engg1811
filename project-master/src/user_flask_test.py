'''
File that tests that all the https endpoint routes
work correctly for user functions.
'''
import re
import signal
from subprocess import Popen, PIPE
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
def registered_user(url):
    '''
    A basic fixture that registers a user, just to reduce lines
    and make the tests easier to understand.
    '''
    r = requests.post(f"{url}/auth/register", json={
        'email': "john.smith@gmail.com",
        'password': "abcd1081$#",
        'name_first': "John",
        'name_last': "Smith",
    })
    user_data = r.json()

    return user_data  


def test_user_profile_functionality(url, registered_user):
    '''
    register a user using the post method which uses the auth_register function 
    and check their profile is returned using user_profile.
    '''
    test_user = registered_user
    assert test_user['u_id'] == 1

    r = requests.get(f"{url}/user/profile?token={test_user['token']}&u_id={test_user['u_id']}")
    payload = r.json()
    assert payload == { 
        'user' :{
            'u_id': test_user['u_id'],
            'email': 'john.smith@gmail.com',
            'name_first': 'John',
            'name_last': 'Smith',
            'handle_str': 'johnsmith',
            'profile_img_url' : ""
        }

    }

def test_user_profile_set_name_functionality(url, registered_user):
    '''
    This is a test to see that the name_first and name_last for a given user
    gets changed using the user_profile_setname function.
    '''
    user_data = registered_user

    requests.put(f"{url}/user/profile/setname", json={
        'token': user_data['token'],
        'name_first': 'Jon',
        'name_last': 'Snow'
    })

    r = requests.get(f"{url}/user/profile?token={user_data['token']}&u_id={user_data['u_id']}")
    payload = r.json()

    assert payload == {
        'user' : {
            'u_id': user_data['u_id'],
            'email': 'john.smith@gmail.com',
            'name_first': 'Jon',
            'name_last': 'Snow',
            'handle_str': 'johnsmith',
            'profile_img_url' : ""
        }

    }


def test_user_profile_set_name_functionality_fail_case(url, registered_user):
    '''
    This is a test case to make sure an error is raised as a result of the name_first parameter not meeting the specification. 
    '''
    user_data = registered_user

    r = requests.put(f"{url}/user/profile/setname", json={
        'token': user_data['token'],
        'name_first': '', 
        'name_last': 'Smith'
        })

    error_caught = r.json()
    assert error_caught['code'] == 400


def test_user_profile_set_email_functionality(url, registered_user):
    '''
    This is a test to see that the user_profile_setemail function works as required.
    '''
    user_data = registered_user

    requests.put(f"{url}/user/profile/setemail", json={
        'token': user_data['token'],
        'email': 'john.smith2@gmail.com'
    })

    r = requests.get(f"{url}/user/profile?token={user_data['token']}&u_id={user_data['u_id']}")
    payload = r.json()

    assert payload == {
        'user' : {
            'u_id': user_data['u_id'],
            'email': 'john.smith2@gmail.com',
            'name_first': 'John',
            'name_last': 'Smith',
            'handle_str': 'johnsmith',
            'profile_img_url' : ""
        }

    }

def test_user_profile_set_email_functionality_failure_case_1(url, registered_user):
    '''
    This is a test to see that the user_profile_setemail function works as required.
    This will be tested by providing an invalid email address change and should raise an error.
    '''
    user_data = registered_user

    r = requests.put(f"{url}/user/profile/setemail", json={
        'token': user_data['token'],
        'email': 'john.smith2.com'
    })

    error_caught = r.json()
    assert error_caught['code'] == 400


def test_user_profile_set_email_functionality_failure_case_2(url, registered_user):
    '''
    This is a test to see that the user_profile_setemail function works as required.
    This will be tested by providing a email address that has already been used and should raise an error.
    '''
    user2 = requests.post(f"{url}/auth/register", json={
        'email' : 'john.smith2@gmail.com',
        'password' : 'abcd1081$#',
        'name_first' : 'John',
        'name_last' : 'Smith'
    })

    user_data2 = user2.json()

    r = requests.put(f"{url}/user/profile/setemail", json={
        'token': user_data2['token'],
        'email': 'john.smith@gmail.com'
    })

    error_caught = r.json()
    assert error_caught['code'] == 400

def test_user_profile_set_handle_functionality(url, registered_user):
    '''
    This is a test to ensure that the set_handle works as required and correctly sets the new handle requested by the user.
    '''
    user_data = registered_user

    r = requests.put(f"{url}/user/profile/sethandle", json={
        'token': user_data['token'],
        'handle_str': 'smithjohn'
    })

    r = requests.get(f"{url}/user/profile?token={user_data['token']}&u_id={user_data['u_id']}")
    payload = r.json()
    
    assert payload == {
        'user' : {
            'u_id': user_data['u_id'],
            'email': 'john.smith@gmail.com',
            'name_first': 'John',
            'name_last': 'Smith',
            'handle_str': 'smithjohn',
            'profile_img_url' : ""
        }

    }

def test_user_profile_set_handle_functionality_failure_case_1(url, registered_user):
    '''
    This is a test to check that the set_handle function fails when provided a handle below 3 characters.
    '''
    user_data = registered_user

    r = requests.put(f"{url}/user/profile/sethandle", json={
        'token': user_data['token'],
        'handle_str': 'js'
    })

    error_caught = r.json()
    assert error_caught['code'] == 400


def test_user_profile_set_handle_functionality_failure_case_2(url, registered_user):
    '''
    This is a test to check the input error - handle is already used by another user.
    '''
    fake_user = requests.post(f"{url}/auth/register", json={
        'email' : 'john.smith2@gmail.com',
        'password' : 'abcd1081$#',
        'name_first' : 'John',
        'name_last' : 'Smith'
    })

    fake_user_data = fake_user.json()

    r = requests.put(f"{url}/user/profile/sethandle", json={
        'token': fake_user_data['token'],
        'handle_str': 'johnsmith'
    })

    error_caught = r.json()
    assert error_caught['code'] == 400


def test_user_profile_uploadphoto(url, registered_user):
    '''
    test that a user can set their profile photo with given img_url on the flask server
    '''
    user_data = registered_user
    img_url = "https://i.ytimg.com/vi/CPhihTANyPo/maxresdefault.jpg"
    
    requests.post(f"{url}/user/profile/uploadphoto", json={
        'token': user_data['token'],
        'img_url' : img_url,
        'x_start' : 300,
        'y_start' : 0,
        'x_end' : 920,
        'y_end' : 600
    })

    #user.user_profile_uploadphoto(user_data['token'], img_url, 300, 0, 920, 600)
    r = requests.get(f"{url}/user/profile?token={user_data['token']}&u_id={user_data['u_id']}")
    profile_data = r.json() 

    assert profile_data['user']['profile_img_url'] == f"{url}img/{profile_data['user']['u_id']}.jpg"

def test_user_profile_uploadphoto_two_users(url, registered_user):
    '''
    test that multiple users can set their profile photos with given img_url on the flask server
    '''
    user_data = registered_user
    img_url = "https://i.ytimg.com/vi/CPhihTANyPo/maxresdefault.jpg"
    
    requests.post(f"{url}/user/profile/uploadphoto", json={
        'token': user_data['token'],
        'img_url' : img_url,
        'x_start' : 300,
        'y_start' : 0,
        'x_end' : 920,
        'y_end' : 600
    })

    user2 = requests.post(f"{url}/auth/register", json={
        'email' : 'john.smith2@gmail.com',
        'password' : 'abcd1081$#',
        'name_first' : 'John',
        'name_last' : 'Smith'
    })

    user2_data = user2.json()

    requests.post(f"{url}/user/profile/uploadphoto", json={
        'token': user2_data['token'],
        'img_url' : img_url,
        'x_start' : 300,
        'y_start' : 0,
        'x_end' : 920,
        'y_end' : 600
    })

    #user.user_profile_uploadphoto(user_data['token'], img_url, 300, 0, 920, 600)
    r = requests.get(f"{url}/user/profile?token={user_data['token']}&u_id={user_data['u_id']}")
    profile_data = r.json() 

    assert profile_data['user']['profile_img_url'] == f"{url}img/{profile_data['user']['u_id']}.jpg"

    r = requests.get(f"{url}/user/profile?token={user2_data['token']}&u_id={user_data['u_id']}")
    profile2_data = r.json()

    assert profile2_data['user']['profile_img_url'] == f"{url}img/{profile_data['user']['u_id']}.jpg"


def test_user_profile_uploadphoto_invalid_url(url, registered_user):
    '''
    test that an error code is raised when an invalid URL is given
    '''
    user_data = registered_user
    img_url = "not_a_url"
    
    r = requests.post(f"{url}/user/profile/uploadphoto", json={
        'token': user_data['token'],
        'img_url' : img_url,
        'x_start' : 300,
        'y_start' : 0,
        'x_end' : 920,
        'y_end' : 600
    })

    error_check = r.json() 

    assert error_check['code'] == 400


def test_user_profile_uploadphoto_invalid_url_2(url, registered_user):
    '''
    test that an error code is raised when an invalid URL is given
    '''
    user_data = registered_user
    img_url = "http://www.google.com"
    
    r = requests.post(f"{url}/user/profile/uploadphoto", json={
        'token': user_data['token'],
        'img_url' : img_url,
        'x_start' : 300,
        'y_start' : 0,
        'x_end' : 920,
        'y_end' : 600
    })

    error_check = r.json() 

    assert error_check['code'] == 400

def test_user_profile_uploadphoto_not_JPEG(url, registered_user):
    '''
    test that the server returns an error code when an image that is not a jpeg is given
    '''
    user_data = registered_user
    img_url = "https://www.google.com/images/branding/googlelogo/1x/googlelogo_color_272x92dp.png"
    
    r = requests.post(f"{url}/user/profile/uploadphoto", json={
        'token': user_data['token'],
        'img_url' : img_url,
        'x_start' : 0,
        'y_start' : 0,
        'x_end' : 200,
        'y_end' : 90
    })

    error_check = r.json() 

    assert error_check['code'] == 400


def test_user_profile_uploadphoto_invalid_x_start(url, registered_user):
    '''
    test that an error code is raised when invalid x_start is given
    '''
    user_data = registered_user
    img_url = "https://i.ytimg.com/vi/CPhihTANyPo/maxresdefault.jpg"
    
    r = requests.post(f"{url}/user/profile/uploadphoto", json={
        'token': user_data['token'],
        'img_url' : img_url,
        'x_start' : 99999,
        'y_start' : 0,
        'x_end' : 920,
        'y_end' : 600
    })

    error_check = r.json() 

    assert error_check['code'] == 400


def test_user_profile_uploadphoto_invalid_y_start(url, registered_user):
    '''
    test that an error code is raised when invalid y_start is given
    '''
    user_data = registered_user
    img_url = "https://i.ytimg.com/vi/CPhihTANyPo/maxresdefault.jpg"
    
    r = requests.post(f"{url}/user/profile/uploadphoto", json={
        'token': user_data['token'],
        'img_url' : img_url,
        'x_start' : 300,
        'y_start' : 99999,
        'x_end' : 920,
        'y_end' : 600
    })

    error_check = r.json() 

    assert error_check['code'] == 400


def test_user_profile_uploadphoto_invalid_x_end(url, registered_user):
    '''
    test that an error code is raised when invalid x_end is given
    '''
    user_data = registered_user
    img_url = "https://i.ytimg.com/vi/CPhihTANyPo/maxresdefault.jpg"
    
    r = requests.post(f"{url}/user/profile/uploadphoto", json={
        'token': user_data['token'],
        'img_url' : img_url,
        'x_start' : 300,
        'y_start' : 0,
        'x_end' : 99999,
        'y_end' : 600
    })

    error_check = r.json() 

    assert error_check['code'] == 400


def test_user_profile_uploadphoto_invalid_y_end(url, registered_user):
    '''
    test that an error code is raised when invalid y_end is given
    '''
    user_data = registered_user
    img_url = "https://i.ytimg.com/vi/CPhihTANyPo/maxresdefault.jpg"
    
    r = requests.post(f"{url}/user/profile/uploadphoto", json={
        'token': user_data['token'],
        'img_url' : img_url,
        'x_start' : 300,
        'y_start' : 0,
        'x_end' : 920,
        'y_end' : 99999
    })

    error_check = r.json() 

    assert error_check['code'] == 400
