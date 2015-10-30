import math
import numpy as np
import copy
import time

def sign(p1, p2, p3):
  return (p1[0] - p3[0]) * (p2[1] - p3[1]) - (p2[0] - p3[0]) * (p1[1] - p3[1])

def pointInAABB(pt, c1, c2):
  return c2[0] <= pt[0] <= c1[0] and c2[1] <= pt[1] <= c1[1]

# http://stackoverflow.com/questions/20248076/how-do-i-check-if-a-point-is-inside-a-triangle-on-the-line-is-ok-too
# Thanks a lot to: Krumelur, even though he stole it too from GameDev somewhere :-)
def pointInTriangle3(pt, v1, v2, v3):
    b1 = sign(pt, v1, v2) <= 0
    b2 = sign(pt, v2, v3) <= 0
    b3 = sign(pt, v3, v1) <= 0
    
    return ((b1-b2)<0.000001) and ((b2-b3)<0.000001) and pointInAABB(pt, map(max, v1, v2, v3), map(min, v1, v2, v3))

def pointInTriangle2(p, t):
    return pointInTriangle3(p, t[0], t[1], t[2])
    
def pointInTriangle4(p,t):
    
    m1 = np.array([ [1, t[0][0], t[0][1]],
                    [1, t[1][0], t[1][1]],
                    [1, p[0]   , p[1]   ]])
    m2 = np.array([ [1, t[1][0], t[1][1]],
                    [1, t[2][0], t[2][1]],
                    [1, p[0]   , p[1]   ]])
    m3 = np.array([ [1, t[2][0], t[2][1]],
                    [1, t[0][0], t[0][1]],
                    [1, p[0]   , p[1]   ]])
    
    res = (np.linalg.det(m1) >= 0) == (np.linalg.det(m2) >= 0) == (np.linalg.det(m3) >= 0)
    return res
    

def findTriangle(point, triangles):
    for t in triangles:
        if pointInTriangle4(point, t):
            return t
    print "Das sollte nicht passieren..."

def dist(p1, p2):
    a = (p2[0]-p1[0])**2 + (p2[1]-p1[1])**2
    return math.sqrt(a)

def pointOnLine2(p, p1, p2):
    d1 = dist(p, p1)
    d2 = dist(p, p2)
    d3 = dist(p1,p2)
    return math.fabs(d3 - (d1+d2)) <= 0.0000001

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

# Fuegt einen Punkt in eine bestehende Triangulierung ein und
# korrigiert moegliche auftretende Fehler.
def insertPointIntoTriangles(point, triangles):
    t = findTriangle(point, triangles)
    line = pointOnLine(point, t)
    
    triangles.remove(t)
    if line == -1:
        # Hier ganz normal in das Dreieck einfuegen:
        t1 = (point, t[0], t[1])
        triangles.append(t1)
        triangles = legalize(triangles, t1)
        t2 = (point, t[1], t[2])
        triangles.append(t2)
        triangles = legalize(triangles, t2)
        t3 = (point, t[2], t[0])
        triangles.append(t3)
        triangles = legalize(triangles, t3)
    else:
        #print "Sonderfall: Punkt auf Kante zweier Dreiecke."
        # Hier der Sonderfall: Punkt auf der Kante:
        # Jetzt muss er theoretisch automatisch das richtige zweite Dreieck finden!
        t2 = findTriangle(point, triangles)
        line2 = pointOnLine(point, t2)
        triangles.remove(t2)
        
        tt1 = (point, t[line], t[(line+1)%3])
        triangles.append(tt1)
        triangles = legalize(triangles, tt1)
        tt2 = (point, t[(line+2)%3], t[line])
        triangles.append(tt2)
        triangles = legalize(triangles, tt2)
        tt3 = (point, t2[line2], t2[(line2+1)%3])
        triangles.append(tt3)
        triangles = legalize(triangles, tt3)
        tt4 = (point, t2[(line2+2)%3], t2[line2])
        triangles.append(tt4)
        triangles = legalize(triangles, tt4)
        
    return triangles

# Fuegt inkrementell Punkte in die Triangulierung ein.
def createDelaunayTriangulation(points, triangle):
    triangles = [triangle]
    for point in points:
        triangles = insertPointIntoTriangles(point, triangles)
    return triangles    

# Loescht alle Dreiecke, die sich auf das initiale Dreieck beziehen.
def removeAllInitTriangles(triangles, t):
    for i in range(3):
        for t2 in triangles:
            for j in range(3):
                if t[i] == t2[j]:
                    triangles.remove(t2)
    return triangles

# Maximale Koordinate in irgendeine Richtung...
def maxCoord(points):
    ma = 0
    mi = 0
    for p in points:
        ma = max(max(p), ma)
        mi = min(min(p), mi)
    return max(ma, math.fabs(mi))

# Es kommt vor, dass Dreiecke erstellt werden, die die Grenzen ueberschreiten...
# Die werden erstmal manuell geloescht.
def removeOutOfBoundsTriangles(triangles, minX, minY, maxX, maxY):
    for t in triangles:
        for i in range(3):
            p = t[i]
            if p[0] > maxX or p[1] > maxY or p[0] < minX or p[1] < minY:
                if t in triangles:
                    triangles.remove(t)
    return triangles

# Erstellt eine Delaunay-Triangulierung der uebergebenen Punkte!
def delaunay(points, minX, minY, maxX, maxY):
    # maximale Ausdehnung der Koordinaten:
    m = maxCoord(points)
    # Initiales Dreieck:
    t = ((-3*m,-3*m), (3*m,0), (0,3*m))

    triangles = createDelaunayTriangulation(points, t)
    
    start = time.clock()
    # Alle Dreiecke nochmal legalisieren, Just in Case...
    for t1 in triangles:
        triangles = legalize(triangles, t1)
    print "Legalisieren dauert: %.2fs" % (time.clock()-start)
    
    triangles = removeAllInitTriangles(triangles, t)
    triangles = removeOutOfBoundsTriangles(triangles, minX, minY, maxX, maxY)
    
    return triangles












