# Assumptions

## Iteration 1
 * IDs start from 1 and not 0

 * a user can join a public channel with channel_join,
but a user needs to be invited (channel_invite) by 
an owner for a private channel

 * channel_addowner only works for users that are in the channel

 * channel_invite can be used in both public and private channels,
but for public channels the user inviting does not have to be an
owner

 * the user who creates a channel with channel_create is automatically
an owner

 * auth_register automatically logs you in (assigns a token)

 * we assume the user has logged out if they're token is 'None'

 * we assume a user has logged in if they have a token

 * channel_messages returns a dictionary of the form :
Return = {
	Messages : [0..49] (where 0 is the newest message and 49 is the oldest),
	'start' = (whatever start was input),
        'end' = (either start + 50 or -1 if there are not more than 50 messages before start)

## Iteration 2
* if messages is empty, channel_messages returns a dictionary with empty messages

* If there is only 50 messages in the channel, channel_messages would return -1 
for 'end' if start is 0 since there are no messages after 50

* The first user to register is automatically given the owner permission_id

* once the permission has been changed of a user, they automatically become part 
of the 'owner_members' of the channels they are a part of

* user_setname does not change the handle string


* the jwt token gets passed around the functions as a utf-8 decoded string using 
.decode('utf-8') rather than the binary itself.

* hashing of passwords is taken care of in auth.py and not server.py

## Iteration 3 
* The 'time_finish' that is returned in standup_start is a unix
timestamp for when the standup finishes

* In order to successfully test auth_passwordreset_request and 
auth_passwordreset_reset, whitebox testing method has to be used to 
ensure that the reset_code could be retrieved

* uploadphoto needs the server url and thus only http testing can 
be used to properly test uploadphoto