#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ENGG1811 18s2 exam 

Template for Question 1b. 
"""

def q1b_func(a_list,m):
    output = []
    
    for num in range(len(a_list)):
        largest = max(a_list[num])
        #print("0. ",largest)
        if largest <= m:
            #print(m)
            index = a_list.index(a_list[num])
            #print("1. ", index)
            output.append(index)
            #print("2. ", output)
    return output