#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on -- 28/03/2021 --

@author: -- Jawad Tanana --

"""
import calculate_similarity as cal

def calculate_similarity_list(data_series, pattern): 
    idk_list = []
    
    # This should calculate the similarities by calling the function
    # Need to slice up the list to make it equal to pattern 
    start = 0
    end = len(pattern)
    for s in range(len(data_series)):
        sliced = data_series[s:end]
        idk = cal.calculate_similarity(sliced, pattern)
        idk_list.append(idk)
        end = s + len(pattern)
    """ 
    data_series[1] * pattern[0] + data_series[2] * pattern[1] + 
    data_series[3] * pattern[2] + data_series[4] * pattern[3] 
    
    
    Calculate the similarity measures between all possible data segments
    and the pattern.

    The function calculates the similarity measures, using the 
    function 'calculate_similarity', of all possible data segments in a 
    data_series against a given pattern and returns the list of calculated 
    similarity values.

    Parameters
    ----------
    data_series : [float]
        A list of float values representing a data series. 
        
    pattern : [float]
        A list of float values representing the pattern. 

    Returns
    -------
        List of floats
            The list of calculated similarity values.

    """

