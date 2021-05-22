#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ENGG1811 Sample Exam 

Solution to Question 1b
"""

def q1b_func(a_list,m):
    output = []

    for k in range(len(a_list)):
        if max(a_list[k]) <= m:
            output.append(k)

    return output
        
