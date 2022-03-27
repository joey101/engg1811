'''
This file will contain the user functions tests
'''

import pytest
import auth
import channels
import channel
import other
import user
import data
from error import InputError


def test_user_profile_1():
    '''
    A basic test that checks the user has been correctly registered and
    can be retrieved when user_profile is called.
    '''
    other.clear()

    test_user = auth.auth_register("john.smith@gmail.com", "Abcd1234","John", "Smith")
    test_user_result = user.user_profile(test_user["token"], test_user["u_id"])

    assert test_user_result == {
        'user' : {
            'u_id': test_user['u_id'],
            'email': "john.smith@gmail.com",
            'name_first': 'John',
            'name_last': "Smith",
            'handle_str': "johnsmith",
            'profile_img_url' : ""
        }
    }

def test_user_profile_not_valid_user():
    '''
    This test registers the user and when it goes to retrieve the user_profile it
    throws an error in the case that the u_id does not match.
    '''
    other.clear()

    test_user = auth.auth_register("james.bond007@gmail.com", "CasinoRoyale2006", "James", "Bond")

    with pytest.raises(InputError):
        user.user_profile(test_user['token'], 23)


def test_user_profile_setname_firstname():
    '''Test that will check if the first name is being updated correctly'''
    other.clear()

    test_user = auth.auth_register("user1@email.com", "testpass", "Milhouse", "Houten")
    user.user_profile_setname(test_user['token'], "Thrillhouse", "Houten")

    assert user.user_profile(test_user['token'], test_user['u_id']) == { 
        'user' : {
            'u_id': test_user['u_id'],
            'email': "user1@email.com",
            'name_first': "Thrillhouse",
            'name_last': "Houten",
            'handle_str': "milhousehouten",
            'profile_img_url' : ""
        }
    }


def test_user_profile_setname_second_user():
    '''Test that will check if the name is being updated correctly for second user'''
    other.clear()

    auth.auth_register("user1@email.com", "testpass", "Milhouse", "Houten")
    test_user = auth.auth_register("user2@email.com", "testpass", "Carlton", "Banks")
    user.user_profile_setname(test_user['token'], "Uncle", "Phil")

    assert user.user_profile(test_user['token'], test_user['u_id']) == {
        'user' : {
            'u_id': test_user['u_id'],
            'email': "user2@email.com",
            'name_first': "Uncle",
            'name_last': "Phil",
            'handle_str': "carltonbanks",
            'profile_img_url' : ""
        }
    }

def test_user_profile_setname_lastname():
    '''Test that will check if the last name is being updated correctly'''
    other.clear()

    test_user = auth.auth_register("user1@email.com", "testpass", "Milhouse", "Houten")
    user.user_profile_setname(test_user['token'], "Milhouse", "Tootin")

    assert user.user_profile(test_user['token'], test_user['u_id']) == {
        'user' : {
            'u_id': test_user['u_id'],
            'email': "user1@email.com",
            'name_first': "Milhouse",
            'name_last': "Tootin",
            'handle_str': "milhousehouten",
            'profile_img_url' : ""            
        }

    }

def test_user_profile_setname_firstname_and_lastname():
    '''Test that will check if the first name and the last name is being updated correctly'''
    other.clear()

    test_user = auth.auth_register("user1@email.com", "testpass", "Milhouse", "Houten")
    user.user_profile_setname(test_user['token'], "Thrillhouse", "Tootin")

    assert user.user_profile(test_user['token'], test_user['u_id']) == {
        'user' : {

            'u_id': test_user['u_id'],
            'email': "user1@email.com",
            'name_first': "Thrillhouse",
            'name_last': "Tootin",
            'handle_str': "milhousehouten",
            'profile_img_url' : ""
        }
    }

def test_user_profile_setname_updated_on_channel():
    '''
    Test that user's details get updated on the channel
    '''
    other.clear()

    owner = auth.auth_register("user1@email.com", "testpass", "First", "User")
    test_user = auth.auth_register("user2@email.com", "password", "Notedited", "Alsonotedited")

    channel_1 = channels.channels_create(owner['token'], "Test Channel", True)
    channels.channels_create(owner['token'], "Test Channel 2", True)
    

    channel_3 = channels.channels_create(test_user['token'], "Test Channel 2", True)
    channel.channel_join(test_user['token'], channel_1['channel_id'])
    channel.channel_join(owner['token'], channel_3['channel_id'])
    


    details = channel.channel_details(test_user['token'], channel_1['channel_id'])
    owner_dict = {
        'u_id' : owner['u_id'],
        'name_first' : "First",
        'name_last' : "User",
        'profile_img_url' : ""     
    }
    test_user_dict = {
        'u_id' : test_user['u_id'],
        'name_first' : "Notedited",
        'name_last' : "Alsonotedited",
        'profile_img_url' : ""
    }
    assert details == {
        'name' : 'Test Channel',
        'owner_members' : [owner_dict],
        'all_members' : [owner_dict, test_user_dict]
    }

    user.user_profile_setname(test_user['token'], "Newname", "Nowedited")
    user.user_profile_setname(owner['token'], "Firstedited", "Nowedited")

    details = channel.channel_details(test_user['token'], channel_1['channel_id'])
    owner_dict = {
        'u_id' : owner['u_id'],
        'name_first' : "Firstedited",
        'name_last' : "Nowedited",
        'profile_img_url' : ""    
    }
    test_user_dict = {
        'u_id' : test_user['u_id'],
        'name_first' : "Newname",
        'name_last' : "Nowedited",
        'profile_img_url' : ""
    }
    assert details == {
        'name' : 'Test Channel',
        'owner_members' : [owner_dict],
        'all_members' : [owner_dict, test_user_dict]
    }

