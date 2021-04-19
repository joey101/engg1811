#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 

@author: 
    

Purpose:
   Determining the discomfort levels for a given damper values and inerter values

Inputs:
   time   time_array
   y_road  an array of road heights
   ms     the mass of 1/4 of the car body
   mu     the mass of the tyre and wheel
   kt     tyre stiffness
   k      spring stiffness
   inerter_values              inertance values (array of type float)
   damping_coefficient_values  damping coefficient values (array of type float)

Output:
   discomfort_array   2-dimentional numpy array with discomfort values for 
                      given damper values and inerter values (read the specs)
   
"""

import numpy as np
import calc_discomfort as cd
import simulate_qc as sqc


def explore_qc(time_array, y_road, ms, mu, kt, k, 
               inerter_array, damping_coefficient_array):
    
    # Calculate time increment (dt)
    dt = time_array[1] - time_array[0]   
    
    # Created 2-D array of the lengths inerter array (row) and damping 
    # coefficient (column) filled with zero.
    discomfort_levels = np.zeros((len(inerter_array),\
                                 len(damping_coefficient_array)))
    
    # Loop first time through rows    
    for i in range(len(inerter_array)):
        # Loop through the columns
        for j in range(len(damping_coefficient_array)):
            # Get values needed for discomfort function
            # Back Slash is to make it within 80 border.            
            ys, yu, vs, vu = sqc.simulate_qc(time_array,y_road,ms,mu,kt,k,\
                                             inerter_array[i],\
                                                 damping_coefficient_array[j])

            # Fill 2-D array with values calculated for discomfort.
            discomfort_levels[i][j] = cd.calc_discomfort(vs, dt)
            
    
    # print('inerter', inerter_array, 'damping_co', damping_coefficient_array)
    # print('discomfort = ', discomfortLevels, np.shape(discomfortLevels))
    
    return discomfort_levels 

