#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 

@author: 
    

Purpose:
   Determining the discomfort level for a given set of suspension parameters

Inputs:
  vs    the verticle velocity of the quarter car body       
  dt    time increment 

Output:
   discomfort: a scalar representing the discomfort level for the given
   vehicle and suspension parameters
       
"""
import numpy as np

def calc_discomfort(vs , dt):
    
    # Double recursive function 
    acceleration = np.diff(vs,n=1) / dt    
    
    # Sum to make it scalar
    discomfort = np.sum(np.diff(acceleration,n=0)**2)


    #print("Acceleration = ", acceleration)
    #print("Discomfort = ", discomfort)
    
    return discomfort


