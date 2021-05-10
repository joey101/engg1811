#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ENGG1811 18s2 exam 

Template for Question 1a. 
"""
import numpy as np
def q1a_func(a_list,a,b):
    
    temp = np.array(a_list)
    temp = (temp >= a) & (temp < b)
    
    if temp[~temp] == False:
        
        return False
    else:
        return True
    
