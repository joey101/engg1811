#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Task 2: What does * and + do to a list

By Jawad Tanana

z5320158
"""
import matplotlib.pyplot as plt
"""
idk = [1, 2] * 4;

print(idk);

# * this operator multiplies what is inside the list four
# times.

idk_2 = [10] + [23, 15, 66] + [-3, -5]
print(idk_2);

# + operator adds the components into the list
"""
# Task 3:

list_hor = [];
list_ver = [3] * 8;

for i in range(8):
    list_hor.append(i);


print(list_hor);
print(list_ver);

fig1 = plt.figure() # Create the table
plt.plot(list_hor, list_ver, 'x') # Plot the axis which i have specified

plt.show() # This prints the actual plot out


plt.xlabel('X-axis') # Label for the X- Axis
plt.ylabel('Y-axis') # Label for the Y- Axis
fig1.savefig('part_b2.png') # Save theplot as a png
