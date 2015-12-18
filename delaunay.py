#!/usr/bin/python
# -*- coding: utf-8 -*-

import math
import numpy as np
import copy
import time
import sys
from matplotlib import path
from PIL import Image, ImageDraw

# working but slow!
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

    return (np.linalg.det(m1) >= 0) == (np.linalg.det(m2) >= 0) == (np.linalg.det(m3) >= 0)

def pointInTriangle6(p, t):
    triangle = path.Path([t[0], t[1], t[2]])
    points = np.array([p[0], p[1]]).reshape(1, 2)
    res = triangle.contains_points(points)
    return res[0]

#def findTriangle(point, triangles):
#    for t in triangles:
#        if pointInTriangle6(point, t):
#            return t
#    print "Das sollte nicht passieren..."

def vecLen(v):
    return math.sqrt(v[0]**2 + v[1]**2)

def euclidDistance(p1, p2):
    p = (p2[0]-p1[0], p2[1]-p1[1])
    return vecLen(p)

def alreadyVisited(t, visited):
    for v in visited:
        if t == None or equal(t,v):
            return True
    return False

def getOuterPoint(nextT, thisT):
    for i in range(3):
        if nextT[i] != thisT[0] and nextT[i] != thisT[1] and nextT[i] != thisT[2]:
            return nextT[i]
    print "not happening..."

def debugDrawPath(triangles, startT, p):
    im = Image.new('RGB', (2000, 2000))
    draw = ImageDraw.Draw(im)
    lastT = triangles[0]
    for t in triangles[1:]:
        tmpP1 = ((lastT[0][0]+lastT[1][0]+lastT[2][0])/3.0, (lastT[0][1]+lastT[1][1]+lastT[2][1])/3.0)
        tmpP2 = ((t[0][0]+t[1][0]+t[2][0])/3.0, (t[0][1]+t[1][1]+t[2][1])/3.0)
        draw.polygon((t[0],t[1],t[2]), fill=None, outline='blue')
        draw.line([tmpP1, tmpP2],fill='white')
        lastT = t

    tmpP = (int((startT[0][0]+startT[1][0]+startT[2][0])/3.0), int((startT[0][1]+startT[1][1]+startT[2][1])/3.0))
    print "Tuple:","(",startT[0],startT[1],startT[2],")"
    print tmpP
    draw.arc((p[0], p[1], p[0]+20,p[1]+20),0,360,fill='red')
    draw.arc((tmpP[0], tmpP[1], tmpP[0]+20,tmpP[1]+20),0,360,fill='green')

    im.save("some_lines.jpg")

def getCenterPoint(t):
    return ((t[0][0]+t[1][0]+t[2][0])/3, (t[0][1]+t[1][1]+t[2][1])/3)

def normVectorFromPoints(p1, p2):
    v = (p2[0]-p1[0], p2[1]-p1[1])
    return v/np.linalg.norm(v)

def tupleToString(t):
    return "{" + str(t[0]) + ", " + str(t[1]) + ", " + str(t[0]) + "}"

def printTriangleList(l):
    for t in l:
        if t != None:
            print tupleToString(t),
    print ""

def findTriangle2Rec(p, t, lastT, debug):

    count = 0
    visited = []
    index = 0

    while True:
        upStream = False
        count += 1
        if t != None and pointInTriangle6(p, t):
            #print count
            return t

        d1 = sys.maxint
        d2 = sys.maxint

        # Welches anliegende Dreieck ist näher an p:
        t1 = t[3]
        t2 = t[4]
        t3 = t[5]

        if equal(t1, lastT):
            nextT1 = t2
            nextT2 = t3
        else:
            if equal(t2, lastT):
                nextT1 = t1
                nextT2 = t3
            else:
                nextT1 = t1
                nextT2 = t2

        visitedT1 = alreadyVisited(nextT1, visited)
        visitedT2 = alreadyVisited(nextT2, visited)

        # mehr ein: isInList(t)
        if not alreadyVisited(t, visited):
            visited[:0] = [t]

        if nextT1 == None and nextT2 == None:
            print "shit."

        # Wenn einer von beiden None ist und der andere nicht.
        if nextT1 == None and nextT2 != None:
            if not visitedT2:
                t = nextT2
                continue
            else:
                upStream = True

        if nextT2 == None and nextT1 != None:
            if not visitedT1:
                t = nextT1
                continue
            else:
                upStream = True

        if not upStream:
            # Vektorrechnung um zu überprüfen, welche Richtung mehr in Richtung
            # des Ziels führt. In die Richtung wollen wir gehen!
            herePos   = getCenterPoint(t)
            targetPos = p
            dir1Pos   = getCenterPoint(nextT1)
            dir2Pos   = getCenterPoint(nextT2)
            dir1      = normVectorFromPoints(herePos, dir1Pos)
            dir2      = normVectorFromPoints(herePos, dir2Pos)
            targetVector = normVectorFromPoints(herePos, targetPos)
            dot1 = np.dot(targetVector, dir1)
            dot2 = np.dot(targetVector, dir2)

            # Je größer das Skalarprodukt ist, desto mehr geht der Richtungsvektor
            # in Richtung des Zielpunktes und wir nähern uns immer stärker an!
            if dot1 > dot2 and not visitedT1:
                lastT = t
                t = nextT1
                continue

            if dot2 > dot1 and not visitedT2:
                lastT = t
                t = nextT2
                continue

            if not visitedT1:
                lastT = t
                t = nextT1
                continue

            if not visitedT2:
                lastT = t
                t = nextT2
                continue

        lastT = t
        index += 1
        t = visited[index]

