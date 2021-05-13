#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ENGG1811 20T1 final exam 

Test file for Question 4 
"""

# %% import numpy
import numpy as np 

# Test case 0
expt_data_0 = np.array([[9.6, 3.5, 1.7, 2.8],
                        [2.2, 1.1, 1.3, 1.6],
                        [2.4, 1.0, 1.1, 1.3],
                        [6.7, 6.9, 4.9, 0.7],
                        [0.6, 2.0, 0.3, 0.5]]) 
predicted_means_0 = np.array([4.3, 1.6, 1.7, 1.1, 2.7])
expected_output_0 = 3
# experimental means [4.4 , 1.55, 1.45, 4.8 , 0.85]

# Test case 1
expt_data_1 = expt_data_0
predicted_means_1 = np.array([4.5, 1.3, 1.2, 2.1, 4.5])
expected_output_1 = 4
# experimental means [4.4 , 1.55, 1.45, 4.8 , 0.85]

# Test case 2
expt_data_2 = np.array([[4.6, 4.5, 2.7, 8.8, 4.7, 6.6],
                        [2.3, 1.6, 2.3, 4.6, 6.7, 5.7],
                        [2.4, 1.0, 1.1, 1.3, 1.4, 1.6],
                        [6.7, 6.9, 4.9, 0.7, 5.4, 4.7],
                        [0.6, 2.0, 0.3, 0.5, 0.6, 0.9],
                        [1.3, 2.1, 2.6, 2.9, 4.1, 2.3],
                        [1.6, 2.9, 2.4, 5.6, 6.1, 5.6]]) 
predicted_means_2 = np.array([2.3, 3.6, 1.5, 4.1, 0.7, 2.1, 4.0])
expected_output_2 = 0
# experimental means 
# array([5.31666667, 3.86666667, 1.46666667, 4.88333333, 0.81666667,
#        2.55      , 4.03333333])

# Test case 3
expt_data_3 = np.array([[1.6, 2.9, 2.4, 4.6, 4.5, 2.7, 2.8, 4.7, 6.6],
                        [6.7, 2.9, 4.9, 2.3, 1.6, 2.3, 4.6, 6.7, 5.7]]) 
predicted_means_3 = np.array([2.3, 6.6])
expected_output_3 = 1
# experimental means 
# array([3.64444444, 4.18888889])
    
expt_data_all = [expt_data_0, expt_data_1, 
                 expt_data_2, expt_data_3]
predicted_means_all = [predicted_means_0, predicted_means_1, 
                       predicted_means_2, predicted_means_3]
expected_output_all = [expected_output_0, expected_output_1, 
                       expected_output_2, expected_output_3]

# %% Testing 
import q5

for k in range(len(expt_data_all)):
    expt_data = expt_data_all[k]
    predicted_means = predicted_means_all[k]
    
    your_output = q5.q5_func(expt_data, predicted_means)
    if your_output == expected_output_all[k]:
        print('Test case',k,':','Passed','\n')
    else:
        print('Test case',k,':','Failed')
        print('Your output is:', your_output)
        print('Expected output is:', expected_output_all[k],'\n')
    