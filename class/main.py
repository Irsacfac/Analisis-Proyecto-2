import numpy as np 
import pygame
import random
from PIL import Image
from Point import *
from surface import *
import rt
import math
import threading


def raytrace():
    pixel = 0


def getFrame():
    return px




#pygame stuff
h,w=550,550
border=50
pygame.init()
screen = pygame.display.set_mode((w+(2*border), h+(2*border)))
pygame.display.set_caption("Proyecto 2")
done = False
clock = pygame.time.Clock()

#init random
random.seed()

#image setup
i = Image.new("RGB", (500, 500), (0, 0, 0) )
px = np.array(i)

#reference image for background color
im_file = Image.open("Fondo.jpg")
ref = np.array(im_file)

#light positions
sources = [ Point(250,250), Point(250,210) ]

#light color
light = np.array([0.65, 0.65, 0.3])

#warning, point order affects intersection test!!
segments = [
            
            #([Point(180, 230), Point(330, 230)])
            ([Point(240, 230), Point(330, 230)])
    
            ]


#thread setup
t = threading.Thread(target = raytrace) # f being the function that tells how the ball should move
t.setDaemon(True) # Alternatively, you can use "t.daemon = True"
t.start()

#main loop
while not done:
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done = True

        # Clear screen to white before drawing 
        screen.fill((255, 255, 255))

        # Get a numpy array to display from the simulation
        npimage=getFrame()

        # Convert to a surface and splat onto screen offset by border width and height
        surface = pygame.surfarray.make_surface(npimage)
        screen.blit(surface, (border, border))

        pygame.display.flip()
        clock.tick(60)
