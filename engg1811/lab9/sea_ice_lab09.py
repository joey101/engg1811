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
data_sea_ice = np.loadtxt('/home/bladerunner/Documents/engg1811/lab9/sea_ice/sea_ice.txt')

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

# plot the data 
plt.figure(1)
plt.plot(months,np.transpose(data_sea_ice))
plt.xlabel("Months")
plt.xticks([2,4,6,8,10,12],["Feb","Apr","Jun","Aug","Oct","Dec"])
plt.ylabel("Sea ice extent")
plt.grid()
plt.show()

# %% ****************************
# Please insert your code below
# Part 1

sliced_year = [(years >= 1987) & (years <= 1999)]
var = data_sea_ice[sliced_year]
ans_1 = np.average(var)
print('1.', ans_1)

# %%
# Part 2

three_months = data_sea_ice[:,-6:]
shape_three = np.shape(three_months)
# print(shape_three)
# print(three_months)
print('2.', np.average(three_months))
# %%
# Part 3
sliced_idk = (years >= 2000) & (years <= 2009)
sliced_month = (months<=6)
ans_3 = np.average(data_sea_ice[np.ix_(sliced_idk,sliced_month)])
print('3. ', ans_3)
# %%
# Part 4
half_months = data_sea_ice[::,0::2]
end_months = data_sea_ice[::,1::2]
# print(np.shape(half_months))
# print(np.shape(end_months))

combined_months = (half_months + end_months) / 2
# print('Months = ', months)
# print('Half months = ', half_months)
# print('End months = ', end_months)
print('4. Months = ', combined_months[0,0:3])
# print('Shape = ', np.shape(combined_months)) 

# %%
# Part 5

straightened = np.ravel(data_sea_ice)
difference = np.abs(np.min(np.diff(data_sea_ice)))
# print(straightened)
# print(np.shape(straightened))
print('5. Biggest Decrease = ', difference)
# print(np.shape(difference))


# %%

# Part 6 
peak = np.argmax(data_sea_ice, axis=1)
peak_unique,counts = np.unique(peak,return_counts=True)
high_months = months[peak_unique[np.argmax(counts)]]
print('6. Highest Half Month = ', high_months)










