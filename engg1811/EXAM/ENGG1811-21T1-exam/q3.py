#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ENGG1811 Exam

Template file for Question 3
"""

def   q3_funct (t1, t2):
    
    alert = t1 + t2
    if alert > 200:
        if t1 >= 150 or t2 >=150:
            return "alertHigh"
        else:
            return "alertLow"
    elif t1 < 50 and t2 < 50:
        return "normalLow"
    else: 
        return "normalHigh"
    
