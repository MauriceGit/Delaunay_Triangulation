import math
import numpy as np
import copy

# http://totologic.blogspot.de/2014/01/accurate-point-in-triangle-test.html
def pointInTriangle(p, t):
    x  = p[0]
    y  = p[1]
    x1 = t[0][0]
    y1 = t[0][1]
    x2 = t[1][0]
    y2 = t[1][1]
    x3 = t[2][0]
    y3 = t[2][1]
    
    a = ((y2 - y3)*(x - x3) + (x3 - x2)*(y - y3)) / \
        ((y2 - y3)*(x1 - x3) + (x3 - x2)*(y1 - y3))
    b = ((y3 - y1)*(x - x3) + (x1 - x3)*(y - y3)) / \
        ((y2 - y3)*(x1 - x3) + (x3 - x2)*(y1 - y3))
    c = 1 - a - b   
    return (0<=a<=1) and (0<=b<=1) and (0<=c<=1)

def findTriangleIndex(point, triangles):
    for i in range(len(triangles)):
        if pointInTriangle(point, triangles[i]):
            return i

def dist(p1, p2):
    a = (p2[0]-p1[0])**2 + (p2[1]-p1[1])**2
    return math.sqrt(a)

def pointOnLine2(p, p1, p2):
    d1 = dist(p, p1)
    d2 = dist(p, p2)
    d3 = dist(p1,p2)
    return math.fabs(d3 - (d1+d2)) <= 0.001

# Ich nehm den Abstand von t0-p und t1-p und
# wenn das zusammenaddiert t1-t0 ergibt, liegts drauf.
# Zurueck gegeben wird der Index (0..2) des entfernten Punktes!
def pointOnLine(p, t):
    if pointOnLine2(p, t[0], t[1]):
        return 2
    if pointOnLine2(p, t[1], t[2]):
        return 0
    if pointOnLine2(p, t[2], t[0]):
        return 1
    return -1
    
# prueft, ob t p1 und p2 und not p3 matched.
def matchT(t, p1, p2, notp3):
    b1 = False
    b2 = False
    b3 = True
    index = -1
    for i in range(3):
        if t[i] == p1:
            b1 = True
            continue
        if t[i] == p2:
            b2 = True
            continue
        if t[i] == notp3:
            b3 = False
        else:
            index = i
    return (b1 and b2 and b3, index)

# Findet ein Dreieck, welches p1 und p2 aber NICHT p3 enthaelt.
def findNeighbourTriangle(triangles, p1, p2, notp3):
    for t in triangles:
        (b, i) = matchT(t, p1, p2, notp3)
        if b:
            return (t, i)
    return (None, -1)

# https://en.wikipedia.org/wiki/Delaunay_triangulation
# Brainfuck aber awesome, wenns geht :-)
def notValid(t, p):
    matrix = np.array(
            [[t[0][0],t[0][1],t[0][0]**2+t[0][1]**2,1],
             [t[1][0],t[1][1],t[1][0]**2+t[1][1]**2,1],
             [t[2][0],t[2][1],t[2][0]**2+t[2][1]**2,1],
             [p[0]   ,p[1]   ,p[0]**2   +p[1]**2   ,1]])
             
    return np.linalg.det(matrix) > 0

# Verifiziert die Kante des Dreiecks gegenueber des Index i.
# Weil wir das schoen und sinnvoll programmieren, ist die Kante, die verifiziert
# werden soll immer gegenueber von Punkt 0. Also zwischen p1 und p2.
def legalize(triangles, t):
    # check nextI in nextT auf Validitaet.
    (nextT, nextI) = findNeighbourTriangle(triangles, t[1], t[2], t[0])
    if nextT == None:
        return triangles
    p = nextT[nextI]
    
    if notValid(t, p):
        triangles.remove(t)
        triangles.remove(nextT)
        t1 = (t[0], t[1], p)
        triangles.append(t1)
        t2 = (t[0], p, t[2])
        triangles.append(t2)
        triangles = legalize(triangles, t1)
        triangles = legalize(triangles, t2)
    return triangles    

def insertPointIntoTriangles(point, triangles):
    i = findTriangleIndex(point, triangles)
    line = pointOnLine(point, triangles[i])
    if line == -1:
        # Hier ganz normal in das Dreieck einfuegen:
        t = triangles[i]
        triangles.remove(t)
        t1 = (point, t[0], t[1])
        triangles.append(t1)
        t2 = (point, t[1], t[2])
        triangles.append(t2)
        t3 = (point, t[2], t[0])
        triangles.append(t3)
        triangles = legalize(triangles, t1)
        triangles = legalize(triangles, t2)
        triangles = legalize(triangles, t3)
    else:
        # Hier der Sonderfall: Punkt auf der Kante:
        t1 = triangles[i]
        triangles.remove(t1)
        # Jetzt muss er theoretisch automatisch das richtige zweite Dreieck finden!
        i2 = findTriangleIndex(point, triangles)
        line2 = pointOnLine(point, triangles[i2])
        t2 = triangles[i2]
        triangles.remove(t2)
        
        tt1 = (point, t1[line], t1[(line+1)%3])
        triangles.append(tt1)
        tt2 = (point, t1[(line+2)%3], t1[line])
        triangles.append(tt2)
        tt3 = (point, t2[line2], t2[(line2+1)%3])
        triangles.append(tt3)
        tt4 = (point, t2[(line2+2)%3], t2[line2])
        triangles.append(tt4)
        
        triangles = legalize(triangles, tt1)
        triangles = legalize(triangles, tt2)
        triangles = legalize(triangles, tt3)
        triangles = legalize(triangles, tt4)
        
    return triangles

def createDelaunayTriangulation(points, triangle):
    triangles = [triangle]
    for point in points:
        triangles = insertPointIntoTriangles(point, triangles)
    return triangles    

def removeAllInitTriangles(allTriangles, t):
    triangles = copy.copy(allTriangles)
    for i in range(3):
        for t2 in allTriangles:
            for j in range(3):
                #print t[i], " <--> ", t2[j]
                if t[i] == t2[j]:
                    #print "weg --> ", t[i], " <--> ", t2[j]
                    if t2 in triangles:
                        triangles.remove(t2)
    return triangles

###################################################

# read or create Points out of thin air:
points = [(1,2.5), (2,1), (2,5), (2.5,3), (3.5,2), (4,4.5), (5,3)]
# maximale Ausdehnung der Koordinaten:
m = 12
# Initiales Dreieck:
t = ((-3*m,-3*m), (3*m,0), (0,3*m))

triangles = createDelaunayTriangulation(points, t)
triangles = removeAllInitTriangles(triangles, t)
print triangles















