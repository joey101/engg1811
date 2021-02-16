# -*- coding: utf-8 -*-
"""
Created on Thu Feb 11 20:54:04 2021

@author": Jawad
"""
time = 1000000;

years = (time // (24 * 60)) // 365;
days = years // (24 * 60);
hours = days // 24;
minutes = hours // 60 ;
print(years, 'years', days ,'days', hours, 'hours', 'and', minutes, 'minutes');
