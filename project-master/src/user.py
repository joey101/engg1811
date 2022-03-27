'''
All functions that handle the users data and update it
'''
import jwt
import os
import data
import auth_helper_functions as helper
import error
from PIL import Image
import urllib.request
import urllib.error

def token_find_user(token):
    '''Given a user's token, returns the user's info dictionary'''
    required_user = {}
    for user in data.users:
        if user['token'] == token:
            required_user = user

    return required_user

def update_user_details_in_channels(token):
    '''
    Updates the user details in all channels a user is in with their new details
    '''
    decoded_jwt = jwt.decode(token.encode('utf-8'), data.secret, algorithms=['HS256'])
    decoded_token = decoded_jwt['token']
    required_user = token_find_user(decoded_token)

    for channel in data.channels:
        for user in channel['all_members']:
            if user['u_id'] == required_user['u_id']:
                user['name_first'] = required_user['name_first']
                user['name_last'] = required_user['name_last']
                user['profile_img_url'] = required_user['profile_img_url']

        for user in channel['owner_members']:
            if user['u_id'] == required_user['u_id']:
                user['name_first'] = required_user['name_first']
                user['name_last'] = required_user['name_last']
                user['profile_img_url'] = required_user['profile_img_url']

        


def user_profile(token, u_id):
    '''
    This function for a valid user, returns information about their
    u_id (int), email (string), first name (string), last name (string), and handle(string).

    This is done by firstly initialising a dictionary called 'profile'.
    Once the u_id that was found is passed in the assigning of the variables will occur.
    Then the 'profile' dictionary is returned.
    '''
    decoded_jwt = jwt.decode(token.encode('utf-8'), data.secret, algorithms=['HS256'])
    decoded_token = decoded_jwt['token']
    token_find_user(decoded_token)
    profile_dict = {}
    u_id_found = False
    for user in data.users:
        if user["u_id"] == u_id:
            
            u_id_found = True
            profile_dict["u_id"] = user["u_id"]
            profile_dict["email"] = user["email"]
            profile_dict["name_first"] = user["name_first"]
            profile_dict["name_last"] = user["name_last"]
            profile_dict["handle_str"] = user["handle_str"]
            profile_dict['profile_img_url'] = user['profile_img_url']

    
    if not u_id_found:
        raise error.InputError(f"User with u_id:{u_id} is not a valid user")
    
    profile = {'user' : profile_dict}
    
    return profile


def user_profile_setname(token, name_first, name_last):
    '''
    This function allows the user to update their name_first and name_last parameters.

    The function will firstly check the name_first and name_last are valid i.e. the names
    are between 1 and 50 characters.

    If both the above parameters are successful then the function will search for the user
    via the token that was passed in and set the new name_first and new name_last for the user.

    '''
    decoded_jwt = jwt.decode(token.encode('utf-8'), data.secret, algorithms=['HS256'])
    decoded_token = decoded_jwt['token']
    name_first_valid = helper.name_length_check(name_first)
    name_last_valid = helper.name_length_check(name_last)

    if not name_first_valid:
        raise error.InputError("The provided first name is not between 1 and 50 characters.")

    if not name_last_valid:
        raise error.InputError("The provided last name is not between 1 and 50 characters.")

    for user in data.users:
        if user["token"] == decoded_token:
            user["name_first"] = name_first
            user["name_last"] = name_last

    # Update user's details in all channels they are in
    update_user_details_in_channels(token)

def user_profile_setemail(token, email):
    '''
    Given an email will update the required user's email to that and will
    check if the email format is correct and if the email has already been registered
    '''
    decoded_jwt = jwt.decode(token.encode('utf-8'), data.secret, algorithms=['HS256'])
    decoded_token = decoded_jwt['token']
    required_user = token_find_user(decoded_token)

    if not helper.validate_email(email):
        raise error.InputError("Email format is invalid")

    if not helper.check_email_has_already_been_registered(email):
        raise error.InputError("Email is already registered")

    required_user['email'] = email

def user_profile_sethandle(token, handle_str):
    '''
    Given a handle, user's handle will be updated to that. Will lso check
    that the length of the handle is correct and that the handle is not already
    in use by someone else
    '''
    decoded_jwt = jwt.decode(token.encode('utf-8'), data.secret, algorithms=['HS256'])
    decoded_token = decoded_jwt['token']
    required_user = token_find_user(decoded_token)

    handle_len = len(handle_str)

    if handle_len < 3 or handle_len > 20:
        raise error.InputError("Handle must be between 3 and 20 chars")

    # Check if the handle is already used by another user
    for user in data.users:
        if user['handle_str'] == handle_str:
            raise error.InputError("Handle already in use")

    required_user['handle_str'] = handle_str


def user_profile_uploadphoto(token, img_url, x_start, y_start, x_end, y_end):
    '''
    This function takes an image url, saves it and sets its path to the profile_img_url
    of the given user.
    '''
    decoded_jwt = jwt.decode(token.encode('utf-8'), data.secret, algorithms=['HS256'])
    decoded_token = decoded_jwt['token']
    required_user = token_find_user(decoded_token)
    
    # Check the working directory of where the server started
    if '/src' in os.getcwd():
        url_to_open = os.getcwd() + f"/img/{required_user['u_id']}"
    else:
        url_to_open = os.getcwd() + f"/src/img/{required_user['u_id']}"


    image = Image.open(url_to_open)
    
    # Check if the image is a valid JPEG image
    if image.format != "JPEG":
        raise error.InputError("image not a JPG")

    image_width, image_height = image.size
    x_valid = False
    y_valid = False
    if x_start >= 0 and x_start <= image_width:
        if x_end >= 0 and x_end <= image_width:
            x_valid = True
    if y_start >= 0 and y_start <= image_height:
        if y_end >= 0 and y_end <= image_height:
            y_valid = True

    if not x_valid or not y_valid:
        raise error.InputError("invalid crop dimensions given")

    # Save the cropped image
    cropped_image = image.crop((x_start, y_start, x_end, y_end))
    cropped_image.save(f"{url_to_open}.jpg", "JPEG")

    # Remove the temp image file that was used previously
    if '/src' in os.getcwd():
        os.remove(f"img/{required_user['u_id']}")
    else:
        os.remove(f"src/img/{required_user['u_id']}")

    # set the profile_img_url of the user
    for user in data.users:
        if user['u_id'] == required_user['u_id']:
            user['profile_img_url'] = f"{img_url}.jpg"

    # Update user's details in all channels they are in
    update_user_details_in_channels(token)

    return