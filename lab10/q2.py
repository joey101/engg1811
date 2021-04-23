#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ENGG1811 Lab 10

Template file for Question 2 
"""
# Import numpy
import numpy as np 

def q2_func(x,y):

    z = np.zeros_like((len(x)+len(y)))    
    
    """
    tmp = [abs(x) >  abs(y)]
    
    tmp_1 = np.where(tmp)   
    
    print("TESTING = ", tmp, tmp_1
          """
    
    
    tmp = [abs(x) > abs(y)]
    
    sliced = np.where(tmp == True)
    
    if (sliced):
        np.append(z, (np.subtract(x, y) / 2))
    else:
        np.append(z, (np.subtract(y, x) / 2))
    
    
    return z