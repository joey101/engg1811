import auth_helper_functions as helper #include the functions
import error
import data
import jwt
import hashlib

def auth_login(email, password):
    #checking if provided email is invalid
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    if not helper.validate_email(email):
        raise error.InputError("The provided email is invalid")

    #If the email inputted, does not belong to a current user
    user_not_valid = True
    u_id = 0
    token = 0
    for user in data.users:
        if user.get('email') == email:
            user_not_valid = False
            u_id = user['u_id']
            break
    
    if user_not_valid == True:
        raise error.InputError("The provided email is not registered")

    #If the password inputted is not correct
    not_valid_password = True
    for user in data.users:
        if user.get("email") == email:
            if user.get("password") == hashed_password:
                not_valid_password = False
    
    if not_valid_password == True:
        raise error.InputError("The provided password is not valid")

    for user in data.users:
        if user['u_id'] == u_id:
            user['token'] = user['u_id']
            token = jwt.encode({'token' : user['u_id']}, data.secret, algorithm='HS256').decode('utf-8')
            
    return {'u_id': u_id, 'token': token}
    
    
def auth_logout(token):
    #logging out the user (setting their token to None)
    decoded_jwt = jwt.decode(token.encode('utf-8'), data.secret, algorithms=['HS256'])
    decoded_token = decoded_jwt['token']
    for user in data.users:
        if user['token'] == decoded_token:
            user['token'] == None
            
    return {'is_success': True}


def auth_register(email, password, name_first, name_last):
    # Perform parameter checking first
    # 1) Valid email check 
    email_valid = helper.validate_email(email)
    if email_valid == False:
        raise error.InputError("The email you have provided is invalid.")
    # 2) Email has already been registered
    email_not_already_registered = helper.check_email_has_already_been_registered(email)
    if email_not_already_registered == False:
        raise error.InputError("The email you have provided has already been registered.")
    # 3) len(password) must be greater than 6 characters
    password_valid = helper.password_check(password)
    if password_valid == False:
        raise error.InputError("The password you have provided must be greater than 6 characters.")
    # 4) len(name_first) must be between 1 and 50 characters
    name_first_valid = helper.name_length_check(name_first)
    if name_first_valid == False:
        raise error.InputError("The provided first name is not between 1 and 50 characters.")
    # 5) len(name_last) must be between 1 and 50 characters
    name_last_valid = helper.name_length_check(name_last)
    if name_last_valid == False:
        raise error.InputError("The provided last name is not between 1 and 50 characters.")

    # Start to assign variables
    new_user = {}
    new_user['u_id'] = data.num_users + 1
    new_user['email'] = email
    new_user['password'] = hashlib.sha256(password.encode()).hexdigest()
    new_user['name_first'] = name_first
    new_user['name_last'] = name_last
    new_user['token'] = new_user['u_id']
    new_user['handle_str'] = helper.generate_user_handle_str(name_first, name_last)
    new_user['profile_img_url'] = ""
    if data.users == []:
        new_user['permission_id'] = 1
    else:
        new_user['permission_id'] = 2
    data.users.append(new_user)
    return_user = {}
    return_user['u_id'] = new_user['u_id']
    return_user['token'] = jwt.encode({'token' : new_user['u_id']}, data.secret, algorithm='HS256').decode('utf-8')
    data.num_users += 1
    return return_user

def auth_passwordreset_request(email):
    '''
    This function will search through the users data structure, check if the 
    user is registered and then send an email to the user with their 16 digit 
    alphanumeric reset code. 
    '''
    # Find if the email is valid/ is a registered user
    current_user = {}
    is_registered_user = False
    for user in data.users:
        if user['email'] == email:
            is_registered_user = True
            # picking up the u_id to be used when adding the user to the rest_codes list
            current_user['u_id'] = user['u_id']

    # Send the email
    if is_registered_user:
        # generate reset_code
        reset_code = helper.generate_reset_code(current_user['u_id'], email)
        # create a dictionary to be appended to reset_codes list 
        reset_dict = {}
        reset_dict['user_email'] = email
        reset_dict['u_id'] = current_user['u_id']
        reset_dict['reset_code'] = reset_code
        data.reset_codes.append(reset_dict)
        #the sending of the reset code is done through an external helper
        helper.send_reset_code_email(email, reset_code)
    else:
        raise error.InputError("given email does not exist")

def auth_passwordreset_reset(reset_code, new_password):
    '''
    This function resets the password for the user based on their new password they have reset it to.
    This function will firstly check if the reset_code is valid by firstly searching the reset_code in the 
    resets_codes storage structure, secondly checks if the new_password is valid, thirdly hashes the new_password
    and overwrites it in the user data storage structure.
    '''
    # Need to check if the reset_code is valid first
    current_user = {}
    is_reset_code_valid = False
    for user in data.reset_codes:
        if user['reset_code'] == reset_code:
            is_reset_code_valid = True
            #collect email address
            current_user['email'] = user['user_email'] ##
        
    # Raise error if reset_code is not valid
    if is_reset_code_valid == False:
        raise error.InputError("Invalid reset code.")

    # Need to check if the new_password is valid, otherwise raise error
    password_result = helper.password_check(new_password)
    if not password_result:
        raise error.InputError("Password entered is not a valid password.")
   
    # hash it then store accordingly
    new_password_hashed = hashlib.sha256(new_password.encode()).hexdigest()

    # Set the new_password_hashed for the particular user.
    for targeted_user in data.users:
        if current_user['email'] == targeted_user['email']:
            targeted_user['password'] = new_password_hashed

        