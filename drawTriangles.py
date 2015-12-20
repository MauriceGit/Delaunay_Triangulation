#!/usr/bin/python
# -*- coding: utf-8 -*-

from PIL import Image, ImageDraw, ImageFilter, ImageEnhance
from delaunay import delaunay
import random as rand
import time
import numpy as np
import pickle

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
    for p in points:
        px = p[0]*10
        py = p[1]*10
        draw.arc((px, py, px+20,py+20),0,360,fill='white')
    im.save(filename)

def drawTriangulation(triangles, filename, sizeX, sizeY, multiplier):
    im = Image.new('RGB', (sizeX*multiplier, sizeY*multiplier))
    draw = ImageDraw.Draw(im)
    start = time.clock()
    for t in triangles:
        r = rand.randint(0,255)
        g = rand.randint(0,255)
        b = rand.randint(0,255)
        p0 = tuple(map(lambda x:x*multiplier, t[0]))
        p1 = tuple(map(lambda x:x*multiplier, t[1]))
        p2 = tuple(map(lambda x:x*multiplier, t[2]))
        drawT = (p0, p1, p2)
        draw.polygon(drawT, fill=(r,g,b,255))
    im.save(filename)
    print "Dreiecke zeichnen: %.2fs" % (time.clock()-start)

def getCenterPoint(t):
    return ((t[0][0]+t[1][0]+t[2][0])/3, (t[0][1]+t[1][1]+t[2][1])/3)

def getTriangleColor(t, im):

    # 3x der Wert in der Mitte + jew. die Ecke / 6.
    center = getCenterPoint(t)
    p1 = t[0]
    p2 = t[1]
    p3 = t[2]
    centerPixel = im.getpixel(center)
    color = [im.getpixel(p1), im.getpixel(p2), im.getpixel(p3)] + [centerPixel]*3
    div = float(len(color))
    color = reduce(lambda rec, x : ((rec[0]+x[0])/div, (rec[1]+x[1])/div, (rec[2]+x[2])/div), color, (0,0,0))
    color = map(lambda x : int(x), color)
    return color

def brightenImage(im, value):
    enhancer = ImageEnhance.Brightness(im)
    im = enhancer.enhance(value)
    return im

def drawImageColoredTriangles(triangles, filename, origIm, multiplier):
    (sizeX, sizeY) = origIm.size
    im = Image.new('RGB', (sizeX*multiplier, sizeY*multiplier))
    draw = ImageDraw.Draw(im)
    start = time.clock()
    for t in triangles:
        (r,g,b) = getTriangleColor(t, origIm)
        p0 = tuple(map(lambda x:x*multiplier, t[0]))
        p1 = tuple(map(lambda x:x*multiplier, t[1]))
        p2 = tuple(map(lambda x:x*multiplier, t[2]))
        drawT = (p0, p1, p2)
        draw.polygon(drawT, fill=(r,g,b,255))
    im = brightenImage(im, 7.0)
    im.save(filename)

def generateTriangles(points):
    start = time.clock()
    triangles = delaunay(points)
    print "Delaunay-Triangulierung: %.2fs" % (time.clock()-start)
    return triangles

# Der Faktor, der die Anzahl generierter Punkte bestimmt ist der Exponent von v.
# Auf ein Bild der Auflösung 1000x750:
# 1.0 ~ 80   Punkte
# 1.5 ~ 500  Punkte
# 2.0 ~ 3000 Punkte
# 2.2 ~ 9500 Punkte
def findPointsFromImage(im):
    start = time.clock()
    pix = np.array(im)
    points = []

    for row in range(len(pix)):
        for col in range(len(pix[row])):

            v =  pix[row][col]
            v = v**2.2 / float(2**18)
            if np.random.random() < v:
                points.append((col, row))

    print "Anzahl erzeugter Punkte:", len(points)
    print "Punkte extrahieren: %.2fs" % (time.clock()-start)
    return points


def loadAndFilterImage(name):
    start = time.clock()
    orig = Image.open(name)
    im = orig.convert("L")
    im = im.filter(ImageFilter.GaussianBlur(radius=5))
    im = im.filter(ImageFilter.FIND_EDGES)

    im = brightenImage(im, 20.0)

    im = im.filter(ImageFilter.GaussianBlur(radius=5))
    print "Bild laden: %.2fs" % (time.clock()-start)
    return (orig, im)

def tupleToString(t):
    return "{" + str(t[0]) + ", " + str(t[1]) + ", " + str(t[0]) + "}"

def printTriangleList(l):
    for t in l:
        if t != None:
            print tupleToString(t),
    print ""

def removeUnusedLinks(triangles):
    newList = []
    for t in triangles:
        newList[:0] = (t[0],t[1],t[2])
    return newList

def pointsToTriangles(points):
    triangles = []
    for i in range(len(points)-2):
        t = (points[i],points[i+1],points[i+2])
        triangles.append(t)
    return triangles

def readTriangleListFromFile(filename):
    with open(filename, 'r') as f:
        points = pickle.load(f)
    triangles = pointsToTriangles(points)
    return triangles

def saveTriangleListToFile(triangles, filename):

    triangles = removeUnusedLinks(triangles)
    with open(filename, 'w') as f:
        pickle.dump(triangles, f)

def delaunayFromImage():
    (colorIm, blackIm) = loadAndFilterImage("sunset_small.jpg")
    points = findPointsFromImage(blackIm)
    triangles = generateTriangles(points)

    #saveTriangleListToFile(triangles, "triangles.txt")
    #triangles = readTriangleListFromFile("triangles.txt")
    #printTriangleList(triangles)

    # Alle Werte (besonder inklusive Bildgröße) werden hochskaliert.
    multiplier = 10
    (width, height) = colorIm.size
    drawTriangulation(triangles, "triangle_fast.jpg", width, height, multiplier)
    drawImageColoredTriangles(triangles, "triangle_colored.jpg", colorIm, multiplier)

if __name__ == '__main__':
    delaunayFromImage()

    #im = Image.open("triangle_colored.jpg")
    #im = brightenImage(im, 20.0)
    #im.save("triangle_colored.jpg")




















