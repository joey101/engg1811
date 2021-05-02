#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ENGG1811 Exam

Test file for Question 5
"""
import numpy as np  

# %% 
# Test cases 

# Test case 0 
# The inputs are: 
array_0 = np.array([-2,  6, 0, -23, 1.9, -4.5, 7.3, -5.1])	
n_0 = 4 
# Expected function output 
output_0_expected = np.array([ -0.1,   1.5,   7.3, -28.1])
# 
# Explanation:
# array_0 has 8 entries 
# n_0 is 4 
# Integer part of 8/4 is 2
# 
# output_0_expected[0] is sum of array_0[0] and array_0[4],
#       which is -2 + 1.9 = -0.1
# 
# output_0_expected[1] is sum of array_0[1] and array_0[5],
#       which is 6 + (-4.5) = 1.5
#
# output_0_expected[2] is sum of array_0[2] and array_0[6],
#       which is 0 + 7.3 = 7.3
# 
# output_0_expected[3] is sum of array_0[3] and array_0[7],
#       -23 + (-5.1) = -28.1


# Test case 1
# The inputs are:  
array_1 = np.array([-2,  6, 0, -23, 1.9])	 
n_1 = 2 
# Expected function output 
output_1_expected = np.array([ -2., -17.])
# 
# Explanation:
# array_1 has 5 entries 
# n_1 is 2 
# Integer part of 5/2 is 2
# 
# output_1_expected[0] is sum of array_1[0] and array_1[2],
#       which is -2 + 0 = -2
# 
# output_1_expected[1] is sum of array_1[1] and array_1[3],
#       which is 6 + -23 = -17
# 
# Remark: Note that the last element 1.9 is not used 

# Test case 2 
# The inputs are: 
array_2 = np.array([1, -3, 4, 0, 1.4,  9.2, 7.3, -5.1, 2.7, -1.7, 3.7])	# 
n_2 = 3 
# Expected function output 
output_2_expected = np.array([8.3,  -6.7,  15.9])
# 
# Explanation:
# array_2 has 11 entries 
# n_2 is 3 
# Integer part of 11/3 is 3
# 
# output_2_expected[0] is sum of array_2[0], array_2[3] and
#       array_2[6] 
#       which is 1 + 0 + 7.3 = 8.3
#
# output_2_expected[1] is sum of array_2[1], array_2[4] and
#       array_2[7] 
#       which is -3 + 1.4 + (-5.1) = -6.7
#
# output_2_expected[2] is sum of array_2[2], array_2[5] and
#       array_2[8] 
#       which is 4 + 9.2 + 2.7 = 15.9
#  
# Remark: Note that the last two elements -1.7 and 3.7 are not used 


# Test case 3 
# The inputs are:  
array_3 = np.array([1., 4., 2., 10.])	 
n_3 = 1
# Expected function output 
output_3_expected = np.array([17.])
# Explanation:
# array_3 has 4 entries 
# n_3 is 1 
# Integer part of 4/1 is 4
# 
# output_3_expected[0] is sum of array_3[0], array_3[1], 
#       array_3[2] and array_3[3]
#       which is 1. + 4. + 2. + 10. = 17. 
#  

# Pack the test cases into a list of lists
test_cases = [[array_0, n_0, output_0_expected],
              [array_1, n_1, output_1_expected],
              [array_2, n_2, output_2_expected],
              [array_3, n_3, output_3_expected]]

# %%
import q5  

# Specify tolerance for floating point comparison
TOL = 0.01

# Initialise test number
test_number = 0  

# Loop through the tests 
for test in test_cases:
    # Print test number
    print('Performing test',test_number)
    # Call the function 
    func_output = q5.q5_func(test[0],test[1])
    # Compare function output against expected value 
    if np.all(np.abs(func_output - test[2]) < TOL):
        print('Test passed')
    else:
        print('Test failed')
    # Increment test number
    test_number += 1     


# End of file 
