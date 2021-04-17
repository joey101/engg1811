# -*- coding: utf-8 -*-
"""
Created on Fri Apr 16 20:01:24 2021

@author: Jawad
"""
import timeit as t



test_cases = int(input("test = "))
count = 0
walls = 0
for i in range(test_cases):
    no_beds, limit = input().split()
    layout = input()
    for k in range(len(layout)-1):
        if layout[k+1] == len(layout) :
            break
        if layout[k] == '1':
            count += 1
            if count == limit and layout[k+1] == '0':
                walls += 1
        elif count == limit and layout[k+1] == '0':
            walls += 1
        elif count == limit and layout[k+1] == '1':
            count = 0
            walls += 1
    if walls == 0:
        walls = -1
        print('OUtput = ', walls)
    print("output = ", walls)

print('Expected Output = 3')
print(t.timeit())
