import math

class Joint2D():
    body = {}

    def __init__(self, name, coords):
        x,y = coords
        self.x = x
        self.y = y
        self.name = name

        Joint2D.body[name] = self

    def update(self, coords):
        x,y = coords
        self.x = x
        self.y = y

    def isAbove(self, other, offset=0):     return self.y < other.y     - offset
    def isBelow(self, other, offset=0):     return self.y > other.y     + offset
    def isRightOf(self, other, offset=0):   return self.x < other.x     - offset
    def isLeftOf(self, other, offset=0):    return self.x > other.x     + offset

    def isBetweenX(self, one, two): 
        return one.x < self.x < two.x or two.x < self.x < one.x
    def isBetweenY(self, one, two): 
        return one.y < self.y < two.y or two.y < self.y < one.y
    def isInside(self, one, two):
        return self.isBetweenX(one, two) and self.isBetweenY(one, two)

    def isCloseTo(self, other, prox=.025): return self.dist(other) < prox
    def isCloseToX(self, other, prox=.025): return self.distX(other) < prox
    def isCloseToY(self, other, prox=.025): return self.distY(other) < prox

    def midPointX(self, other): return (self.x + other.x)/2
    def midPointY(self, other): return (self.y + other.y)/2

    def isInline(self, one, two, offset=.025):
        areaTraiangle = abs(self.x * (one.y - two.y) + one.x * (two.y - self.y) + two.x * (self.y - one.y))
        # assert(areaTraiangle >= 0)
        return areaTraiangle <= offset


# Utils
    
    def dist(self, other):
        return math.sqrt(((self.x- other.x)**2)+((self.y-other.y)**2) )
    def distX(self, other):
        return abs(self.x - other.x)
    def distY(self, other):
        return abs(self.y - other.y)

class Joint3D(Joint2D):
    def __init__(self, name, coords3D):
        x,y,z = coords3D
        super().__init__(name, (x,y))
        self.z = z

    def isInFrontOf(self, other, offset=0): return self.z < other.z - offset
    def isBehind(self, other, offset=0): return self.z > other.z + offset

    

