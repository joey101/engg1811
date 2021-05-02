#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ENGG1811 18s2 exam 

Test file for Question 1a
"""

# Test case 0
a_list_0 = [10,5,12]
a_0 = 5
b_0 = 13
expected_output_0 = True     # Expected output

# Test case 1
a_list_1 = [10,5,12,11]
a_1 = 5
b_1 = 12
expected_output_1 = False    # Expected output

# Test case 2
a_list_2 = [10,5,12,11]
a_2 = 6
b_2 = 13
expected_output_2 = False    # Expected output

# Assemble the test cases into a list of lists / lists
a_list_all = [a_list_0,a_list_1,a_list_2]
a_all = [a_0,a_1,a_2]
b_all = [b_0,b_1,b_2]
expected_output_all = [expected_output_0,expected_output_1,expected_output_2]

# %% Testing 
import q1a

for k in range(len(a_list_all)):
    a_list = a_list_all[k]
    a = a_all[k]
    b = b_all[k]
    output = q1a.q1a_func(a_list,a,b)
    if output == expected_output_all[k]:
        print('Test case',str(k),':','Passed')
    else:
        print('Test case',str(k),':','Failed')
    
