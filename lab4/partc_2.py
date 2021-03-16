#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ENGG1811 Lab04, Part C 

explore the use of functions

by Jawad Tanana 
"""
import matplotlib.pyplot as plt
import math as m

# Part C: Task 1
def extension(function):
    if function <= 10:
        e = function * 5.5;
        return(e); 
    elif function <= 20:
        e = function ** 2 - 10 * function + 55;
        return(e);

# Part C: Task 2
size_step = 0.4;

step_size_formula = m.floor(20 / size_step) + 1

force_list = []
list_dud = []

for i in range(step_size_formula):
    list_dud.append(i);

for j in list_dud:
    new = j * size_step
    force_list.append(round(new,2));

print(force_list);



list_y = []
for num in force_list:
    list_y.append(extension(num))
"""
fig1 = plt.figure() # Create the table
plt.plot(force_list, list_y , 'x') # Plot the axis which i have specified

plt.show() # This prints the actual plot out


plt.xlabel('X-axis') # Label for the X- Axis
plt.ylabel('Y-axis') # Label for the Y- Axis
fig1.savefig('part_c.png') # Save theplot as a png
"""
