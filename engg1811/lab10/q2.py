#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ENGG1811 Lab 10

Template file for Question 2 
"""
# Import numpy
import numpy as np 

def q2_func(x,y):

     
    length = len(x)
    z = np.zeros(length)
    booalean = abs(x) > abs(y)
    not_booalean = ~booalean

    z[booalean] = x[booalean] - y[booalean] / 2

    z[not_booalean] = y[not_booalean] - x[not_booalean] /2
    
    """
        if (abs(x[i]) > abs(y[i])):
            z[i] = x[i] - y[i] / 2
        else:
            z[i] = y[i] - x[i]/2
    """
    
    return z