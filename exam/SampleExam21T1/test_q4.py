#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ENGG1811 Exam

Test file for Question 4
"""
# Import numpy
import numpy as np 

# Define the test cases
# x is one-dimensional numpy array
# t is a positive scalar (float)
# z is the expected answer 

# Test case 0
x_0 = np.array([6, -6, 4, -4, 1, -1.])
t_0 = 5.
z_0 = np.array([ 1. , -1. ,  0.8, -0.8,  0.2, -0.2])

# Test case 1
x_1 = np.array([4,  8, -8, -4, -1.5, 1.5, 0.5, -0.5])
t_1 = 4.2
z_1 = np.array([ 0.95238095,  1., -1., -0.95238095, 
                -0.35714286, 0.35714286,  0.11904762, 
                -0.11904762])

# Test case 2
x_2 = np.array([ 1, -3, 4,   0, 1.4,  9.2, 7.3, -5.1])								
t_2 = 3.7
z_2 = np.array([ 0.27027027, -0.81081081,  1.,  0.,  
                0.37837838, 1.,  1., -1.])

# Put the test cases in an array 
test_cases = [[x_0,t_0,z_0],
              [x_1,t_1,z_1],
              [x_2,t_2,z_2]]

# %% Testing 
import q4  

# Tolerance for comparison 
TOL = 0.001

# Loop through the test cases 
test_number = 0
for test in test_cases:
    # Print test number
    print('Performing test',test_number)
    # Call the function 
    func_output = q4.q4_func(test[0],test[1])
    # Compare function output against expected value 
    # print(func_output)
    if np.all(np.abs(func_output - test[2]) < TOL):
        print('Test passed')
    else:
        print('Test failed')
    # Increment test number
    test_number += 1     

