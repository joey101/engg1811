from error import InputError
from auth import auth_login, auth_register, auth_logout, auth_passwordreset_request, auth_passwordreset_reset
import auth_helper_functions
import pytest
import other
import data 



############################## TESTING ######################################
# Tests for auth_login 
# Test 1 --> Email entered does not belong to a user

# Note that auth_register and auth_login return a {u_id, token} --> and we are comparing these in our tests

# Test auth_login raises InputError for incorrect email
def test_auth_login_wrong_email():
    other.clear()
    auth_register("john.smith@example.com", "abcd1081$#", "John", "Smith")
    with pytest.raises(InputError):
        auth_login("notjohn.smith@example.com", "abcd1081$#")

# Test auth_login returns InputError for an invalid formatted email
def test_auth_login_invalid_email():
    other.clear()
    with pytest.raises(InputError):
        auth_login("notjohnsmithgmailcom", "abcd1081$#")
        
# Test auth_logout successfully works
def test_auth_logout():
    other.clear()
    user = auth_register('john.smith@example.com', 'abcd1234', 'John', 'Smith')
    assert auth_logout(user['token']) == {'is_success': True}

# Test that auth_login works successfully
def test_auth_login_success():
    other.clear()
    user = auth_register('john.smith@example.com', 'abcd1234', 'John', 'Smith')
    assert auth_logout(user['token']) == {'is_success': True}
    user_login = auth_login('john.smith@example.com', 'abcd1234')
    assert user_login['u_id'] == 1

def test_auth_login_two_users():
    other.clear()
    user1 = auth_register('john.smith@example.com', 'abcd1234', 'John', 'Smith')
    user2 = auth_register('will.smith@example.com', 'abcd1234', 'Will', 'Smith')
    auth_logout(user1['token'])
    auth_logout(user2['token'])
    user2_login = auth_login('will.smith@example.com', 'abcd1234')
    assert user2_login['u_id'] == 2
    
#Test 2 --> Password is not correct
def test_auth_login_wrong_password():
    other.clear()
    auth_register("john.smith@example.com", "abcd1081$#", "John", "Smith")
    with pytest.raises(InputError):
        auth_login("john.smith@example.com", "abcd1231$#")


# Tests for auth_register
# Test 1 --> invalid email check 
def test_auth_register_invalid_email_check_acceptable():
    other.clear()
    auth_register("james.bond007@example.com", "CasinoRoyale2006", "James", "Bond")
    auth_login("james.bond007@example.com", "CasinoRoyale2006") 

def test_auth_register_invalid_email_check():
    other.clear()
    with pytest.raises(InputError):
        auth_register("darth.vader.com", "DeathStar2020", "Darth", "Vader")

# Test 2 --> double checking if email address has already been used
def test_email_already_used():
    other.clear()
    auth_register("johnsmith@hotmail.com", "password", "Bob", "Smith")
    with pytest.raises(InputError):
        auth_register("johnsmith@hotmail.com", "New_password", "Goku", "Smith")

# Test 3 --> password checking1 - len(password) < 6
def test_auth_register_password_too_small():
    other.clear()
    with pytest.raises(InputError):
        auth_register("john.smith@example.com", "abc12", "John", "Smith") 

def test_auth_register_no_password():
    other.clear()
    with pytest.raises(InputError):
        auth_register("john.smith@example.com", "", "John", "Smith")

# Test 4 --> name_first checking - len(name_first) <= 1 or len(name_first) > 50
def test_auth_register_name_first_empty():
    other.clear()
    with pytest.raises(InputError):
        auth_register("john.smith@example.com", "abcd1081$#", "", "Smith") 

def test_auth_register_name_first_too_long():
    other.clear()
    with pytest.raises(InputError):
        auth_register("john.smith@example.com", "DKR2012", "JohnAdamAlfredChristianBruceMichaelGaryArnoldArthur", "Smith")

