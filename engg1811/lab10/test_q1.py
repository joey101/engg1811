#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ENGG1811 Lab 10

Test file for q1 
"""
# import the function 
import q1 

# The test cases 
# Format: List of lists
# Inner level is a list with 4 elements
# [distance, height, speed, function output]
test_cases = [
             [ 7.5, 400,   2.8,	  'Medium'],
             [   6,	150,	 3,		'Easy'],
             [  21,	600,   3.5,	  'Medium'],
             [  21,	600,   3.2,	    'Hard'],
             [  21,	  0,   3.2,	  'Medium'],
             [   2,	400,	 1,	  'Medium'],
             [   2,	610,	 3,	    'Hard'],
             [   8,	  0,	 2,	  'Medium'],
             [   7,	100,	 2,	    'Easy'],
             [   7,	190,	 2,	    'Easy'],
             [   7,	200,	 2,	  'Medium'],
             [  16,	  0,     2,	  'Medium'],
             [  16,	  0,  1.95,	    'Hard'],
             [  16,	 50,	 2,	    'Hard'],
             [  16,	 50,   2.1,   'Medium'],
             [-5.1,  12,  1.51,  'Invalid'],  # Invalid distance  
             [-5.1, -12,  1.51,  'Invalid'],  # Invalid distance and height 
             [  16,  50,     0,  'Invalid'],  # Invalid speed
             [-5.1,  40,     0,  'Invalid'],  # Invalid distance and speed
             [   0, -10,     0,  'Invalid'],  # All parameters are invalid
             ]

# An array to store the test outcomes
# 1 means passed; 0 means failed
test_results = []

# Loop through all the tests 
for test in test_cases:
    # Read the test inputs 
    distance = test[0]
    height = test[1]
    speed = test[2]
    
    try: 
        # Call the function 
        function_output = q1.q1_func(distance,height,speed)
        
        # Compare function output to expected result 
        # Convert to lower case to do case insensitive
        # comparison
        if function_output.lower() == test[3].lower():
            test_results.append(1)
        else:
            print('This test has failed. [d, h, s]: ',test[0:3])
            print('The expected output:', test[3])
            print('Your output:', function_output)
            print('')
            test_results.append(0)
    except:
        print('This test has failed. [d, h, s]: ',test[0:3])
        print('The expected output:', test[3])
        print('Reason: Your function had a run-time error\n')
        test_results.append(0)             

if sum(test_results) == len(test_results):
    print('All tests are passed')    