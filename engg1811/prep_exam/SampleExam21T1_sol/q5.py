#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ENGG1811 Sample Exam 

Solution to Question 5
"""
import numpy as np

def q5_func(array,n):
    # To determine the number of entries in array
    m = len(array)

    # To determine s
    s = m // n

    # Extract the first n*s elements
    array_shorten = array[0:n*s]

    # reshape the array with s rows and n columns
    array_reshaped = np.reshape(array_shorten,(s,n))

    # sum the columns
    output = np.sum(array_reshaped,axis=0)
    
    output = list(output)

    # return output
    return output
