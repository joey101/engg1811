# -*- coding: utf-8 -*-
"""
Created on Wed Feb 17 22:01:34 2021

@author: Jawad

This program will compute the number of revolutions and angular position
"""

REVOLUTION_DEGREES = 360;
ANG_SPEED = 621;
TIME = 17.5;

degrees = ANG_SPEED * TIME;
no_revolution = degrees // REVOLUTION_DEGREES;
angular_degrees = degrees % REVOLUTION_DEGREES;


print(no_revolution, 'revolutions', 'and' ,angular_degrees,'angular position');