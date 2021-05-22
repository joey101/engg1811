#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ENGG1811 21T1 exam 

Test file for Question 1
"""

# Test case 0
a_list_0 = [10,5,12]
expected_output_0 = 5     # Expected output

# Test case 1
a_list_1 = [10,-5, 12, 4, 11]
expected_output_1 = 4    # Expected output

# Test case 2
a_list_2 = [ -45, -19, -5, -89, -34]
expected_output_2 = 0    # Expected output

# Assemble the test cases into a list of lists / lists
a_list_all = [a_list_0,a_list_1,a_list_2]
expected_output_all = [expected_output_0,expected_output_1,expected_output_2]

# %% Testing 
import q1

for k in range(len(a_list_all)):
    a_list = a_list_all[k]
    output = q1.q1_funct(a_list)
    if output == expected_output_all[k]:
        print('Test case',str(k),':','Passed')
    else:
        print('Test case',str(k),':','Failed')
    
