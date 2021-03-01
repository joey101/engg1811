# -*- coding: utf-8 -*-
"""
Created on Wed Feb 24 18:47:21 2021

Creating a program that convers bearings to an angle

@author: Jawad
"""
import matplotlib.pyplot as plt
# import math as m

user = float(input('input a real number between 0.0 to 360.0 inclusively: '))



conv1 = 90 - user

if conv1 <= 0:
    conv1 + 360
elif conv1 >= 360:
    conv1 - 360 

print('Bearing', user, '-->', 'Angle', conv1)    
