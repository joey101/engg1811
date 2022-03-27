'''
All the routes needed for the server to function
'''
import sys
import os
from json import dumps
from flask import Flask, request
from flask_cors import CORS
from flask import send_file
from error import InputError
from PIL import Image, UnidentifiedImageError
import urllib.request
import urllib.error
import jwt
import message
import auth
import channel
import channels
import data
import user
import standup
import other

def defaultHandler(err):
    response = err.get_response()
    print('response', err, err.get_response())
    response.data = dumps({
        "code": err.code,
        "name": "System Error",
        "message": err.get_description(),
    })
    response.content_type = 'application/json'
    return response

APP = Flask(__name__)
CORS(APP)

APP.config['TRAP_HTTP_EXCEPTIONS'] = True
APP.register_error_handler(Exception, defaultHandler)


# Example
@APP.route("/echo", methods=['GET'])
def echo():
    data = request.args.get('data')
    if data == 'echo':
   	    raise InputError(description='Cannot echo "echo"')
    return dumps({
        'data': data
    })
    
@APP.route("/admin/userpermission/change", methods=['POST'])
def admin_user_permission_change():
    payload = request.get_json()
    token = payload['token']
    u_id = payload['u_id']
    permission_id = payload['permission_id']
    other.admin_userpermission_change(token, u_id, permission_id)
    return dumps({})


@APP.route("/users/all", methods=['GET'])
def users_all():
    token = request.args.get('token')
    dump = other.users_all(token)
    return dumps(dump)


@APP.route("/auth/register", methods=['POST'])
def auth_register():
    '''
    Registers a user given an email, password and name
    '''
    data = request.get_json()
    email = data['email']
    password = data['password']
    name_first = data['name_first']
    name_last = data['name_last']
    user = auth.auth_register(email, password, name_first, name_last)
    return dumps(user)


@APP.route("/auth/logout", methods=['POST'])
def auth_logout():
    '''
    Route for logging out a user
    '''
    payload = request.get_json()
    token = payload['token']
    dump = auth.auth_logout(token)
    return dumps(dump)

@APP.route("/auth/login", methods=['POST'])
def auth_login():
    '''
    Route that will login a user
    '''
    payload = request.get_json()
    email = payload['email']
    password = payload['password']
    dump = auth.auth_login(email, password)
    return dumps(dump)


@APP.route("/auth/passwordreset/request", methods=['POST'])
def auth_passwordreset_request():
    '''
    Route that sends a 16 character alphanumeric reset code 
    to a user who is requesting the password reset.
    '''
    payload = request.get_json()
    email = payload['email'] 
    auth.auth_passwordreset_request(email)
    return dumps({})

@APP.route("/auth/passwordreset/reset", methods=['POST'])
def auth_passwordreset_reset():
    '''
    Route that takes in the reset_code and new_password, 
    checks both parameters are valid and then resets the password for the user.
    '''
    payload = request.get_json()
    reset_code = payload['reset_code']
    new_password = payload['new_password']
    auth.auth_passwordreset_reset(reset_code, new_password) 
    return dumps({})

@APP.route("/user/profile", methods=['GET'])
def user_profile():
    '''
    Takes a token and the user id from URL and will return a json
    string with user's profile info
    '''
    token = request.args.get('token')
    u_id = int(request.args.get('u_id'))

    user_info = user.user_profile(token, u_id)
    return dumps(user_info)

@APP.route("/user/profile/setname", methods=['PUT'])
def user_profile_setname():
    '''
    Takes a token and a name from the user and updates the users name
    '''
    data = request.get_json()
    token = data['token']
    name_first = data['name_first']
    name_last = data['name_last']
    user.user_profile_setname(token, name_first, name_last)
    return dumps({})

@APP.route("/user/profile/setemail", methods=['PUT'])
def user_profile_setemail():
    '''
    Takes a token and an email and updates the users email
    '''
    data = request.get_json()
    token = data['token']
    email = data['email']
    user.user_profile_setemail(token, email)
    return dumps({})

@APP.route('/user/profile/sethandle', methods=['PUT'])
def user_profile_sethandle():
    '''
    Route that sets the new handle of the user
    '''
    data = request.get_json()
    token = data['token']
    handle_str = data['handle_str']
    user.user_profile_sethandle(token, handle_str)
    payload = request.get_json()
    email = payload['email']
    password = payload['password']
    name_first = payload['name_first']
    name_last = payload['name_last']
    dump = auth.auth_register(email, password, name_first, name_last)
    return dumps(dump)