# Might be faster...
def findTriangle2(point, triangles, debug):
    # Start with first triangle Doesn't matter which one.
    #print len(triangles),
    return findTriangle2Rec(point, triangles[0], None, debug)

def dist(p1, p2):
    a = (p2[0]-p1[0])**2 + (p2[1]-p1[1])**2
    return math.sqrt(a)

def pointOnLine2(p, p1, p2):
    d1 = dist(p, p1)
    d2 = dist(p, p2)
    d3 = dist(p1,p2)
    return math.fabs(d3 - (d1+d2)) <= 0.0000001

def equal(t1, t2):
    return (t1 == None and t2 == None) or (t1 != None and t2 != None and (t1[0] == t2[0] and t1[1] == t2[1] and t1[2] == t2[2]))

# Muss ich selber implementieren, da nur die ersten 3 Komponenten auf
# Gleichheit getestet werden sollen!
def removeTriangleFromList(triangle, triangles):
    for t in triangles:
        if equal(t, triangle):
            triangles.remove(t)
    return triangles

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

# Prüft, ob die uebergebenen zwei Punkte zu t gehören.
def pointsMatchTriangle(p1, p2, t):
    return t != None and (p1 == t[0] or p1 == t[1] or p1 == t[2]) and (p2 == t[0] or p2 == t[1] or p2 == t[2])

# Bestimmt die Referenz, die quasi nach außen zeigt von dem neuen Dreieck aus.
def getReferenceWithPoints(p1, p2, t):
    for i in range(3):
        if pointsMatchTriangle(p1, p2, t[3+i]):
            return t[3+i]
    # Grenzt nach ganz außen (MUSS!!!)
    return None

# Verifiziert die Kante des Dreiecks gegenueber des Index i.
# Weil wir das schoen und sinnvoll programmieren, ist die Kante, die verifiziert
# werden soll immer gegenueber von Punkt 0. Also zwischen p1 und p2.
def legalize(triangles, t):
    # check nextI in nextT auf Validitaet.
    nextT = getReferenceWithPoints(t[1], t[2], t)

    if nextT == None:
        return triangles

    (b, nextI) = matchT(nextT, t[1], t[2], t[0])
    p = nextT[nextI]

    if notValid(t, p):

        triangles = removeTriangleFromList(t, triangles)
        triangles = removeTriangleFromList(nextT, triangles)

        t1 = [t[0], t[1], p, getReferenceWithPoints(t[0], t[1], t), getReferenceWithPoints(t[1], p, nextT)]
        t2 = [t[0], p, t[2], getReferenceWithPoints(t[0], t[2], t), getReferenceWithPoints(t[2], p, nextT), t1]

        t1.append(t2)

        changeReferenceFromTo(t, t1, t1[3])
        changeReferenceFromTo(nextT, t1, t1[4])

        changeReferenceFromTo(t, t2, t2[3])
        changeReferenceFromTo(nextT, t2, t2[4])

        triangles.append(t1)
        triangles.append(t2)

        triangles = legalize(triangles, t1)
        triangles = legalize(triangles, t2)
    return triangles

# verändert in t die veraltete Referenz fromT nach toT.
def changeReferenceFromTo(fromT, toT, t):
    for i in range(3,6):
        if fromT != None and t != None and t[i] != None and equal(t[i], fromT):
            t[i] = toT
            break

def findNextTriangleWithPoint(point, t):
    for i in range(3, 6):
        if t != None and pointInTriangle6(point, t[i]):
            return t[i]
    print "shit fuck"


