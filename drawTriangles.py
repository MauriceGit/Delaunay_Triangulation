#!/usr/bin/python
# -*- coding: utf-8 -*-

from PIL import Image, ImageDraw
from delaunay import delaunay
import random as rand
import time

def generateRandomPoints(count, sizeX, sizeY):
    points = []
    start = time.clock()
    for i in range(count):
        p = (rand.randint(0,sizeX),rand.randint(0,sizeY))
        if not p in points:
            points.append(p)
    print "Punkte generieren: %.2fs" % (time.clock()-start)
    return points

def generateWeightedRandomPoints(count, sizeX, sizeY):
    points = []
    start = time.clock()
    for i in range(count):
        x = rand.randint(0,sizeX/2)-rand.randint(0,sizeX/2) + sizeX/2
        y = rand.randint(0,sizeY/2)-rand.randint(0,sizeY/2) + sizeY/2
        p = (x, y)
        if not p in points:
            points.append(p)
    print "Punkte generieren: %.2fs" % (time.clock()-start)
    return points

def drawPoints(points, filename, sizeX, sizeY):
    im = Image.new('RGB', (sizeX*10, sizeY*10))
    draw = ImageDraw.Draw(im)
    for p in debugPoints:
        px = p[0]*10
        py = p[1]*10
        draw.arc((px, py, px+20,py+20),0,360,fill='white')
    im.save(filename)

def drawTriangulation(triangles, filename, sizeX, sizeY):
    im = Image.new('RGB', (sizeX, sizeY))
    draw = ImageDraw.Draw(im)
    start = time.clock()
    for t in triangles:
        r = rand.randint(0,255)
        g = rand.randint(0,255)
        b = rand.randint(0,255)
        draw.polygon((t[0],t[1],t[2]), fill=(r,g,b,255))
    im.save(filename)
    print "Dreiecke zeichnen: %.2fs" % (time.clock()-start)

def generateTriangles(points):
    start = time.clock()
    triangles = delaunay(points)
    print "Delaunay-Triangulierung: %.2fs" % (time.clock()-start)
    return triangles


########################################################################
########################################################################
########################################################################


sizeX = 20000
sizeY = 20000
pointCount = 5000

#points = generateRandomPoints(pointCount, sizeX, sizeY)
points = generateWeightedRandomPoints(pointCount, sizeX, sizeY)

#drawPoints(debugPoints, "debug_out.jpg", sizeX, sizeY)

triangles = generateTriangles(points)

drawTriangulation(triangles, "triangle_fast.jpg", sizeX, sizeY)

