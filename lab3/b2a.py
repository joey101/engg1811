# -*- coding: utf-8 -*-
"""
Created on Wed Feb 24 18:47:21 2021

Creating a program that convers bearings to an angle

@author: Jawad
"""
import matplotlib.pyplot as plt
# import math as m

user = float(input('input a real number between 0.0 to 360.0 inclusively: '))

conv1 = user
# y = -x + 450
# y = -x + 90
if conv1 <= 270:
    conv1 = -conv1 + 90
    print('Bearing', user, '-->', 'Angle', conv1)
elif conv1 >= 270:
    conv1 = -conv1 + 450 
    print('Bearing', user, '-->', 'Angle', conv1)
    
