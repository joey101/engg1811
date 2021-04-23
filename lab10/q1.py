#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ENGG1811 Lab 10

Template for Question 1  
"""

def q1_func(d,h,s):
    if d <= 0 or s <= 0 or h < 0:
        return 'Invalid'
    
    time = (d/s) + (h/400)
    
    if time < 4 and h < 200:
        return 'Easy'
    elif time > 8 or h > 600  :
        return 'Hard'
    else:
        return 'Medium'