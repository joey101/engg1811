#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ENGG1811 21T1 final exam 

Template for Question 2. 
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

"""
The sea ice data began in year 1979 and lasted until 2013 (35 years)
There are 24 half-monthly measurements per year

years is the numpy array [1979, 1980, ..., 2013]

months is the numpy array [0.5, 1, 1.5, ..., 12]. 
where, 
  the first column (0.5) represents first half-month measurements of January, 
  the second column (1) represents second half-month measurements of January, 
  the third column (1.5) represents first half-month measurements of February, 
  and so on.

data_sea_ice is a numpy array of shape (35,24) containing sea ice extent. 
"""

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
Task-1 (4 marks): Calculate and save the number of sea ice extent 
over the entire data collection that is between two values 
10 and 12 (inclusive) in the variable ans_task1.
'''

sliced = (data_sea_ice >= 10) & (data_sea_ice <= 12)
ans_task1 = data_sea_ice[sliced]
# print(ans_task1)


######   Task-2 ######   
'''
Task-2 (8 marks): For each half month from the start of March to 
the end of July (inclusive), and for every year before 1985 or after 2010, 
calculate the total number of sea ice extent that is less than 12 and 
save your answer in the variable ans_task2.
'''

#defined constants
march = 5
july = 14
b4_2010 = -4
ninteen = 5
threshold = 12

before_1985 = data_sea_ice[:ninteen:,march:july:] 
after_2010 = data_sea_ice[b4_2010::,march:july] 


combine_1 = np.sum(before_1985 < threshold)
combine_2 = np.sum(after_2010 < threshold)
combined_3 = combine_1+combine_2


ans_task2 = np.sum(data_sea_ice[combined_3])



######   Task-3 ######   
'''
Task-3 (8 marks): For every year between 1990 and 2000 (inclusive), 
calculate quarterly sea ice extent and arrange the years such that 
their corresponding third quarterly sea ice extents are sorted in 
ascending order. That is, the first year in the list is the year that 
has the lowest third quarterly sea ice extent, the second year has 
the second lowest third quarterly sea ice extent and so on. Save your 
answer in the variable ans_task3.

The expected answer for Task-3 is provided below.

For Task-3, first quarter includes months Jan, February, and March; 
second quarter includes months April, May, and June; 
third quarter includes months July, August, and September; 
fourth quarter includes months October, November, and December.
'''



#every four months
sliced_1 = data_sea_ice[11:22:,12:18:] 

print(sliced_1)
comb = np.sum(sliced_1,axis=1)
ascending = np.argsort(comb,axis=0)

#print(combined_months)
print(comb)
print(ascending)
ravel = np.ravel(years)
ans_task3 = ravel[ascending] 

print(np.shape(years))
print(ans_task3)

'''
Expected answer for Task-3, ans_task3 should be:
array([1995, 1990, 1999, 2000, 1993, 1997, 1998, 1991, 1994, 1992, 1996])
'''
################   End of the program  ################   

