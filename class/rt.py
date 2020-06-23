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
    #v1 vevctor que va del origen al centro del circulo
    v1 = c - ori
    #se proyecta sobre el vector de direccion
    #para obtener el punto mas cercano al centro del circulo
    R = v1.dot(dir)/(length(dir)*length(dir))
    closest = Point(R*dir.x, R*dir.y) + ori

    #calculamos b como la distancia desde el centro al punto mas cercano
    b = length(c - closest)
    #ai b es mayor que el radio, no hay interseccion
    if b > r:
        return -1.0
    #obtenemos h usando pitagoras
    h = math.sqrt(r*r - b*b)
    #el vector cruza el circulo en 2 distancias: R-h y R+h
    return (R-h, R+h)

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
