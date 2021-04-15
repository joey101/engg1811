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
    
    #print('discomfort = ', discomfort_array)
    
    min_inerter = np.min(inerter_array)
    min_damping_coefficient = np.min(damping_coefficient_array)
    print("minimum = ", min_inerter, min_damping_coefficient)
    print(discomfort_array)
    
    discomfort_inerter = np.argmax(discomfort_array, axis=1)
    discomfort_damp = np.argmax(discomfort_array, axis=0)
    print('interter and damp =', discomfort_inerter, discomfort_damp)
    print(np.shape(discomfort_array))
    
    max_inerter = inerter_array[discomfort_inerter]
    max_damping_coefficient = damping_coefficient_array[discomfort_damp]
    print("max = ", max_inerter, max_damping_coefficient)
    
    
    return min_inerter, min_damping_coefficient, \
           max_inerter, max_damping_coefficient
