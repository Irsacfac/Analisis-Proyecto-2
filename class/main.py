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
    #Raytraces the scene progessively
    while True:
        #random point in the image
        point = Point(random.uniform(0, 500), random.uniform(0, 500))
        #pixel color
        pixel = 0

        for source in sources:
            #calculates direction to light source
            
            dir = source-point
            #add jitter
            #dir.x += random.uniform(0, 25)
            #dir.y += random.uniform(0, 25)

            #distance between point and light source
            length = rt.length(dir)
            #normalized distance to source
            length2 = rt.length(rt.normalize(dir))
            bandera=False
            free = True
            for seg in segments:                
                #check if ray intersects with segment
                dist = rt.raySegmentIntersect(point, dir, seg[0], seg[1])
                #if intersection, or if intersection is closer than light source
                if  dist > 0 and length2>dist:
                    free = False
                    break
            
            for circle in circles:
                dist = rt.rayCircleIntersect(point, dir, circle[0], circle[1])
                dist-=circle[1]*0.004
                if  dist > 0 and length2>dist:
                    free = False
                    break
                
            if free:        
                intensity = (1-(length/500))**2
                #print(len)
                #intensity = max(0, min(intensity, 255))
                values = (ref[int(point.y)][int(point.x)])[:3]
                #combine color, light source and light color
                values = values * intensity * light
                
                #add all light sources 
                pixel += values
            
            #average pixel value and assign
            px[int(point.x)][int(point.y)] = pixel // len(sources)
                


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
sources = [ Point(250,300), Point(250,210) ]

#light color
light = np.array([0.65, 0.65, 0.3])

#warning, point order affects intersection test!!
segments = [
            
            #([Point(180, 230), Point(330, 230)])
            ([Point(180, 230), Point(260, 230)])
            ]

circles = [
            (Point(330, 180),30)
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
