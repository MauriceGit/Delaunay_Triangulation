#!/usr/bin/python
# -*- coding: utf-8 -*-

#import math
import numpy as np
from shapely.geometry import LineString
from PIL import Image, ImageDraw


# Calculates a perpendicular bisector for the line between p1 and p2 and returnes
# a new line (point and direction) which represents the perpendicular bisector.
def calcPerpendicularBisector(p1, p2):
    diff = (p2[0]-p1[0], p2[1]-p1[1])
    v = np.array([diff[0], diff[1], 0])
    z = np.array([0,0,1])
    cross = np.cross(v,z)
    middle = (p1[0]+diff[0]/2.0, p1[1]+diff[1]/2.0)
    newPoint = (middle[0]+cross[0], middle[1]+cross[1])
    return (middle, newPoint)

# Thanks to Paul Draper at
# http://stackoverflow.com/questions/20677795/find-the-point-of-intersecting-lines
def line_intersection(line1, line2):
    xdiff = (line1[0][0] - line1[1][0], line2[0][0] - line2[1][0])
    ydiff = (line1[0][1] - line1[1][1], line2[0][1] - line2[1][1]) #Typo was here

    def det(a, b):
        return a[0] * b[1] - a[1] * b[0]

    div = det(xdiff, ydiff)
    if div == 0:
       raise Exception('lines do not intersect')

    d = (det(*line1), det(*line2))
    x = det(d, xdiff) / div
    y = det(d, ydiff) / div
    return x, y

def calcIntersection(t):
    pb1 = calcPerpendicularBisector(t[0], t[1])
    pb2 = calcPerpendicularBisector(t[1], t[2])
    return line_intersection(pb1, pb2)

def valid(t1, triangles):
    for t in triangles:
        if equalT(t, t1) or t1 == None:
            return False
    return True

def equalT(t1, t2):
    return t1 != None and t2 != None and t1[0] == t2[0] and t1[1] == t2[1] and t1[2] == t2[2]

def tupleToString(t):
    if t != None:
        return "{" + str(t[0]) + ", " + str(t[1]) + ", " + str(t[2])  + "}"
    else:
        return "None"

def printTriangleList(l):
    for t in l:
        if t != None:
            print tupleToString(t),
    print ""

def printT(t):
    print tupleToString(t),
def printTNewline(t):
    print tupleToString(t)

def getNextTriangle(p, t, lastT):
    for i in range(3,6):
        if valid(t, lastT):
            if t[i][0] == p or t[i][1] == p or t[i][2] == p:
                return t[i]
    return None

def debugDrawPath(triangles, p):
    im = Image.new('RGB', (2000, 2000))
    draw = ImageDraw.Draw(im)
    for t in triangles:
        tn = []
        for i in range(3):
            tn.append(map(lambda y:y*50, list(t[i])))
        draw.polygon((tuple(tn[0]),tuple(tn[1]),tuple(tn[2])), fill=None, outline='white')

    pn = tuple(map(lambda x: x*50, p))
    draw.arc((pn[0], pn[1], pn[0]+20,pn[1]+20),0,360,fill='red')

    im.save("some_lines.jpg")

def getTrianglesAroundPoint(p, t):
    lastT = None
    firstT = t
    thisT = t
    triangles = []
    while True:
        triangles.append(thisT)
        nextT = getNextTriangle(p, thisT, triangles)

        if nextT == None:
            break

        lastT = thisT
        thisT = nextT
    return triangles


def calcPolygonRec(p, firstT, t, lastT):

    listOfIntersections = []
    listOfTriangles = []

    while True:
        intersection = calcIntersection(t)

        if intersection in listOfIntersections:
            print "already in."
            break

        listOfIntersections.append(intersection)

        # calc next triangle to go to.
        nextT = getNextTriangle(p, t, lastT)

        if equalT(firstT, nextT):
            print "yay"
            break

        listOfTriangles.append(nextT)

        lastT = t
        t = nextT

    debugDrawPath(listOfTriangles, p)

    return listOfIntersections

# Calculates a polygon by following all references to triangles which contain the defined
# point. Until we get back to the initial triangle. Then a closed polygon should be constructed.
def calcOnePolygonAroundPoint(p, t):
    return calcPolygonRec(p, t, t, None)

#
# Gets a list of valid triangles (with the references to each other!)
# Creates a list of valid voronoi-polygons.
#
def createVoronoiFromDelaunay(triangles):

    for t in triangles[:10]:
        printTriangleList(getTrianglesAroundPoint(t[0], t))
        #polygon = calcOnePolygonAroundPoint(t[0], t)
        #print "len:",len(polygon),
        #print polygon





















