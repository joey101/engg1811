#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ENGG1811 18s2 exam 

Template for Question 1a. 
"""
import numpy as np
def q1a_func(a_list,a,b):
    count = 0
    for num in a_list:
        if num >= a and num < b:
            count += 1
    
            
    if count == len(a_list):
        return True
    else:
        return False