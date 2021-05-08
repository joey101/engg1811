#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ENGG1811 18s2 exam 

Template for Question 1b. 
"""


import numpy as np


def q1b_func(a_list,m):
    
    tmp = np.zeros(len(a_list))
    
    for i in range(len(a_list)):
        boo = i < m
        print(boo)
        if boo == True:
            tmp = a_list.append(a_list.index(a_list[i]))
        print(tmp)
              
            
            
    return tmp 