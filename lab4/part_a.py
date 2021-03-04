#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ENGG1811 Lab04, Part A 

explore the use of functions

by Jawad Tanana 
"""
import math as m;

# Task 1: Write the function for calculating H(z,a) 
"""def proportion(z,a):
    return z / (z + a)

prop = proportion(7,1)
print(prop)
"""
# Task 2: 
# Defining the function and associating it with its formula
def two_proportion(x,b,y,c) :
    second = x / (x + b)
    third = c / (c + y)
    first = second * third
    return first, second, third;

r1, r2, r3 = two_proportion(2,6,5,35);

print(r1, r2, r3);

# two_proportions(2,6,5,35) gives 0.21875, 0.25, 0.875
# two_proportions(5,2,2.7,6.3) gives 
# 0.5, 0.7142857142857143, 0.7
# two_proportions(2.5,5.2,1.7,0.7) gives 
# 0.0946969696969697, 0.3246753246753247, 0.2916666666666667
