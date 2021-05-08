# -*- coding: utf-8 -*-
"""
Created on Wed Feb 24 18:47:21 2021

Creating a program that convers bearings to an angle

@author: Jawad
"""
import matplotlib.pyplot as plt
# import math as m

bearing = float(input('input a real number between 0.0 to 360.0 inclusively: '))

conv1 = bearing
# y = -x + 450
# y = -x + 90
if bearing < 360 or bearing > 0:
    if conv1 < 270:
        conv1 = -conv1 + 90
        print('Bearing', bearing, '-->', 'Angle', conv1)
    else:
        conv1 = -conv1 + 450 
        print('Bearing', bearing, '-->', 'Angle', conv1)
else:
    print("I told you between 0 and 360")
