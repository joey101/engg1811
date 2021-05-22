#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ENGG1811 21T1 exam 

Template for Question 1. 
"""


def   q1_funct (a_list):
    second = []
    
    for num in a_list:
        if num > 0:
            second.append(num) 
    
    if not second:
        return 0
    return min(second)
    
  