"""
!/usr/bin/env python3
# -*- coding: utf-8 -*-

Lab 4 Part B

By Jawad Tanana
"""
import matplotlib.pyplot as plt

list_x = [] # Empty list initiation
list_y = [] # Y axis List Initiation


for i in range(2, 14, 2):
    list_x.append(i);

for cube in list_x:
    list_y.append(cube**2);


print("List X = ", list_x)
print("List Y = ", list_y)


fig1 = plt.figure() # Create the table
plt.plot(list_x, list_y, 'x') # Plot the axis which i have specified
plt.show() # This prints the actual plot out
plt.xlabel('X-axis') # Label for the X- Axis
plt.ylabel('Y-axis') # Label for the Y- Axis
fig1.savefig('part_b1.png') # Save theplot as a png
