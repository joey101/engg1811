#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ENGG1811 Lab 10

Test file for Question 2
"""
# Import numpy
import numpy as np 

# Define the test cases

# Test case 0
# Define the arrays
x_0 = np.array([6,  6, -6, -6, 4,  4, -4, -4,  1, -1, 1, -1.])
y_0 = np.array([4, -4,  4, -4, 6, -6,  6, -6, -1,  1, 1, -1.])
z_0 = np.array([4,  8, -8, -4, 4 ,-8,  8, -4, -1.5, 1.5, 0.5, -0.5])

# Test case 1
x_1 = np.array([ 1, -3, 4,   0, 1.4,  9.2, 7.3, -5.1])								
y_1 = np.array([-2,  6, 0, -23, 1.9, -4.5, 7.3, -5.1])	
z_1 = np.array([-2.5, 7.5,4. ,-23., 1.2 ,11.45, 3.65, -2.55])

# Put the test cases in an array 
test_cases = [[x_0,y_0,z_0],
              [x_1,y_1,z_1]]

# %% Loop through the test cases 
import q2  
test_number = 0

for test in test_cases:
    # Print test number
    print('Performing test',test_number)
    # Call the function 
    func_output = q2.q2_func(test[0],test[1])

    # Compare function output against expected value 
    if all(func_output == test[2]):
        print('Test passed')
    else:
        print('Test failed')
        print('The test inputs are')
        print('array x is', test[0])
        print('array y is', test[1])
        print('The expected output is:', test[2])
        print('Your output is:', func_output, '\n')        
    # Increment test number
    test_number += 1     

# %% Check if the code has a loop
with open('q2.py','r') as file:
    # Read the contents of the file into an array
    contents = file.readlines()
    
    # Algorithm:
    # First find the line containing function definition
    # For each line after that, check whether 
    # the word for or while is used. Need to check
    # whether it is a comment or not 
    
    # Define two Boolean variables
    # Boolean variable found_def_line is True if the
    # def line has been found
    # Boolean variable found_for_or_while is True if the
    # for or while is found    
    found_def_line = False
    found_for_or_while = False
    
    for line in contents:
        # Skip the lines until the def line is found 
        if not found_def_line: # On or before def line
            if 'q2' in line:
                found_def_line = True
        else:
            # Check for the word for or while 
            if 'for' in line or 'while' in line:   
                # Check whether the word for or while 
                # is in the comment part 
                pos_hash = line.find('#') # returns -1 if not found
                pos_for = line.find('for')                     
                pos_while = line.find('while') 
                  
                if pos_hash == -1:
                    # No hashes in the line
                    found_for_or_while = True
                else: # There is at least a hash 
                    if (pos_for > 0 and pos_for < pos_hash) or \
                       (pos_while > 0 and pos_while < pos_hash):
                        found_for_or_while = True
                                        
    if found_for_or_while:
        print('\nIt looks like you are using loops')   
        
        