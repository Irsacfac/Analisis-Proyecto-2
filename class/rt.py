from Point import *
import math

def raySegmentIntersect(ori, dir, p1, p2):

    #calculate vectors
    #calcular vectores
    v1 = ori - p1
    v2 = p2 - p1
    v3 = Point(-dir.y, dir.x)

    #dot product v2 y v3
    dot = v2.dot(v3)
    if (abs(dot) < 0.000001):
        return -1.0

    t1 = v2.cross(v1) / dot
    t2 = v1.dot(v3) / dot

    if (t1 >= 0.0 and (t2 >= 0.0 and t2 <= 1.0)):
        return t1

    return -1.0


def rayCircleIntersect(ori, dir, c, r):
    #v1 vector que va del origen al centro del circulo
    v1 = c - ori
    #se proyecta sobre el vector de direccion
    #para obtener el punto mas cercano al centro del circulo
    R = v1.dot(dir)/(length(dir)*length(dir))
    closest = Point(R*dir.x, R*dir.y) + ori

    #calculamos b como la distancia desde el centro al punto mas cercano
    b = length(c - closest)
    #print("B es: ")
    #print(b)
    #print("R es: ")
    #print(r)
    #ai b es mayor que el radio, no hay interseccion
    if b > r:
        return -1.0
    #obtenemos h usando pitagoras
    h = math.sqrt(r*r - b*b)
    #el vector cruza el circulo en 2 distancias: R-h y R+h
    return R
    #return (R-h, R+h)

def segCircleIntersect(ori, dir, p, c, r):
    #calculamos la pendiente
    m = (ori.y - p.y)/(ori.x - p.x)
    #ecuacion de segundo grado
    a =  1 + m*m
    b = (-2)*(c.x - m*p.y + m*m*p.x + c.y*m)
    c1 = c.x*c.x + p.y*p.y - 2*p.y*(m*p.x + c.y) + m*m*p.x*p.x + 2*c.y*m*p.x + c.y*c.y - r*r
    return b*b - 4*a*c1

def inRadio(p, c, r):
    x = p.x - c.x
    y = p.y - c.y
    return r == math.sqrt(x*x + y*y)

#largo de un segmento
def length(v1):
    #assumes v1 starts at (0,0)
    return math.sqrt(v1.x*v1.x + v1.y*v1.y)

#normalizacion
def normalize(v1):
    #assumes v1 starts at (0,0)
    v1 = v1 / length(v1)
    return v1

#interseccion punto
def intersectionPoint(ori, dir, dist):
    x = ori.x + dir.x*dist
    y = ori.y + dir.y*dist

    return Point(x,y)

#angulo coseno
def cosAngle(a, b, ori):
    #returns the cosine of the angle of 2 vectors that part from ori

    v1 = ori - a
    v2 = ori - b

    cos = v1.dot(v2)/(length(v1)*length(v2))
    return cos
