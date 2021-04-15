=#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ENGG1811, Lab 05, Part C. File for students

Date: 14/08/18
"""
# #############  DO NOT CHANGE THIS PART ########
# %% Import file
import matplotlib.pyplot as plt


# %% 
# ########### DO NOT CHANGE THIS CELL ############
# Load data and convert to float
# load the file that contains the sampling instants
# create a list of time instants
with open('time_data_complete.txt') as f:
    time_str_list = f.read().splitlines()

# load file the contains the voltage measurements
# create a list of voltage values
with open('voltage_data_complete.txt') as f:
    voltage_str_list = f.read().splitlines()

# convert to elements in the list to float data type
time_list = [float(t) for t in time_str_list]
voltage_list = [float(v) for v in voltage_str_list]

# Plot a graph of the data
fig1 = plt.figure()         # create a new figure
plt.plot(time_list,voltage_list, '--x')
plt.xlabel('time [s]')    # label for x-axis
plt.ylabel('voltage [V]')   # label for y-axis
plt.title('Pulse oximeter data')  # title of the graph
plt.grid()  # display the grid
plt.show()  # to display the graph

# ########### DO NOT CHANGE THIS CELL ############


# %% Your solution
########### PUT YOUR SOLUTION BELOW ###########

