#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ENGG1811 Sample Exam 

Solution to Question 1a
"""

def q1a_func(a_list,a,b):
        
        bool_list = []
        
        for entry in a_list:
            if entry >=a and  entry <b:
                bool_list.append(True)
            else:
                bool_list.append(False)
                
        return all(bool_list)


""" 
# Solution without using the all() function

def q1a_func(a_list,a,b):
        
        final_boolean=True
        
        for entry in a_list:
            if entry >=a and  entry <b:
                final_boolean= final_boolean and True
            else:
                final_boolean= final_boolean and False
                
        return final_boolean
"""        
