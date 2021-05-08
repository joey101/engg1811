#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ENGG1811 Lab05, Part A 

explore Lists and how they are used
Add the previos number in the list to the number before

by Jawad Tanana 
"""
import math as m

num_list = [1.5, 2.4, 6.5] # Initiating a list
cumulative_num_list = [num_list[0]] # Initiate list with the first number of 
                                    # the old list

# This for loop adds the next number to the previous number.
for num in range(len(num_list)-1):
    value = cumulative_num_list[num] + num_list[num + 1]
    cumulative_num_list.append(round(value,3)) 


print(cumulative_num_list);
