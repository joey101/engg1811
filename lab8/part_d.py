# -*- coding: utf-8 -*-
"""
Created on Tue Apr 13 10:00:38 2021

@author: Jawad
"""
import numpy as np
import sim_projectile as sim
import math as m
import matplotlib.pyplot as plt

angle_start = 20
angle_final = 60
increment = 1
landing_height = 10
mass = 0.145
c = 0.0013
v0 = 50
landing_level = 10


launch_angle = np.arange(angle_start, angle_final + increment, increment)

time_array = np.arange(0,10,0.1)
landing_times = np.zeros_like(launch_angle, dtype = 'float')
landing_distance = np.zeros_like(launch_angle, dtype = 'float')

for angle in launch_angle:
    position_x,position_y = sim.sim_projectile(time_array,mass,c,v0,angle)
    pos, time = sim.find_landing_pos_time(time_array,position_x,position_y,landing_level)
    landing_distance = np.append(landing_distance, pos)
    landing_times = np.append(landing_times, time)

    
plt.figure(1)
plt.plot(landing_times, landing_distance)
plt.grid()
plt.xlabel('Landing Time')
plt.ylabel('Landing Position')
plt.title('Position of the strawberry')
plt.show()