@APP.route("/channels/create", methods=['POST'])
def channels_create():
    '''
    Route that creates a channel
    '''
    payload = request.get_json()
    token = payload['token']
    name = payload['name']
    is_public = payload['is_public']

    dump = channels.channels_create(token, name, is_public)
    return dumps(dump)

@APP.route("/channels/list", methods=['GET'])
def channels_list():
    '''
    Route that lists the channels a user is a part of
    '''
    token = request.args.get('token')
    dump = channels.channels_list(token)
    return dumps(dump)

@APP.route("/channels/listall", methods=['GET'])
def channels_listall():
    '''
    Route that lists all created channels
    '''
    token = request.args.get('token')
    dump = channels.channels_listall(token)
    return dumps(dump)

@APP.route("/channel/invite", methods=['POST'])
def channel_invite():
    '''
    Route that invites a user to a channel
    '''
    payload = request.get_json()
    token = payload['token']
    channel_id = payload['channel_id']
    u_id = payload['u_id']
    channel.channel_invite(token, channel_id, u_id)
    return dumps({})

@APP.route("/channel/join", methods=['POST'])
def channel_join():
    '''
    Route that allows a user join a channel
    '''
    payload = request.get_json()
    token = payload['token']
    channel_id = payload['channel_id']
    channel.channel_join(token, channel_id)
    return dumps({})

@APP.route("/channel/leave", methods=['POST'])
def channel_leave():
    '''
    Route that allows a user to leave a channel
    '''
    payload = request.get_json()
    token = payload['token']
    channel_id = payload['channel_id']
    channel.channel_leave(token, channel_id)
    return dumps({})    


@APP.route("/channel/details", methods=['GET'])
def channel_details():
    '''
    Route that shows the details of a given channel
    '''
    token = request.args.get('token')
    channel_id = request.args.get('channel_id')
    dump = channel.channel_details(token, channel_id)
    return dumps(dump)

@APP.route("/channel/messages", methods=['GET'])
def channel_messages():
    '''
    Route that returns up to 50 messages from a specified channel from
    start to start + 50
    '''
    token = request.args.get('token')
    channel_id = request.args.get('channel_id')
    start = request.args.get('start')
    dump = channel.channel_messages(token, channel_id, start)
    return dumps(dump)

@APP.route("/channel/addowner", methods=['POST'])
def channel_addowner():
    '''
    Route that adds another user as an owner of the channel
    '''
    payload = request.get_json()
    token = payload['token']
    channel_id = payload['channel_id']
    u_id = payload['u_id']
    channel.channel_addowner(token, channel_id, u_id)
    return dumps({})

@APP.route("/channel/removeowner", methods=['POST'])
def channel_removeowner():
    '''
    Route that removes a user as an owner from a channel
    '''
    payload = request.get_json()
    token = payload['token']
    channel_id = payload['channel_id']
    u_id = payload['u_id']
    channel.channel_removeowner(token, channel_id, u_id)
    return dumps({})

@APP.route("/message/send", methods=['POST'])
def message_send():
    '''
    Route that sends a message to a specified channel
    '''
    payload = request.get_json()
    token = payload['token']
    channel_id = payload['channel_id']
    message_sent = payload['message']
    message_id = message.message_send(token, channel_id, message_sent)
    return dumps(message_id)

@APP.route("/message/remove", methods=['DELETE'])
def message_remove():
    '''
    Route that removes a message from a specified channel
    '''
    payload = request.get_json()
    token = payload['token']
    message_id = payload['message_id']

    message_id = message.message_remove(token, message_id)
    return dumps({})

@APP.route("/message/edit", methods=['PUT'])
def message_edit():
    '''
    Route that edits a message specified by the message ID
    '''
    payload = request.get_json()
    token = payload['token']
    message_id = payload['message_id']
    message_edited = payload['message']
    message_id = message.message_edit(token, message_id, message_edited)
    return dumps({})

@APP.route("/message/react", methods=['POST'])
def message_react():
    '''
    Route that reacts to the specified message
    '''
    payload = request.get_json()
    token = payload['token']
    message_id = payload['message_id']
    react_id = payload['react_id']
    message.message_react(token, message_id, react_id)
    return dumps({})


@APP.route("/message/unreact", methods=['POST'])
def message_unreact():
    '''
    Route that unreacts to the specified message
    '''
    payload = request.get_json()
    token = payload['token']
    message_id = payload['message_id']
    react_id = payload['react_id']
    message.message_unreact(token, message_id, react_id)
    return dumps({})

@APP.route("/message/pin", methods=['POST'])
def message_pin():
    '''
    Route that pins the specified message
    '''
    payload = request.get_json()
    token = payload['token']
    message_id = payload['message_id']
    message.message_pin(token, message_id)
    return dumps({})

