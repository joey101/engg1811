users = []
channels = []
num_users = 0
num_channels = 0
num_messages = 0
reset_codes = []
secret = "Lisa, in this house we obey the laws of thermodynamics!"

'''
reset_codes storage structre:

reset_codes [
    {
        'u_id' : 1,
        'user_email' : email,
        'reset_code': asldhasjfsdhkfhsfbsakjf
    },
    {
        'u_id' : 2,
        'user_email' : email,
        'reset_code' : kkjhhiyghsiufgsdifgsdf
    },
    ...
]

user storage structure:
    users is a list that
    contains dictionaries
    for example:
        users [
            {
                'u_id' : 1
                'email' : example@gmail.com
                'password' : verygoodpassword
                'name_first' : John
                'name_last' : Smith
                'token' : encoded jwt token
                'handle_str': johnsmith
            },
            ...
        ]

'''

'''
channel storage structure:
    channels is a list that
    contains dictionaries
    for example:
        channels [
            {
                'channel_id' : 1
                'name' : 'My Channel'
                'is_public' : True
                'standup_endtime': None,
                'standup_conversation': Message
                'owner_members' : [
                    {
                        'u_id': 1,
                        'name_first': 'Hayden',
                        'name_last': 'Jacobs',
                    }
                ],
                'all_members': [
                    {
                        'u_id': 1,
                        'name_first': 'Hayden',
                        'name_last': 'Jacobs',
                    },{
                        'u_id': 2,
                        'name_first': 'John',
                        'name_last': 'Smith',
                    }
                ],
                'messages': [
                    {
                        'message_id': 1,
                        'u_id': 1,
                        'message': 'Hello world',
                        'time_created': 1582426789,
                    }
                ],
            },
            ...
        ]

'''