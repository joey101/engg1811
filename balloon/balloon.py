#Pygame v2.1.2
import pygame as py
import sys
import random
from math import *

# class balloon:
#     radius = 5
#     speed = 5

#     def increaseSpeed():
#         speed += 5
   
# class shooter:
#     boxH = 5
#     boxW = 10
#     bulletSpeed = balloon.speed() * 10

width = 700
height = 600
displayIndex = 0
rec = py.Rect(50,height - 100,width,100)
rec.center = (width/2,height/2)

# Set up the drawing window
DISPLAYS = [(1024,576),(1152,648),(1280,720),(1600,900),(1920,1080),(2560,1440)] 
screen = py.display.set_mode(DISPLAYS[displayIndex])
py.display.set_caption("Shoot away")

# Run until the user asks to quit
running = True

while running:
    # Did the user click the window close button?
    for event in py.event.get():
        if event.type == py.QUIT:
            running = False

    # Fill the background with white
    screen.fill((114,114,114))

    py.draw.rect(screen,(250,100,100),rec,4)
    py.display.flip()

# Done! Time to quit.
py.quit()