@APP.route("/message/unpin", methods=['POST'])
def message_unpin():
    '''
    Route that pins the specified message
    '''
    payload = request.get_json()
    token = payload['token']
    message_id = payload['message_id']
    message.message_unpin(token, message_id)
    return dumps({})

@APP.route("/message/sendlater", methods=['POST'])
def message_sendlater():
    '''
    Route that sends a message after a specified amount of time
    '''
    payload = request.get_json()
    token = payload['token']
    channel_id = int(payload['channel_id'])
    message_to_send = payload['message']
    time_sent = payload['time_sent']
    message_sent = message.message_sendlater(token, channel_id, message_to_send, time_sent)
    return dumps(message_sent)


@APP.route("/search", methods=['GET'])
def search():
    '''
    Route that searches for messages with the given query string
    '''
    token = request.args.get('token')
    query_str = request.args.get('query_str')
    messages = other.search(token, query_str)
    
    return dumps(messages)

@APP.route("/clear", methods=['DELETE'])
def clear():
    '''
    Route that clears all data that exists on the server
    '''
    other.clear()

@APP.route("/user/profile/uploadphoto", methods=['POST'])
def user_profile_uploadphoto():
    '''
    Checks the link given by the user if it is a valid img url,
    and then calls the user.py uploadphoto function to crop the photo
    and set the img url to the user's profile_img_url
    '''
    payload = request.get_json()
    token = payload['token']
    img_url = payload['img_url']
    decoded_jwt = jwt.decode(token.encode('utf-8'), data.secret, algorithms=['HS256'])
    decoded_token = decoded_jwt['token']
    user_data = user.token_find_user(decoded_token)

    server_url = request.url_root

    # Check where the server has been started from (inside or outside src)
    # and set the directory to save the images
    if '/src' in os.getcwd():
        if not os.path.exists(os.path.dirname(f"img/{user_data['u_id']}")):
            os.makedirs(os.path.dirname(f"img/{user_data['u_id']}"))

        saved_image_path = f"img/{user_data['u_id']}"

    else:
        if not os.path.exists(os.path.dirname(f"src/img/{user_data['u_id']}")):
            os.makedirs(os.path.dirname(f"src/img/{user_data['u_id']}"))

        saved_image_path = f"src/img/{user_data['u_id']}"

    # Check if the link given for the image is valid
    try:
        urllib.request.urlretrieve(img_url, saved_image_path)

        try:
            Image.open(saved_image_path)
        except UnidentifiedImageError:
            raise InputError("Invalid image link")
        
        # Send link into the user function to crop and set for the user's profile_img_url
        x_start = int(payload['x_start'])
        y_start = int(payload['y_start'])
        x_end = int(payload['x_end'])
        y_end = int(payload['y_end'])
        url_to_send = f"{server_url}img/{user_data['u_id']}"
        user.user_profile_uploadphoto(token, url_to_send, x_start, y_start, x_end, y_end) 
        return dumps({})

    except (urllib.error.URLError, ValueError):
        raise InputError("Invalid image link")


@APP.route('/img/<filename>')
def display_picture(filename):
    '''
    route to get the saved profile images
    '''
    path = os.getcwd()
    if '/src' in os.getcwd():
        send_path = path + f"/img/{filename}"
        return send_file(send_path, mimetype='image/jpeg')
    else:
        send_path = path + f"/src/img/{filename}"
        return send_file(send_path, mimetype='image/jpeg')

@APP.route("/standup/start", methods=['POST'])
def standup_start():
    '''
    Endpoint that starts a standup in a given channel for a
    certain amount of time
    '''
    payload = request.get_json()
    token = payload['token']
    channel_id = payload['channel_id']
    length = payload['length']
    start_standup = standup.standup_start(token, channel_id, length)
    return dumps(start_standup)

@APP.route("/standup/active", methods=['GET'])
def standup_active():
    '''
    Endpoint that checks if a standup is active
    and how long it is active for
    '''
    token = request.args.get('token')
    channel_id = request.args.get('channel_id')
    standup_status = standup.standup_active(token, channel_id)
    return dumps(standup_status)

@APP.route("/standup/send", methods=['POST'])
def standup_send():
    '''
    Endpoint that sends a message in a standup if
    a standup is active
    '''
    payload = request.get_json()
    token = payload['token']
    channel_id = payload['channel_id']
    message = payload['message']
    send_standup_message = standup.standup_send(token, channel_id, message)
    return dumps(send_standup_message)

if __name__ == "__main__":
    #APP.debug = True
    APP.run(port=0) # Do not edit this po
