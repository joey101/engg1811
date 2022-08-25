
dm = [{
                'u_id': 1,
                'email': 'rima@gmail.com',
                'name_first': 'Rima',
                'name_last': 'Nigudkar',
                'handle_str': 'rimanigudkar'
            },
            {
                'u_id': 2,
                'email': 'abbas.tanana@gmail.com',
                'name_first': 'Abbass',
                'name_last': 'Tanana',
                'handle_str': 'abbasstanana'
            }]


dms = { 'u_id': 2,
        'email': 'abbas.tanana@gmail.com',
        'name_first': 'Abbass',
        'name_last': 'Tanana',
        'handle_str': 'abbasstanana'

}
for direct in dm:
    if direct['u_id'] == dms['u_id']:
        dm.remove(dms)
  
        break

print(dm)