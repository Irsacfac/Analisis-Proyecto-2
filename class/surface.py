from Point import *

class surface:

    a = None
    b = None
    especularidad = False

    def __init__(self, a, b, esp):
        self.a = a
        self.b = b
        self.especularidad = esp

    #verifica si el punto esta dentro o fuera
    def itsIn(self, p2):
        if((self.a.x < p2.x) and (p2.x < self.b.x) and (self.a.y < p2.y) and (p2.y < self.b.y)):
            return True
        return False
    
