#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on -- 29/03/2021 --

@author: -- Jawad Tanana --

The purpose of this code is to find the maximum similarity value indexing
that are over the threshold.
"""
import calculate_similarity_list as calc

def pattern_search_max(data_series, pattern, threshold):
    # The set of if statements assess the three conditions given in the 
    # spec sheet.
    if len(data_series) < len(pattern):
        return "Insufficient data"
    elif threshold > max(data_series):
        return "Not detected"
    else:
        # Returns the list of similar values and assign to a list
        # sim_list
        sim_list = calc.calculate_similarity_list(data_series, pattern)
        # Return the index of the highest value in the ans list
        # and assign to a variabel called highest simialrity.
        highest_sim = ans.index(max(sim_list))
    return highest_sim   
    """ Search for the highest similarity measure that is also greater than
        or equal to the given threshold value and returns the index of that
        value.

        The function finds the index of the highest similarity value,
        using the similarity_list returned by the function
        'calculate_similarity_list'.

    Parameters
    ----------
    data_series : [float]
        A list of float values representing a data series.

    pattern : [float]
        A list of float values representing the pattern.

    threshold : [float]
        A float value. Selected similarity measure needs to be greater than or
        equal to the given threshold value.

    Returns
    -------
    "Insufficient data" : [String]
        If the given data_series is shorter than the given pattern.

    "Not detected" : [String]
        If all the similarity measures are (strictly) less than the given
        threshold value.

    integer
        Index of the highest similarity measure that is also greater than
        or equal to the given threshold value.
    """

    # TODO: Insert your code here.
