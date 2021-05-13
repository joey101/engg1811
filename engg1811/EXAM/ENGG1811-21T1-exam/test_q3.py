#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ENGG1811 Exam

Test file for Question 3 
"""
# import the function 
import q3 

# The test cases 
# Format: List of lists
# Inner level is a list with 3 elements
# [t1, t2, classification]
# 

test_cases = [
             [300, 220, 'alertHigh'],
             [125,	135,  'alertLow'],
             [30, 45, 'normalLow'],
             [100, 60,    'normalHigh']
             ]

# An array to store the test outcomes
# 1 means passed; 0 means failed
test_results = []

# Loop through all the tests 
for test in test_cases:
    # Read the test inputs 
    t1 = test[0]
    t2 = test[1]
    
    # Call the function 
    classification_from_function = q3.q3_funct(t1, t2)
    
    # Compare function output to expecte result 
    # Convert to lower case to do case insensitive
    # comparison
    if classification_from_function.lower() == test[2].lower():
        test_results.append(1)
    else:
        print('This test not passed',test)
        test_results.append(0)

if sum(test_results) == len(test_results):
    print('All tests are passed')    