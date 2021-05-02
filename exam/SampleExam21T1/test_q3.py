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
# Inner level is a list with 4 elements
# [mass, height, classification]
# 
# Note: Some numbers are not realistic, they are
# there to test your code 
test_cases = [
             [45.4, 1.57, 'Underweight'],
             [40,	1.5,  'Underweight'],
             [49.7, 1.64, 'Underweight'],
             [74.0, 2,    'Healthy'],
             [50,   1.6,  'Healthy'],
             [71.8, 1.73, 'Healthy'],
             [100,  2,    'Overweight'],
             [70.8, 1.62, 'Overweight'],
             [89.5, 1.73, 'Overweight'],
             [120,  2,    'Obese'],
             [84.7, 1.68, 'Obese'],
             [152,  1.7,  'Obese']
             ]

# An array to store the test outcomes
# 1 means passed; 0 means failed
test_results = []

# Loop through all the tests 
for test in test_cases:
    # Read the test inputs 
    mass = test[0]
    height = test[1]
    
    # Call the function 
    classification_from_function = q3.q3_func(mass,height)
    
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