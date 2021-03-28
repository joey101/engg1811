#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on -- 28/03/2021 --

@author: -- Jawad Tanana --

"""
data_series = [-1, 2, 21, 15, -30.34, 38, 22.2, 4]
pattern =  [5, -1, 3]
idk_list = []
result = []    
# This should calculate the similarities by calling the function
# Need to slice up the list to make it equal to pattern 
start = 0
tmp = 0
end = len(pattern)
for s in range(len(data_series)):
    sliced = data_series[start:end]
    print(sliced)
    start = end
    end = start + len(pattern)
   

