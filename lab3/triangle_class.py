# -*- coding: utf-8 -*-
"""
Created on Wed Feb 24 21:15:41 2021

Classifying triangles to their type

@author: Jawad
"""

# Specify the angles
# a = 60; b = 60; c = 60;
# a = 70; b = 70; c = 40;
# a = 40; b = 70; c = 70;
# a = 70; b = 40; c = 70; 
# a = 50; b = 70; c = 60; 


angle_a = float(input("Put the first angle: "))
angle_b = float(input("Put the second angle: "))
angle_c = float(input("Put the third angle: "))

# Classification 
if angle_a + angle_b + angle_c == 180:
    if angle_a == angle_b and angle_b == angle_c:
        print("Yeah that is an Equilateral Triangle")
    elif angle_a == angle_b or angle_b == angle_c or angle_a == angle_cc:
        print("GOOD JOB THIS IS AN Isosceles Triangle")
    else: 
        print("PFT Scalene Triangle")
else:
    print("Buddy what is that shape!")
         
