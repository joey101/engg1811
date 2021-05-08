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
mass = 0.145
c = 0.0013
v0 = 50
landing_level = 10


launch_angle = np.arange(angle_start, angle_final + increment/2, increment)

time_array = np.arange(0,10,0.01)
landing_times = np.zeros_like(launch_angle, dtype = 'float')
landing_distance = np.zeros_like(launch_angle, dtype = 'float')


print('launch angle =', launch_angle)
print('time = ', time_array)
print('before landing values = ', landing_distance)
print('before landing times = ',landing_times)




for angle in range(len(launch_angle)):
    position_x,position_y = sim.sim_projectile(time_array,mass,c,v0,launch_angle[angle])
    pos, time = sim.find_landing_pos_time(time_array,position_x,position_y,landing_level)
    landing_distance[angle] = landing_distance[angle] + pos
    landing_times[angle] = landing_times[angle] + time


optimal_angle = np.min(np.where(landing_distance >= 90))
optimal_where = launch_angle[optimal_angle]
time_loc = landing_times[optimal_angle]


print('land = ', landing_distance)
print('time = ', landing_times)
print('launch optimal angle = ', optimal_angle)
print('optimal_where = ', optimal_where)
print('optimal time = ', time_loc)

plt.figure(1)
plt.plot(landing_times, landing_distance)
plt.grid()
plt.xlabel('Landing Time')
plt.ylabel('Landing Position')
plt.title('Position of the strawberry')
plt.show()

