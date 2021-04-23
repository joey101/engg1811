#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 

@author: 
    
Purpose:
   Determining the discomfort levels for a given damper values and inerter values

Inputs:
   discomfort_array   2-dimentional numpy array with discomfort values for 
                      given inerter_values and damping_coefficient_values (read the specs)    
   inerter_values     inertance values (array of type float)
   damping_coefficient_values  damping coefficient values (array of type float)
   discomfort_upper_limit      maximum discomfort value to calculate worst comfort
                               (i.e. 'max_inerter' and 'max_damping_coefficient' values)
   

Output:
    min_inerter and min_damping_coefficient  the pair that gives the smallest value of discomfort  
    max_inerter and max_damping_coefficient  the pair that gives the worst value of discomfort, that
                                             is less than or equal to a given 'discomfort_upper_limit'
   
"""

import numpy as np

def optimise_qc(discomfort_array, inerter_array, damping_coefficient_array, discomfort_upper_limit):

    
#   MINIMUM FUNCTIONS:   
    # Find the smallest value and its coordinates.
    minimum = np.min(discomfort_array)
    min_where = np.argwhere(discomfort_array == minimum)
    
    # Access coordinates.
    min_in = min_where[0][0]
    min_di = min_where[0][1]
    
    # Use Coordinates as index for the value in the row and column.
    min_inerter = inerter_array[min_in]
    min_damping_coefficient = damping_coefficient_array[min_di]

    
    # print(min_in, min_di)
    # print('discomfort = ', discomfort_array)
    # print("minimum = ", min_inerter, min_damping_coefficient, minimum, where)

# ----------------------------------------------------------------------------
#   MAX FUNCTIONS
    
    # Sliced the values underneath the limit to find the maximum in the 
    # sub-list. Then find the coordinates of the max number in bigger array.
    sliced_limit = discomfort_array[discomfort_array <= discomfort_upper_limit]
    maximum = np.max(sliced_limit)
    max_where = np.argwhere(discomfort_array == maximum)
    
    # Access coordinates.
    max_in = max_where[0][0]
    max_di = max_where[0][1] 
    
    # Use Coordinates as index for the value in the row and column.
    max_inerter = inerter_array[max_in]
    max_damping_coefficient = damping_coefficient_array[max_di]
   
    
    print('Inerter and Damp =', max_inerter,max_damping_coefficient, max_where)
    #test = np.max(discomfort_array)
    #print('test', test, np.shape(test))
    
    return min_inerter, min_damping_coefficient, \
           max_inerter, max_damping_coefficient