# Fuegt einen Punkt in eine bestehende Triangulierung ein und
# korrigiert moegliche auftretende Fehler.
def insertPointIntoTriangles(point, triangles, debug):
    t = findTriangle2(point, triangles, debug)
    line = pointOnLine(point, t)

    triangles = removeTriangleFromList(t, triangles)
    if line == -1:
        # Hier ganz normal in das Dreieck einfuegen:
        t1 = [point, t[0], t[1], getReferenceWithPoints(t[0], t[1], t)]
        t2 = [point, t[1], t[2], getReferenceWithPoints(t[1], t[2], t), t1]
        t3 = [point, t[2], t[0], getReferenceWithPoints(t[2], t[0], t), t1, t2]

        changeReferenceFromTo(t, t1, t1[3])
        changeReferenceFromTo(t, t2, t2[3])
        changeReferenceFromTo(t, t3, t3[3])

        t2.append(t3)
        t1.append(t2)
        t1.append(t3)

        ################################################################

        triangles.append(t1)
        triangles.append(t2)
        triangles.append(t3)

        triangles = legalize(triangles, t1)
        triangles = legalize(triangles, t2)
        triangles = legalize(triangles, t3)

    else:
        #print "Sonderfall: Punkt auf Kante zweier Dreiecke."
        # Hier der Sonderfall: Punkt auf der Kante:
        # Jetzt muss er theoretisch automatisch das richtige zweite Dreieck finden!
        t2 = findNextTriangleWithPoint(point, t)

        if t2 == None:
            print "shit shit shit..."
            return triangles

        line2 = pointOnLine(point, t2)

        triangles = removeTriangleFromList(t2, triangles)

        tt1 = [point, t[line], t[(line+1)%3],     getReferenceWithPoints(t[line], t[(line+1)%3], t)]
        tt2 = [point, t[(line+2)%3], t[line],     getReferenceWithPoints(t[(line+2)%3], t[line], t), tt1]

        tt3 = [point, t2[line2], t2[(line2+1)%3], getReferenceWithPoints(t2[line2], t2[(line2+1)%3], t2)]
        tt4 = [point, t2[(line2+2)%3], t2[line2], getReferenceWithPoints(t2[(line2+2)%3], t2[line2], t2), tt3]

        tt1.append(tt2)
        tt3.append(tt4)

        changeReferenceFromTo(t,  tt1, tt1[3])
        changeReferenceFromTo(t,  tt2, tt2[3])
        changeReferenceFromTo(t2, tt3, tt3[3])
        changeReferenceFromTo(t2, tt4, tt4[3])

        if getReferenceWithPoints(point, t[(line+1)%3], tt3) != None:
            tt1.append(getReferenceWithPoints(point, t[(line+1)%3], tt3))
            tt2.append(getReferenceWithPoints(point, t[(line+2)%3], tt4))
        else:
            tt1.append(getReferenceWithPoints(point, t[(line+1)%3], tt4))
            tt2.append(getReferenceWithPoints(point, t[(line+2)%3], tt3))

        if getReferenceWithPoints(point, t2[(line2+1)%3], tt1) != None:
            tt3.append(getReferenceWithPoints(point, t2[(line2+1)%3], tt1))
            tt4.append(getReferenceWithPoints(point, t2[(line2+2)%3], tt2))
        else:
            tt3.append(getReferenceWithPoints(point, t2[(line2+1)%3], tt2))
            tt4.append(getReferenceWithPoints(point, t2[(line2+2)%3], tt1))

        triangles.append(tt1)
        triangles.append(tt2)
        triangles.append(tt3)
        triangles.append(tt4)

        triangles = legalize(triangles, tt1)
        triangles = legalize(triangles, tt2)
        triangles = legalize(triangles, tt3)
        triangles = legalize(triangles, tt4)



    return triangles

# Fuegt inkrementell Punkte in die Triangulierung ein.
def createDelaunayTriangulation(points, triangle):
    triangles = [triangle]
    for point in points:
        triangles = insertPointIntoTriangles(point, triangles, False)
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
# O(n)
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
# Soll im Endeffekt am liebsten in O(n logn) laufen...
def delaunay(points):
    # maximale Ausdehnung der Koordinaten:
    # O(n)
    m = maxCoord(points)
    # Initiales Dreieck:
    t = [(-3*m,-3*m), (3*m,0), (0,3*m), None, None, None]

    # Datenstruktur der Dreiecksliste:
    # type Ref       = Triangle
    # type Triangle  = [a,b,c, Ref, Ref, Ref]
    # type Triangles = [Triangle]

    # O( ... )
    triangles = createDelaunayTriangulation(points, t)

    triangles = removeAllInitTriangles(triangles, t)
    triangles = removeOutOfBoundsTriangles(triangles, -m, -m, m, m)

    return triangles












