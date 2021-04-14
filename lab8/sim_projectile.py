#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ENGG1811 Lab

Exercise on simulation
"""
import numpy as np 
import math

def sim_projectile(time_array,m,c,v0,theta0d): 
    """
    Purpose: To simulate a projectile given its mass (m), 
             drag coefficient (c), initial velocity v0 and
             its projectile angle theta0d in degrees

           
     Inputs: 
       time_array  (numpy array) time instants
       m           mass
       c           drag coefficient
       v0          initial total speed
       theta0d     initial launch angle in degrees 
    
     Outputs:
       position_x   (numpy array) x-coordinates 
       position_y   (numpy array) y-coordinates 
        
     Variable definitions:
     
     Simulation parameters:
       dt              time increment for time array
       len_time_array  number of time instants 
       velocity_x      (numpy array)  x-velocity
       velocity_y      (numpy array)  y-velocity 
    
    """
    # Constants 
    # Physical constants 
    g = 9.81   # acceleration due to gravity 
    
    # Extract information from time vector 
    len_time_array = len(time_array)  # number of time points
    dt = time_array[1]-time_array[0]  # time increment 
    
    # Initialise storage for positions and velocities
    position_x = np.zeros_like(time_array)
    velocity_x = np.zeros_like(time_array)
    position_y = np.zeros_like(time_array)
    velocity_y = np.zeros_like(time_array)
    
    # initialise velocity at zero time 
    velocity_x[0] = v0*math.cos(math.radians(theta0d));
    velocity_y[0] = v0*math.sin(math.radians(theta0d));
    # initial position is assumed to be (0,0)
    
    # the simulation loop
    for k in range(len_time_array-1): 
        # Update x-position
        position_x[k+1] = position_x[k] + velocity_x[k] * dt;   
        # Update y-position
        # Insert your Python code here 
        position_y[k+1] = position_y[k] + velocity_y[k] * dt; 
        
        
        # Compute total speed 
        speed_total = math.sqrt(velocity_x[k]**2+velocity_y[k]**2);
        # Update x-velocity
        velocity_x[k+1] = velocity_x[k] - c*speed_total*velocity_x[k]/m*dt; 
        # Update y-velocity
        # Insert your Python code here       
        velocity_y[k+1] = velocity_y[k] - ((c/m)*speed_total*velocity_y[k]+g)*dt;
        
        
  
    return position_x, position_y 


def find_landing_pos_time(time_array,position_x,position_y,landing_level):
    """
    Purpose: To determine the landing position and landing time 
            for a given landing level
     
     Inputs:
           time_array     (numpy array)  time 
           position_x     (numpy array)  x-coordinates 
           position_y     (numpy array)  y-coordinates  
           landing_level  desired landing level 
     
     Outputs:
           landing_position    The landing position is the x-coordinate at
                               the point where the y-coordinate is just
                               greater than the landing level and is falling
                               down
           landing_time        time at the landing_position 

    We use the last position which is just greater than landing level  
    """
    # Insert your Python code here 
    where_height = np.max(np.where(position_y >= landing_level))
    landing_position = position_x[where_height]
    landing_time = time_array[where_height]

    return landing_position,landing_time