def test_auth_register_name_first_acceptable():
    other.clear()
    test_user = auth_register("tommy.shelby@example.com", "TheGarrison1935", "Tommy", "Shelby") 
    assert test_user['token'] != None
    assert test_user['u_id'] == 1

# Test 5 --> name_last checking --> len(name_last) <= 1 or len(name_last) > 50
def test_auth_register_name_last_empty():
    other.clear()
    with pytest.raises(InputError):
        auth_register("iam.batman@example.com", "Batcave123", "Bruce", "")

def test_auth_register_name_last_too_long():
    other.clear()
    with pytest.raises(InputError):
        auth_register("danaerys.targaryen@example.com", "Dracarys24", "Dany", "OfHouseTargaryenKhaleesiOfTheGreatGrassSeaMotherOfDragons")

def test_auth_register_name_last_acceptable():
    other.clear()
    test_user = auth_register("jon.snow@example.com", "KingOfTheNorth1234", "Jon", "Snow")
    assert test_user['u_id'] == 1
    assert test_user['token'] != None


###################################### auth_passwordreset_request ##########################################

def test_auth_passwordreset_reset_success_case():
    '''
    This test will be used to check whether or not the user
    receives the error_code that was sent out. (This test might be redundant).
    '''
    
    other.clear()
    test_user = auth_register("john.smith@example.com", "abcd1081$#", "John", "Smith") 
    
    auth_passwordreset_request("john.smith@example.com")

    code = ''
    for reset_code in data.reset_codes:
        if test_user['u_id'] == reset_code['u_id']:
            code = reset_code['reset_code']
            

    auth_passwordreset_reset(code, "wxyz1081$#") 
    auth_logout(test_user['token'])
    auth_login("john.smith@example.com", "wxyz1081$#")

def test_auth_passwordreset_reset_another_user():
    '''
    Test if another user can also reset their password
    '''
    other.clear()
    auth_register("john.smith@example.com", "abcd1081$#", "John", "Smith")
    user2 = auth_register("will.smith@example.com", "abcd1081$", "Will", "Smith")

    auth_passwordreset_request("john.smith@example.com")

    auth_passwordreset_request("will.smith@example.com")

    code = ''
    for reset_code in data.reset_codes:
        if user2['u_id'] == reset_code['u_id']:
            code = reset_code['reset_code']
            

    auth_passwordreset_reset(code, "wxyz1081$#") 
    auth_logout(user2['token'])
    auth_login("will.smith@example.com", "wxyz1081$#")

def test_auth_passwordreset_reset_invalid_reset_code():
    '''
    This is a test to ensure that the test fails due to the user 
    inputting an invalid reset_code.
    '''
    other.clear()
    auth_register("john.smith@example.com", "abcd1081$#", "John", "Smith") 
 
    auth_passwordreset_request("john.smith@example.com")

    with pytest.raises(InputError):
        auth_passwordreset_reset(10, "abcd1234$")

def test_auth_passwordreset_reset_invalid_new_password():
    '''
    This is a test to ensure that the test fails as a result of 
    the new_password field not meeting the requirements for a valid password.
    '''
    other.clear()
    test_user = auth_register("john.smith@example.com", "abcd1081$#", "John", "Smith") 
    #auth_passwordreset_request("john.smith@example.com")
    # call a function to randomly generate the reset_code

    auth_passwordreset_request("john.smith@example.com")

    code = ''
    for reset_code in data.reset_codes:
        if test_user['u_id'] == reset_code['u_id']:
            code = reset_code['reset_code']

    with pytest.raises(InputError):
        new_password = "pword"
        auth_passwordreset_reset(code, new_password)

def test_auth_password_reset_request_invalid_email():
    '''
    Test that an InputError is raised when an invalid email is given
    '''
    other.clear()
    auth_register("john.smith@example.com", "abcd1081$#", "John", "Smith") 

    with pytest.raises(InputError):
        auth_passwordreset_request("john.smith@nottheemail.com")

