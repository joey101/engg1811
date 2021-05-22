#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ENGG1811 21T1 final exam 

Template for Question 4.   
"""

# Import numpy
import numpy as np

def q4_func(array_a,b):   
    """
    temp = np.array(array_a)
    temp = (array_a >= b)
    
    
    temp[temp] = (temp[temp] - b) / 2.0
    temp[~temp] = pow(temp[~temp],2)             
   
    
    return np.sum(temp)
    """
    
 
    temp = np.zeros(len(array_a))
    
    for num in range(len(array_a)):
        if array_a[num] > b:
            temp[num] = (array_a[num] - b) / 2
        else:
            temp[num] = pow(array_a[num],2)
    
    return np.sum(temp)
