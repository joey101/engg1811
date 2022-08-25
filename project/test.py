from data_store import data_store

num = 0
ds = data_store.get()

u_id = len(ds['users'])

Info = {
    'firstname' : 'name_first',
    'lastname' : 'name_last',
    'email' : 'jawad.tnana@gmail.com',
    'password' : 'password',
    'username' : '' 
}


print(ds['channels'])





"""




idx = 0

store = ds['Users']
for user in store:
        print(store[user]['email']) 
        '''if user[idx]['email'] == 'jawad.tnana@gmail.com':
            print(user['email']) 
        else:
            idx +=1'''
    """
'''
print(ds)


print(ds['Users'][u_id]['username'])
'''



#print(ds['Users'][1]['firstname'])













