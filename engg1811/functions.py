#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

Funciton to print floats to a list

by Jawad Tanana 
"""
import math as m

num_list = [] 

test_list = []

for num in range(0,5,1):
    num_list.append(num)


for num in num_list:
    test_list.append(num)
    
for x in range(len(test_list)):
    print(test_list[x], end = " ");
    
print("\n");
