#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ENGG1811 Lab

Exercise on numpy vectorisation 
"""
import numpy as np
import math as m

pos = np.array([[   1.72,   2.56],
                [   0.24,   5.67],
                [  -1.24,   5.45],
                [  -3.17,  -0.23],
                [   1.17,  -1.23],
                [   1.12,   1.08]])

ref = np.array([1.22, 1.18])
one = np.subtract(pos,ref)**2
second = np.sum(one, axis = 1)
sqrt = np.sqrt(second)
#first = np.sqrt(np.sum(np.subtract(pos,ref)**2, axis=1))


print('one', one)
print('second', second)
print('hectic ans = ', sqrt)
# number_1 = np.sqrt((np.subtract(pos,ref))**2+(np.subtract(pos,ref))**2)

#print('Hectic answer = ', first)

# The expected answer is an array with 6 elements. 
# The elements are approximately:
# [ 1.468,  4.596,  4.928 ,  4.611,  2.410,  0.141 ]


# Insert your solution below

