# -*- coding: utf-8 -*-
"""
Created on Mon Apr 12 22:36:47 2021

@author: Jawad
"""
import numpy as np

tv = np.array([0.6, 0.7, 1.5, 1.6, 1.7, 1.8, 1.9])
px = np.array([2.4, 2.9, 5.7, 6.6, 7.5, 8.4, 9.3])
py = np.array([9.7, 10.1, 10.5, 10.2, 10.1, 9.9, 9.8])

just_before = np.max(np.where(py >= 10))



print(just_before)
