import numpy as np 
import pygame
from time import time
import random
from PIL import Image
from Point import *
from surface import *
import rt
import math
import threading

def especularidadFalse(point, source, seg):
    medio=Point((seg[0].x+seg[1].x)/2,(seg[0].y+seg[1].y)/2)
    nuevaFuente=Point(2*medio.x-source.x,2*medio.y-source.y)
    dir = nuevaFuente-point
    length = rt.length(dir)
    length2 = rt.length(rt.normalize(dir))
    dist = rt.raySegmentIntersect(point, dir, seg[0], seg[1])
    if  dist > 0 and length2>dist:
        return length
    return 0

def rayRefraction(point, source, seg):
    distancia=point.distance(seg[0],seg[1])
    nuevaFuente=Point(source.x+(distancia*2),source.y)
    dir = nuevaFuente-point
    length = rt.length(dir)
    length2 = rt.length(rt.normalize(dir))
    dist = rt.raySegmentIntersect(point, dir, seg[0], seg[1])
    if  dist > 0 and length2>dist:
        return length
    return 0

def especularidadTrue(point, source, seg):
    #ecuacion recta punto-fuente
    m1 = (point.y-source.y)/(point.x-source.x)
    b1 = point.y - (m1*point.x)
    #ecuacion recta ambos puntos del segmento
    m2 = (seg[1].y-seg[0].y)/(seg[1].x-seg[0].x)
    b2 = seg[1].y - (m2*seg[1].x)
    #despejamos x
    x = (b2-b1)/(m1-m2)
    #buscamos la y
    y = (m1*x) + b1
    interseccion = Point(x,y)
    #distancia desde origen hasta interseccion, en eje x
    d = x-source.x
    if(d < 0):
        reflejo = Point(x+d, source.y)
    else:
        reflejo = Point(x+d, source.y)

    #ecuacion de la recta del reflejo
    m3 = (y - reflejo.y)/(x-reflejo.x)
    b3 = y - (m3*x)
        
    dir = interseccion-reflejo
    length = rt.length(dir)
    length2 = rt.length(rt.normalize(dir))
    dist = rt.raySegmentIntersect(point, dir, seg[0], seg[1])
    if  dist > 0 and length2>dist:
        #return [length, m3, b3]
        return length
    #return [0,0,0]
    return 0


def especularidadFalseCircle(point, source, circle):
    medio=circle[0]
    nuevaFuente=Point(2*medio.x-source.x,2*medio.y-source.y)
    dir = nuevaFuente-point
    length = rt.length(dir)
    length2 = rt.length(rt.normalize(dir))
    distanciaFuente=point.distance(circle[0],nuevaFuente)
    dist = rt.rayCircleIntersect(point, dir, circle[0], circle[1])
    dist-=circle[1]*distanciaFuente*0.00001
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
            especularidadF=0
            especularidadT=0
            especularidadC=0
            refraccion=0
            colorB=0
            transparencia=1
            transparenciaR=1
            
            for seg in segments:                
                #check if ray intersects with segment
                dist = rt.raySegmentIntersect(point, dir, seg[0], seg[1])
                if seg[2]==1:
                    especularidadF=especularidadFalse(point, source, seg)
                if seg[2]==2:
                    #data = especularidadTrue(point, source, seg)
                    especularidadT=especularidadTrue(point, source, seg)
                if seg[2]==4:
                    refraccion=rayRefraction(point, source, seg)
                #if intersection, or if intersection is closer than light source
                if  dist > 0 and length2>dist:
                    if seg[2]==3:
                        transparencia=3
                    else:
                        free = False
                        if seg[2]==4 and refraccion!=0:
                            free = True
                            transparenciaR=3
                            
                    break
            dir = source-point
            for circle in circles:
                #if rt.inRadio(point, circle[0], circle[1]):
                    #free = False
                    #break
                distanciaFuente=point.distance(circle[0],source)
                dist = rt.rayCircleIntersect(point, dir, circle[0], circle[1])
                dist-=circle[1]*distanciaFuente*0.00001
                if circle[2]==False:
                    especularidadC=especularidadFalseCircle(point, source, circle)
                    colorB=circle[3]
                if  dist > 0 and length2>dist:
                    free = False
                    break
                
            if free:        
                intensity = (1-(length/500))**2
                intensity/=transparencia
                intensity/=transparenciaR
                #intensity = max(0, min(intensity, 255))
                values = (ref[int(point.y)][int(point.x)])[:3]
                #combine color, light source and light color
                values = values * intensity * light
                
                #add all light sources 
                pixel += values
                if especularidadF!=0:
                    intensity = (1-(especularidadF/500))**2
                    intensity/=2
                    #print(len)
                    #intensity = max(0, min(intensity, 255))
                    values = (ref[int(point.y)][int(point.x)])[:3]
                    #combine color, light source and light color
                    values = values * intensity * light
                    
                    #add all light sources 
                    pixel += values
                if especularidadT!=0:
                    intensity = (1-(especularidadT/500))**2
                    intensity/=2
                    #print(len)
                    #intensity = max(0, min(intensity, 255))
                    values = (ref[int(point.y)][int(point.x)])[:3]
                    #combine color, light source and light color
                    values = values * intensity * light
                    
                    #add all light sources 
                    pixel += values
                if refraccion!=0:
                    intensity = (1-(refraccion/500))**2
                    intensity/=2
                    #print(len)
                    #intensity = max(0, min(intensity, 255))
                    values = (ref[int(point.y)][int(point.x)])[:3]
                    #combine color, light source and light color
                    values = values * intensity * light
                    
                    #add all light sources 
                    pixel += values
                    
                if especularidadC!=0:
                    intensity = (1-(especularidadC/500))**2
                    intensity/=2
                    #print(len)
                    #intensity = max(0, min(intensity, 255))
                    values = (ref[int(point.y)][int(point.x)])[:3]
                    #combine color, light source and light color
                    if colorB!=0:
                        intensity*=2
                        values = np.asarray(colorB) * intensity*2 * light
                    else:
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
im_file = Image.open("Fondo.png")
ref = np.array(im_file)

#light positions
sources = [ Point(190,230),
            Point(250,270),
            #Point(350,400)
            ]
lineal_sources = [
                 ([Point(10, 40), Point(30, 70)])#,
                 #([Point(100, 160), Point(100, 260)])
                 ]
#light color
light = np.array([0.85, 0.85, 0.55])

#warning, point order affects intersection test!!

#0=Ninguno
#1=Especularidad False
#2=Especularidad True
#3=Transparencia
#4=Refraccion
segments = [
            ([Point(50, 180), Point(50, 280), 1]),
            ([Point(30, 60), Point(100, 60), 2]),
            ([Point(70, 350), Point(150, 400), 3]),
            ([Point(280, 330), Point(370, 330), 4]),
            ]


            

circles = [
            (Point(330, 180),32,False,[84,121,215])
            ]
############(84,121,215)


#thread setup
t = threading.Thread(target = raytrace) # f being the function that tells how the ball should move
t.setDaemon(True) # Alternatively, you can use "t.daemon = True"
t.start()

#main loop
tiempo_inicial = time() 
while not done:
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    tiempo_final = time() 
 
                    tiempo_ejecucion = tiempo_final - tiempo_inicial
 
                    print ('El tiempo de ejecucion fue:',tiempo_ejecucion)
                    
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

