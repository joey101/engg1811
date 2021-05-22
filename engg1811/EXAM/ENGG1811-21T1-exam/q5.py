#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ENGG1811 21T1 final exam 

Template for Question 5.   
"""

import numpy as np

def q5_func(expt_data, predicted_means):   
  
    
    temp = np.zeros(len(predicted_means))
    
    
    for i in range(len(predicted_means)):
        
        temp[i] = np.mean(expt_data[i])

    difference = np.abs(temp - predicted_means)

    diff = np.argmax(difference)
    return diff