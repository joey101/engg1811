#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ENGG1811 21T1 final exam 

Test file for Question 4 
"""

# %% import numpy
import numpy as np 

# Test case 0
array_a_0 = np.array([-9.6, 0.9, 1.1, 2.8]) 
b_0 = 1.0
expected_output_0 = 93.92

# Test case 1
array_a_1 = np.array([-4.6, 4.5, -2.7, -8.8, 4.7, 6.6])
b_1 = 2.3
expected_output_1 = 110.34

# Test case 2
array_a_2 = np.array([2.3, -1.6, 2.3, 4.6, -6.7, 5.7, -4.7]) 
b_2 = -4.0
expected_output_2 = 83.63

# Test case 3
array_a_3 = np.array([-1.6, 2.9, 2.4, -4.6]) 
b_3 = 0 
expected_output_3 = 26.36
    
array_a_all = [array_a_0, array_a_1, 
               array_a_2, array_a_3]
b_all = [b_0, b_1, b_2, b_3]
expected_output_all = [expected_output_0, expected_output_1, 
                       expected_output_2, expected_output_3]

# %% Testing 
import q4

TOL = 0.1 # Tolerance for testing

for k in range(len(array_a_all)):
    array_a = array_a_all[k]
    
    if k < 4: 
        b = b_all[k]
        your_output = q4.q4_func(array_a, b)
        able_to_execute = True
 
       
    if able_to_execute: 
        if abs(your_output - expected_output_all[k]) < TOL:
            print('Test case',k,':','Passed','\n')
        else:
            print('Test case',k,':','Failed')
            print('Your output is:', your_output)
            print('Expected output is:', expected_output_all[k],'\n')
    