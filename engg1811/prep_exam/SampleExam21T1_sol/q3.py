#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ENGG1811 Sample Exam 

Solution to Question 3
"""

def q3_func(m,h):
    # Compute the bmi
    bmi = m / h**2

    # Classification
    if bmi < 18.5:
        return 'Underweight'
    elif bmi < 25:
        return 'Healthy'
    elif bmi < 30:
        return 'Overweight'
    else:
        return 'Obese'
