#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ENGG1811 18s2 exam 

Test file for Question 1b
"""

# Test case 0
a_list_0 = [[3,4,8],[6,12],[7,8,14],[-1,-6,-9]]
m_0 = 14
expected_output_0 = [0,1,2,3]

# Test case 1
a_list_1 = a_list_0
m_1 = 9
expected_output_1 = [0,3]

# Test case 2
a_list_2 = a_list_0
m_2 = 7
expected_output_2 = [3]

# Test case 3
a_list_3 = a_list_0
m_3 = -6
expected_output_3 = []

# Test case 4
a_list_4 = [[3,4,-8],[-6,-12],[-7,8],[-1,-6,-9,-10,-2]]
m_4 = 0
expected_output_4 = [1,3]

# Test case 5
a_list_5 = [[3,4,-8],[-6,-12],[-7,8],[-1,-6,-9,-10,-2]]
m_5 = 5
expected_output_5 = [0,1,3]

a_list_all = [a_list_0,a_list_1,a_list_2,a_list_3,a_list_4,a_list_5]
m_all = [m_0,m_1,m_2,m_3,m_4,m_5]
expected_output_all = [expected_output_0, expected_output_1,
                       expected_output_2, expected_output_3,
                       expected_output_4, expected_output_5]

# %% Testing
import q1b

for k in range(len(a_list_all)):
    a_list = a_list_all[k]
    m = m_all[k]
    output = q1b.q1b_func(a_list,m)
    output.sort()
    print('Test case',k,':')
    print('\tOutput returned by you function: ',output)
    print('\tOutput expected: ',expected_output_all[k])
    