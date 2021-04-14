#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 14 11:51:38 2021

@author: bladerunner
"""
import numpy as np


data_sea_ice = np.loadtxt('/home/bladerunner/Documents/engg1811/lab9/sea_ice/sea_ice.txt')


mask = np.copy(data_sea_ice)
mask[(data_sea_ice < 9.69) & (data_sea_ice > 11.06)] = 0


print(mask)


