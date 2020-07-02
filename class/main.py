import numpy as np 
import pygame
import random
from PIL import Image
from Point import *
from surface import *
import rt
import math
import threading

def especularidadTrue(point, source, seg):
    medio=Point((seg[0].x+seg[1].x)/2,(seg[0].y+seg[1].y)/2)
    nuevaFuente=Point(2*medio.x-source.x,2*medio.y-source.y)
    dir = nuevaFuente-point
    length = rt.length(dir)
    length2 = rt.length(rt.normalize(dir))
    dist = rt.raySegmentIntersect(point, dir, seg[0], seg[1])
    if  dist > 0 and length2>dist:
        return length
    return 0

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
            listSeg=[]
            free = True
            especularidad=0
            ########
            for surface in surfaces:
                x1, y1 = 0, 0
                if (surface.itsIn(point)):
                    if(surface.especularidad):
                        free = True
                    else:
                        right = source.x <= 250
                        up = source.y <= 250
                        reflexion = [random.uniform(1, 50), random.uniform(1, 20)]
                        if(right):
                            x1 = point.x + point.x*relexcion[0]/100
                        else:
                            x1 = point.x - point.x*relexcion[0]/100
                        if(up):
                            y1 = point.y + point.y*relexcion[0]/100
                        else:
                            y1 = point.y - point.y*relexcion[0]/100
                        intensity = (1-(length/100))**2
                        #print(len)
                        #intensity = max(0, min(intensity, 255))
                        values = (ref[int(y1)][int(x1)])[:3]
                        #combine color, light source and light color
                        values = values * intensity * light * 100
                    
                        #add all light sources 
                        pixel += values
            ##############
            for seg in segments:                
                #check if ray intersects with segment
                dist = rt.raySegmentIntersect(point, dir, seg[0], seg[1])
                if seg[2]==True:
                    especularidad=especularidadTrue(point, source, seg)
                #if intersection, or if intersection is closer than light source
                if  dist > 0 and length2>dist:
                    free = False
                    break
            dir = source-point
            for circle in circles:
                dist = rt.rayCircleIntersect(point, dir, circle[0], circle[1])
                dist-=circle[1]*0.0045
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
                if especularidad!=0:
                    intensity = (1-(especularidad/500))**2
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
sources = [ Point(250,300), Point(250,210)]
lineal_sources = [
                 ([Point(10, 40), Point(30, 70)])#,
                 #([Point(100, 160), Point(100, 260)])
                 ]
#light color
light = np.array([0.65, 0.65, 0.3])

#warning, point order affects intersection test!!
segments = [
            
            #([Point(180, 230), Point(330, 230)])
            ([Point(190, 230), Point(260, 230), True]),
            ([Point(100, 160), Point(100, 260), True])
            ]

circles = [
            (Point(330, 180),30)
           ]
############
surfaces = [

    (surface(Point(83,31),Point(420,165),False)),

    ]
#############
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
