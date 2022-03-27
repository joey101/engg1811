import channels
import channel
import auth
import pytest
import error
import other

#test that channels can be created
def test_channels_create_1():
    other.clear()
    user1 = auth.auth_register("example@example.com", "abcd1234", "John", "Smith")
    assert channels.channels_create(user1['token'], "Test Channel", True) == {'channel_id' : 1}

#test multiple channels can be created
def test_create_multiple_channels():
    other.clear()
    user1 = auth.auth_register("example@example.com", "abcd1234", "John", "Smith")
    assert channels.channels_create(user1['token'], "Test Channel", True) == {'channel_id' : 1}
    assert channels.channels_create(user1['token'], "Test Channel 2", True) == {'channel_id' : 2}
    assert channels.channels_create(user1['token'], "Test Channel 3", True) == {'channel_id' : 3}
    


#test that one channel can be listed
def test_channels_list_1():
    other.clear()
    user1 = auth.auth_register("example@example.com", "abcd1234", "John", "Smith")
    channels.channels_create(user1['token'], "Test Channel", True)
    assert channels.channels_list(user1['token']) == {
        'channels' : [
            {
                'channel_id' : 1,
                'name' : "Test Channel"
            }
        ]
    }


#test multiple channels can be listed
def test_list_multiple_channels():
    other.clear()
    user1 = auth.auth_register("example@example.com", "abcd1234", "John", "Smith")
    channels.channels_create(user1['token'], "Test Channel", True)
    channels.channels_create(user1['token'], "Test Channel 2", True)
    channels.channels_create(user1['token'], "Test Channel 3", True)
    assert channels.channels_list(user1['token']) == {
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

# test channels_list to make sure that private channels are not listed for 
# users that arent authorised
def test_list_channels_private():
    other.clear()
    user1 = auth.auth_register("example@example.com", "abcd1234", "John", "Smith")
    user2 = auth.auth_register("example2@example.com", "abcd1234", "John", "Smith")
    channel1 = channels.channels_create(user1['token'], "Test Channel", True)
    channel2 = channels.channels_create(user1['token'], "Test Channel 2", True)
    channel3 = channels.channels_create(user1['token'], "Test Channel 3", True)
    channels.channels_create(user1['token'], "Private Channel", False)
    channel.channel_join(user2['token'], channel1['channel_id'])
    channel.channel_join(user2['token'], channel2['channel_id'])
    channel.channel_join(user2['token'], channel3['channel_id'])
    assert channels.channels_list(user1['token']) == {
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
    assert channels.channels_list(user2['token']) == {
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


#test channels_listall lists all channels
def test_list_all_channels():
    other.clear()
    user1 = auth.auth_register("example@example.com", "abcd1234", "John", "Smith")
    channels.channels_create(user1['token'], "Test Channel", True)
    channels.channels_create(user1['token'], "Test Channel 2", True)
    channels.channels_create(user1['token'], "Test Channel 3", True)
    channels.channels_create(user1['token'], "Private Channel", False)
    assert channels.channels_listall(user1['token']) == {
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


#test for a channel name longer than 20 characters to raise InputError
def test_input_error_exception():
    other.clear()
    user1 = auth.auth_register("example@example.com", "abcd1234", "John", "Smith")
    with pytest.raises(error.InputError):
        channels.channels_create(user1['token'], "Very long name for a channel", True)