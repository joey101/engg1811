#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ENGG1811 Lab03 Part C

Determining where you are in the atmosphere

By Jawad Tanana

z5320158
"""
TROPO = 17;
SIXTY = 60;

altitude = float(input("Please type in an altitude number: "));

# First if tests whether you are on Earth or underground
if altitude < 0:
    print("You are underground buddy");
   
elif altitude > 120:
    print("You are in space buddy");

# Tests where you are within the Atmosphere
else: 
    if altitude <= TROPO:
        print("You are in the Troposphere");

    elif altitude <= SIXTY:
        print("You are in the Stratosphere");

    elif SIXTY < altitude <= 120:
        print("You are in the Mesosphere");
