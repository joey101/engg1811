# -*- coding: utf-8 -*-
"""
Created on Tue Apr 13 10:00:38 2021

@author: Jawad
"""
import numpy as np
import sim_projectile as sim
import math as m


angle_start = 20
angle_final = 60
increment = 1
launch_array = np.arange(angle_start, angle_final + increment, increment)



print(launch_array);