def test_user_profile_setname_long_firstname():
    '''Test that checks if an exception is raised when first name is longer than 50 characters'''
    other.clear()
    long_name = "Thrillhouseisthenamesodontmesswiththisguybecauseyea"

    test_user = auth.auth_register("user1@email.com", "testpass", "Milhouse", "Houten")
    with pytest.raises(InputError):
        user.user_profile_setname(test_user['token'], long_name, "Tootin")


def test_user_profile_setname_short_firstname():
    '''Test that checks if an exception is raised when first name is shorter than 1 character'''
    other.clear()

    test_user = auth.auth_register("user1@email.com", "testpass", "Milhouse", "Houten")
    with pytest.raises(InputError):
        user.user_profile_setname(test_user['token'], "", "Tootin")


def test_user_profile_setname_long_lasttname():
    '''Test that checks if an exception is raised when last name is longer than 50 characters'''
    other.clear()
    long_name = "Tootinisthelastnamesodontmesswithitbecauseyeaitgoes"

    test_user = auth.auth_register("user1@email.com", "testpass", "Milhouse", "Houten")
    with pytest.raises(InputError):
        user.user_profile_setname(test_user['token'], "Thrillhouse", long_name)


def test_user_profile_setname_short_lasttname():
    '''Test that checks if an exception is raised when last name is shorter than 1 character'''
    other.clear()

    test_user = auth.auth_register("user1@email.com", "testpass", "Milhouse", "Houten")
    with pytest.raises(InputError):
        user.user_profile_setname(test_user['token'], "Thrillhouse", "")

def test_user_profile_setemail_functionality():
    '''Test that will check the setemail function works correctly'''
    other.clear()

    test_user = auth.auth_register("user1@email.com", "testpass", "Milhouse", "Houten")
    user.user_profile_setemail(test_user['token'], "milhouten@email.com")

    assert user.user_profile(test_user['token'], test_user['u_id']) == { 
        'user' : {
            'u_id': test_user['u_id'],
            'email': "milhouten@email.com",
            'name_first': "Milhouse",
            'name_last': "Houten",
            'handle_str': "milhousehouten",
            'profile_img_url' : ""
        }
    }

def test_user_profile_setemail_invalid_email():
    '''Test that checks an exception is raised when an invalid email is given'''
    other.clear()

    test_user = auth.auth_register("user1@email.com", "testpass", "Milhouse", "Houten")

    with pytest.raises(InputError):
        user.user_profile_setemail(test_user['token'], "milhouten.com")

def test_user_profile_setemail_used_email():
    '''Test that checks an exception is raised when the
    updated email is already in use by another user'''
    other.clear()

    auth.auth_register("milhouten@email.com", "testpass", "Milhouse", "Houten")
    second_test_user = auth.auth_register("user1@email.com", "testpass", "Bart", "Simpson")

    with pytest.raises(InputError):
        user.user_profile_setemail(second_test_user['token'], "milhouten@email.com")


def test_user_profile_sethandle_functionality():
    '''Test that checks that the sethandle function works correctly'''
    other.clear()

    test_user = auth.auth_register("milhouten@email.com", "testpass", "Milhouse", "Houten")
    user.user_profile_sethandle(test_user['token'], "thrillhousehouten")

    assert user.user_profile(test_user['token'], test_user['u_id']) == { 
        'user' : {
            'u_id': test_user['u_id'],
            'email': "milhouten@email.com",
            'name_first': "Milhouse",
            'name_last': "Houten",
            'handle_str': "thrillhousehouten",
            'profile_img_url' : ""
        }
    }

def test_user_profile_sethandle_short_handle():
    '''Test that checks if an exception is raised when the input handle is too short'''
    other.clear()

    test_user = auth.auth_register("milhouten@email.com", "testpass", "Milhouse", "Houten")

    with pytest.raises(InputError):
        user.user_profile_sethandle(test_user['token'], "mi")

def test_user_profile_sethandle_long_handle():
    '''Test that checks if an exception is raised when the input handle is too long'''
    other.clear()

    test_user = auth.auth_register("milhouten@email.com", "testpass", "Milhouse", "Houten")

    with pytest.raises(InputError):
        user.user_profile_sethandle(test_user['token'], "millllllllhouooooouse")


def test_user_profile_sethandle_used_handle():
    '''Test that checks if an exception is raised when the updated
    handle is already used by another user'''
    other.clear()

    auth.auth_register("milhouten@email.com", "testpass", "Milhouse", "Houten")
    second_test_user = auth.auth_register("user1@email.com", "testpass", "Bart", "Simpson")

    with pytest.raises(InputError):
        user.user_profile_sethandle(second_test_user['token'], "milhousehouten")

def test_user_profile_after_user_sets_profile_photo():
    '''
    test that the user's profile photo is displayed after the user sets their profile photo.
    WHITEBOX TEST:
        since we cannot call user_profile_setphoto as it needs the flask http tests, we instead
        manually set the data entry for a user's profile image url
    '''
    other.clear()
    test_user = auth.auth_register("john.smith@gmail.com", "Abcd1234","John", "Smith")
    
    data.users[0]['profile_img_url'] = 'test_url'

    test_user_result = user.user_profile(test_user["token"], test_user["u_id"])

    assert test_user_result == { 
        'user' : {
            'u_id': test_user['u_id'],
            'email': "john.smith@gmail.com",
            'name_first': 'John',
            'name_last': "Smith",
            'handle_str': "johnsmith",
            'profile_img_url' : "test_url"
        }
    }