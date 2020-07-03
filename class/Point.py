import math

class Point:

    x = 0.0
    y = 0.0

    def __init__(self, x, y):
        self.x = x
        self.y = y

    #suma
    def __add__(self, other):
        return Point(self.x+other.x, self.y+other.y)

    #resta
    def __sub__(self, other):
        return Point(self.x-other.x, self.y-other.y)   

    def __truediv__(self, other):
        return Point(self.x/other, self.y/other) 

    #dot product
    def dot(self, p2):
        return (self.x*p2.x) + (self.y*p2.y)

    #cross product
    def cross(self, p2):
        return (self.x*p2.y) - (self.y*p2.x)

    #toString
    def __str__(self):
        return "[ {}, {}]".format(self.x, self.y)

    def distance(self, p1,p2):
       sq1 = (p1.x-p2.x)*(p1.x-p2.x)
       sq2 = (p1.y-p2.y)*(p1.y-p2.y)
       return math.sqrt(sq1 + sq2)
