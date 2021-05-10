#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ENGG1811 Sample Exam 

Solution to Question 4
"""
# Import numpy
import numpy as np

def q4_func(x,t):
    # Create z
    z = np.zeros_like(x)

    # Fill in the elements of z
    # Case 1: > t
    z[x > t] = 1
    # Case 2: < t
    z[x < -t] = -1
    # Case 3: in the interval [-t,t]
    z[(x <= t) & (x >= -t)] = x[(x <= t) & (x >= -t)] / t

    # return z
    return z 
