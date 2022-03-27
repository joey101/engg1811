'''
Contains the functions to test the other.py functions
'''
import pytest
import other
import channel
import channels
import message
import auth
import error



def test_other_search():
    '''
    Test that a user can search for messages in channels that he is a part of
    '''
    other.clear()
    messages_test = [
        'test message 1',
        'test message 2',
        'test message 3'
    ]
    user1 = auth.auth_register('example@example.com', 'abcd1234', 'Will', 'Smith')
    user2 = auth.auth_register('example2@example.com', 'abcd1234', 'John', 'Smith')
    channel_1 = channels.channels_create(user1['token'], 'channel_1', True)
    channels.channels_create(user1['token'], 'channel_2', True)
    channel.channel_join(user2['token'], channel_1['channel_id'])
    message.message_send(user2['token'], channel_1['channel_id'], 'test message 1')
    message.message_send(user2['token'], channel_1['channel_id'], 'test message 2')
    message.message_send(user2['token'], channel_1['channel_id'], 'test message 3')
    message.message_send(user2['token'], channel_1['channel_id'], 'this message should not be found')
    query_messages = other.search(user2['token'], 'test')

    i = 0
    for messages_found in query_messages['messages']:
        assert messages_found['message'] == messages_test[i]
        i += 1
    assert len(query_messages['messages']) == 3


def test_all_users_one_user():
    '''
    Test users_all works for one user
    '''
    other.clear()
    user = {
        'u_id' : 1,
        'email' : 'firstemail@gmail.com',
        'name_first' : 'firstname',
        'name_last' : 'lastname',
        'handle_str' : 'firstnamelastname',
        'profile_img_url' : ""
    }
    new_user = auth.auth_register('firstemail@gmail.com', 'password', 'firstname', 'lastname')
    all_users = other.users_all(new_user['token'])
    assert all_users['users'][0] == user


def test_all_users_multiple_users():
    '''
    Test that users_all works for multiple users
    '''
    other.clear()
    user_1 = {
        'u_id' : 1,
        'email' : 'firstemail@gmail.com',
        'name_first' : 'firstname',
        'name_last' : 'lastname',
        'handle_str' : 'firstnamelastname',
        'profile_img_url' : ""
    }
    
    user_2 = {
        'u_id' : 2,
        'email' : 'secondemail@gmail.com',
        'name_first' : 'Newfirstname',
        'name_last' : 'Newlastname',
        'handle_str' : 'newfirstnamenewlastn',
        'profile_img_url' : ""     
    }
    first_user = auth.auth_register('firstemail@gmail.com', 'password', 'firstname', 'lastname')
    auth.auth_register('secondemail@gmail.com', 'Newpassword', 'Newfirstname', 'Newlastname')
    all_users = other.users_all(first_user['token'])
    assert all_users['users'][0] == user_1
    assert all_users['users'][1] == user_2 


def test_admin_userpermission_change():
    '''
    Test that the function changes a users' permission
    '''
    other.clear()
    user_1 = auth.auth_register('example@example.com', 'abcd1234', 'Will', 'Smith')
    user_2 = auth.auth_register('example2@example.com', 'abcd1234', 'Carlton', 'Banks')
    channel_1 = channels.channels_create(user_1['token'], 'channel_1', True)
    channel.channel_join(user_2['token'], channel_1['channel_id'])


    other.admin_userpermission_change(user_1['token'], user_2['u_id'], 1)

    info = channel.channel_details(user_1['token'], channel_1['channel_id'])

    assert info['owner_members'][1]['u_id'] == user_2['u_id']



def test_admin_userpermission_change_demote():
    '''
    Test if the function can promote a user then demote him
    '''
    other.clear()
    user_1 = auth.auth_register('example@example.com', 'abcd1234', 'Will', 'Smith')
    user_2 = auth.auth_register('example2@example.com', 'abcd1234', 'Carlton', 'Banks')
    channel_1 = channels.channels_create(user_1['token'], 'channel_1', True)
    channels.channels_create(user_1['token'], 'channel_1', True)
    channel.channel_join(user_2['token'], channel_1['channel_id'])


    other.admin_userpermission_change(user_1['token'], user_2['u_id'], 1)
    other.admin_userpermission_change(user_1['token'], user_2['u_id'], 2)
    info = channel.channel_details(user_1['token'], channel_1['channel_id'])

    assert len(info['owner_members']) == 1


def test_admin_userpermission_change_invalid_uid():
    '''
    Exception test for invalid uid
    '''
    other.clear()
    user_1 = auth.auth_register('example@example.com', 'abcd1234', 'Will', 'Smith')
    auth.auth_register('example2@example.com', 'abcd1234', 'Carlton', 'Banks')
    with pytest.raises(error.InputError):
        other.admin_userpermission_change(user_1['token'], 4, 2)


def test_admin_userpermission_change_invalid_permission_id():
    '''
    Exception test for invalid permission id
    '''
    other.clear()
    user_1 = auth.auth_register('example@example.com', 'abcd1234', 'Will', 'Smith')
    user_2 = auth.auth_register('example2@example.com', 'abcd1234', 'Carlton', 'Banks') 
    with pytest.raises(error.InputError):
        other.admin_userpermission_change(user_1['token'], user_2['u_id'], 3)


def test_admin_userpermission_change_unauthorised():
    '''
    Exception test for an unauthorised user
    '''
    other.clear()
    user_1 = auth.auth_register('example@example.com', 'abcd1234', 'Will', 'Smith')
    user_2 = auth.auth_register('example2@example.com', 'abcd1234', 'Carlton', 'Banks') 
    with pytest.raises(error.AccessError):
        other.admin_userpermission_change(user_2['token'], user_1['u_id'], 3)

