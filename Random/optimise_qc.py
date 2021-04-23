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
    small = np.min(discomfort_array)
    low = np.where(discomfort_array == small)
    min_inerter = inerter_array[low[0]]
    min_damping_coefficient = damping_coefficient_array[low[1]]
    
    cut = discomfort_array[discomfort_array <= discomfort_upper_limit]
    highest = np.max(cut)
    highest_point = np.where(discomfort_array == highest)
    max_inerter = inerter_array[highest_point[0]]
    max_damping_coefficient = damping_coefficient_array[highest_point[1]]
   
    return min_inerter, min_damping_coefficient, \
           max_inerter, max_damping_coefficient
