#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on -- 06/04/2021--

@author: -- Jawad Tanana --

"""
# Import packages
import numpy as np
import matplotlib.pyplot as plt

# Load data and store it as a numpy array called data_sea_ice
data_sea_ice = np.loadtxt(fname="sea_ice.txt")

# Check the shape of the numpy array
print("The shape of the numpy array is: ", data_sea_ice.shape)

# The shape of the array is 35 x 25
# number of rows = number of years
# Each row has 25 elements:
# The first element is the year, followed by 24 measurements per year 
# (i.e. 1 measurement per half a month)

# Print out the first row to confirm the data format
print("The first row of data is \n", data_sea_ice[0,:])

# We need to move the years into a different variable and then remove the
# years from the first column


# first column, easy
years = data_sea_ice[:,0];

# remove the first column
data_sea_ice = np.delete(data_sea_ice, 0, axis=1) 

# i should be 35 (years) x 24 (half-monthly samples)
print("The shape of the numpy array is: ", data_sea_ice.shape) 

# The following line uses a numpy function to produce the array:
# array([0.5, 1, 1.5, 2, ..., 11.5, 12])
months = np.linspace(0.5,12,24)
# We haven't discussed linspace yet but for this lab, it is sufficient 
# for you to know what the contents of the numpy array months are
# If you want to know more about the numpy function linspace, its manual 
# page is at
#https://docs.scipy.org/doc/numpy-1.13.0/reference/generated/numpy.linspace.html#numpy.linspace

# plot the data - you should add the xlabel, ylabel, title
# You will see 35 curves, each curve depicts the variation of sea ice 
# extents in one year
# The seasonal variation should be obvious and don't forget, the data came 
# from the northern hemisphere  
# You will need to plot more figures later on, so put it in Figure 1
fig1 = plt.figure()
plt.figure(1)


plt.plot(months, np.transpose(data_sea_ice))
# This shows you how to use xticks
plt.xticks([2, 4, 6, 8, 10, 12], ["Feb", "Apr", "Jun", "Aug", "Oct", "Dec"])
fig1.savefig('numpy.png')
plt.show()


# q1
avg_sea_ice_annual = np.average(data_sea_ice, axis = 1)

# Q2
avg_sea_ice_halfmonth = np.average(data_sea_ice, axis = 0)

# Q3

avg_sea_ice = np.average(data_sea_ice)

# Q4

halfmonths_gt_avg = np.sum(data_sea_ice > avg_sea_ice, axis = 1)

# Q5

halfmonths_less_avg = np.sum(avg_sea_ice_annual < avg_sea_ice)

# Q6

last_ten = np.sum(avg_sea_ice_annual[-10:] < avg_sea_ice)


# Q7

ascending = np.argsort(avg_sea_ice_annual)
sliced = years[ascending[0:10]]



# Q8 

idk = np.ravel(data_sea_ice)
idk_row = int(len(idk)/2)
idk_col = 2
reshaped_idk = np.reshape(idk,(idk_row,idk_col))
mean_reshaped = np.mean(reshaped_idk,axis = 1)
monthly = np.reshape(mean_reshaped,(35,12))

print("1. AVG SEA ICE ANNUAL: ", avg_sea_ice_annual)
print("2. AVG SEA ICE HALF MONTH: ", avg_sea_ice_halfmonth)
print("3. AVG SEA ICE: ", avg_sea_ice)
print("4. HALF MONTHS: ", halfmonths_gt_avg)
print("5. HALF MONTHS LESS: ", halfmonths_less_avg)
print("6. LAST TEN: ", last_ten)
print("7. ASCENDING: ", sliced)
print("8. shaped: ", monthly)