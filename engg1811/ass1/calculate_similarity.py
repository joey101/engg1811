#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on --17-03-2021--

@author: -- Jawad Tanana z5320158--

This program is meant to return a similarity value. 
"""
def calculate_similarity(data_segment, pattern):
    # Tests the lengths of the segment with the pattern to proceed.
    if len(data_segment) != len(pattern):
        return "Error"

    # Initialise a variable with 0.0 to accept float numbers as specified
    # in the specs.
    ret = 0.0 
   
    # This loop will integrate the algorithm supplied in the specs sheet.
    for i in range(len(pattern)):
        ret += data_segment[i] * pattern[i]
        
    return ret
    
    """ Calculate the similarity between one data segment and the pattern.

    Parameters
    ----------
    data_segment : [float]
        A list of float values to compare against the pattern.

    pattern : [float]
        A list of float values representing the pattern. 

    Returns
    -------
    float
        The similarity score/value.
        
    "Error"
        If data segment and pattern are not the same length.

    """
