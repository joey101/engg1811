"""
    Creating a key logging program.

    The goal is to log key strokes with the date and time for each sentence.

"""


import numpy as np
import time as t


with open("/home/bladerunner/Documents/python/keylogger/log.txt",'r') as logging:
    for line in logging: 
        print("first line contains: ", line)



