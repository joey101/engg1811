#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on --30/04/2021--

@author: -- Jawad Tanana --

"""

def pattern_search_multiple(data_values, pattern_width, threshold):
    """ Searches the data_values for all the values that satisfy the criteria
        mentioned below and in the assignment specification document.
        The function returns the indices of these values.

    Parameters
    ----------
    data_values : [float]
        A list of float values representing similarity measures. You are looking
        for instances of the pattern inside this data_values.

    pattern_width : [float]
        A float value. The length/width of the pattern.

    threshold : [float]
        A float value. Selected similarity measure needs to be greater than or
        equal to the given threshold value.

    Returns
    -------

    One of the three possible outcomes: 
        - "Insufficient data", 
        - "Not detected" or 
        -  a list of non overlapping indices that are greater than or 
           equal to the given threshold value, and that satisfy the following criteria:
               - an index is not selected if the value at the index is less than a value 
                 at one of it's overlapping indices.
               - an index is not selected if it is overlapping with first or last index.
           Overlapping indices: We say two indices are overlapping if the distance 
           between them is less than the width of the pattern.

    """

    # TODO: Insert your code here.
