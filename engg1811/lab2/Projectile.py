# -*- coding: utf-8 -*-
"""
Created on Wed Feb 17 22:37:48 2021

@author: Jawad

Computing the position of a projectile
"""
import math;

# Setting variable names 
initial_speed = 80;
initial_angle = math.pi/6;
time = 5;
gravity = 9.81;

# Math Equations to calculate the coordinates.
x_coor = initial_speed * math.cos(initial_angle) * time;
y_coor = initial_speed * math.sin(initial_angle) * time - 0.5 * gravity * time**2;

# Print the coordinates out neatly.
print("x Coordinates =", x_coor, "y Coordinates", y_coor);