#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 13 12:09:31 2021

@author: bladerunner
"""
import numpy as np


num_a = 0
mean_data = []
sliced = []
for i in range(0,30):
    
    with open("/home/bladerunner/Documents/engg1811/lab9/lab09A/" + 'temp'+str('%02d' % i)+'.txt', 'r') as data:
        first_line = data.readline()
        second = data.readline()
        second_line = np.array(second.split())      
        second_line_float = second_line.astype(np.float)
        
        length = int(first_line[2])
       
        if (first_line[0] == 'A'):
            num_a += 1
            
            
        sliced = second_line_float[0:length]
        mean_data = np.append(mean_data, np.mean(sliced))

print('A comes :', num_a, 'times')
print("Mean List: ", mean_data)
