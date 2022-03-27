import re
import data
import random
import string
import smtplib 
import ssl


regex = '^[a-z0-9]+[\\._]?[a-z0-9]+[@]\\w+[.]\\w{2,3}$' 


def validate_email(email):
    '''
    checks if the email is a valid email
    '''
    if (re.search(regex, email)):
        return True
    else:
        return False 
def check_email_has_already_been_registered(email):
    '''
    checks if the email has already been registered
    '''
    for user in data.users:
        if user['email'] == email: #if email is already registered
            return False
    return True

def password_check(password):
    '''
    checks if password is long enough
    '''
    if len(password) > 6:
        return True
    else: 
        return False 

def name_length_check(name):
    '''
    check if name is too long
    '''
    if len(name) >= 1 and len(name) <= 50:
        return True
    else:
        return False


def generate_user_handle_str(name_first, name_last):
    '''
    - This function generates a handle for the user that is attempting to register 
    - A handle is generated that is the concatentation of a lowercase-only first name and last name
    - If the concatenation is longer than 20 characters, it is cutoff at 20 characters. 
    - If the handle is already taken, you may modify the handle in any way you see fit to make it unique.
    '''
    # Generate the handle_str using the inputted name_first and name_last

    # Concatenate strings and limit it to 20 lower characters 
    handle_str = name_first.lower() + name_last.lower()
    if len(handle_str) >= 20: 
        handle_str = handle_str[:20]

    # Search for repeats of handle_strings
    num_repeats = 0
    for user in data.users:
        if user['handle_str'] == handle_str:
            num_repeats += 1
            # change the first few characters of the handle_str to numbers depending on repeats
            num_string = str(num_repeats)
            i = 0
            for char in num_string:
                handle_str_list = list(handle_str)
                handle_str_list[i] = char
                handle_str = "".join(handle_str_list)
                i += 1

    return handle_str

def generate_reset_code(u_id, email):
    '''
    This is a function that will be used to generate an alphanumeric code of
    8 characters long. 
    Characters will include numerics 0-9, alpabetics a-z and A-Z.
    '''
    code = ''.join(random.choices(string.ascii_letters + string.digits, k=16))
    reset_code_data = {
        'u_id' : u_id,
        'user_email': email,
        'reset_code': code
    }

    data.reset_codes.append(reset_code_data)
    return code 

def send_reset_code_email(email, reset_code):
    '''
    This function is used to send out an email to a specified user with their unique
    16 digit alphanumeric reset code. 
    '''
    port = 465 
    smtp_server = "smtp.gmail.com"
    sender_email_address = "thuorangeteam1@gmail.com"  
    receiver_email_address = email  
    password_sender = "Abcd1234$" 

    profile = {}

    for user in data.users:
        if user["email"] == email:
            profile["email"] = user["email"]
            profile["name_first"] = user["name_first"]

    
    message = f"""\
    Subject: Personal password reset code

    Hi {profile['name_first']},

    Your personal pass reset code is: {reset_code} . 

    This message is sent from the team at Flockr."""

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(sender_email_address, password_sender)
        server.sendmail(sender_email_address, receiver_email_address, message)

