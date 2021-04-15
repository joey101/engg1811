#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jul 27 08:38:08 2019

@author:  

Purpose: To simulate a quarter car based on the 
         model described in the assignment

Inputs:
   time   time_array
   y_road  an array of road heights
   ms     the mass of 1/4 of the car body
   mu     the mass of the tyre and wheel
   kt     tyre stiffness
   k      spring stiffness
   b      inertance
   c      damping coefficient

Outputs:
  ys     the verticle displacement of the center of the car body 
         from a reference level
  yu     the verticle displacement of the center of the wheel/tyre 
         from a reference level
  vs     the verticle velocity of the quarter car body       
  vu     the verticle velocity of the wheel/tyre
    
    
"""    

import numpy as np 
   

def simulate_qc(time_array, y_road, ms, mu, kt, k, b, c) : 

    # Calculate time increment (dt)
    dt = time_array[1] - time_array[0]
    
    f = np.zeros_like(time_array)
    h = np.zeros_like(time_array)
    
    ys = np.zeros_like(time_array)
    yu = np.zeros_like(time_array)
    vs = np.zeros_like(time_array)
    vu = np.zeros_like(time_array)
    
    for time in range(len(time_array) - 1):
        f[time] = c * vs[time] - c * vu[time] + k * ys[time] - k * yu[time]
        h[time] = f[time] - kt * yu[time] + kt * y_road[time]        
        
        
        ys[time + 1] = ys[time] + vs[time] * dt 
        yu[time + 1] = yu[time] + vu[time] * dt
        vs[time + 1] = vs[time] + (((-(mu+b) * f[time] + b * h[time])) / \
                       (ms * mu + (ms + mu) * b)) * dt
        vu[time + 1] = vu[time] + (((-b * f[time] + (ms + b) * h[time])) / \
                       (ms * mu + (ms + mu) * b)) * dt
        
    return ys, yu, vs, vu 
    
 

