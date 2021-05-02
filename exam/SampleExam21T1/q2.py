#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ENGG1811 Lab

Data analysis on sea ice (Part 2)
"""

# %% Import packages
import numpy as np
import matplotlib.pyplot as plt 

# %% Preliminary processing 
# Load data and store it as a numpy array called data_sea_ice
data_sea_ice = np.loadtxt('sea_ice.txt')

# Extract information on year from data_sea_ice
years = data_sea_ice[:,0];   # first column
years = years.astype(int)    # change data type to int
data_sea_ice = np.delete(data_sea_ice,0,axis=1)   # remove the first column 

# Array on months 
months = np.linspace(0.5,12,24)

# The sea ice data began in year 1979 and lasted until 2013 (35 years)
# There are 24 half-monthly measurements per year

# years is the numpy array [1979, 1980, ..., 2013]
# months is the numpy array [0.5, 1, 1.5, ..., 12]
# data_sea_ice is a numpy array of shape (35,24) containing 
# sea ice extent 

"""
 ****************************
 Please insert your code below 

 Notes:
   * If required, you can add more numpy statements.
   * You must not use a loop(s) for to answer the following three tasks.
   * There are no test files for this question.
"""

######   Task-1 ######   
'''
Task-1: Calculate and save the average sea ice extent over the entire 
data collection in the variable ans_task1 in the file q2.py (provided).
'''


ans_task1 = 



######   Task-2 ######   
'''
Task-2: For each year, determine the number of half-months that exceeds 
the overall average calculated in the variable ans_task1 (during Task-1), 
and save your answer in the variable ans_task2 in the file q2.py (provided).
'''

ans_task2 = 



######   Task-3 ######   
'''
Task-3: Compute the mean sea ice extend in the first 6 months of 
years 2000-2009 (inclusive), and save your answer in the variable 
ans_task3 in the file q2.py (provided).
'''

ans_task3 = 


################   End of the program  ################   

