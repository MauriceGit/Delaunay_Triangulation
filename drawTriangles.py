#!/usr/bin/python
# -*- coding: utf-8 -*-

from PIL import Image, ImageDraw, ImageFilter, ImageEnhance, ImageOps, ImageFile
from delaunay import delaunay
from voronoi import createVoronoiFromDelaunay
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
    im.save(filename, "JPEG")

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
    im.save(filename, "JPEG")
    print "Dreiecke zeichnen: %.2fs" % (time.clock()-start)

def getCenterPoint(t):
    return ((t[0][0]+t[1][0]+t[2][0])/3, (t[0][1]+t[1][1]+t[2][1])/3)

def getTriangleColor(t, im):

    # 3x der Wert in der Mitte + jew. die Ecke / 6.
    color = []
    for i in range(3):
        p = t[i]
        if p[0] >= im.size[0] or p[0] < 0 or p[1] >= im.size[1] or p[1] < 0:
            continue
        color.append(im.getpixel(p))

    p = getCenterPoint(t)
    if p[0] < im.size[0] and p[0] >= 0 and p[1] < im.size[1] and p[1] >= 0:
        centerPixel = im.getpixel(p)
        color = color + [centerPixel]*3

    div = float(len(color))
    color = reduce(lambda rec, x : ((rec[0]+x[0])/div, (rec[1]+x[1])/div, (rec[2]+x[2])/div), color, (0,0,0))
    color = map(lambda x : int(x), color)
    return color

def getPolygonColor(pol, im):

    centerPoint = (0,0)
    color = []
    count = 0
    #print ""

    for p in pol:
        if p[0] >= im.size[0] or p[0] < 0 or p[1] >= im.size[1] or p[1] < 0:
            continue
        count += 1
        color.append(im.getpixel(p))
        centerPoint = (centerPoint[0]+p[0], centerPoint[1]+p[1])

    centerPoint = (centerPoint[0]/count, centerPoint[1]/count)

    color.append(im.getpixel(centerPoint))
    color.append(im.getpixel(centerPoint))
    color.append(im.getpixel(centerPoint))


    div = float(len(color))
    color = reduce(lambda rec, x : ((rec[0]+x[0]), (rec[1]+x[1]), (rec[2]+x[2])), color, (0,0,0))
    color = (color[0]/div, color[1]/div, color[2]/div)
    # Diese Zeile ergibt KEINEN Sinn!!!!!  Aber anders hab ichs nicht zum Laufen gebracht. Irgendein Fehler mit der Farbe...
    color = (color[0]/4.0, color[1]/4.0, color[2]/4.0)
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
    im = brightenImage(im, 3.0)
    ImageFile.MAXBLOCK = im.size[0] * im.size[1]
    im.save(filename, "JPEG", quality=100, optimize=True, progressive=True)

def drawImageColoredVoronoi(polygons, filename, origIm, multiplier):
    start = time.clock()
    (sizeX, sizeY) = origIm.size
    im = Image.new('RGB', (sizeX*multiplier, sizeY*multiplier))
    draw = ImageDraw.Draw(im)
    for pol in polygons:
        if len(pol) < 2:
            continue
        (r,g,b) = getPolygonColor(pol, origIm)
        newPol = map(lambda x: (x[0] * multiplier, x[1]*multiplier), pol)
        draw.polygon(newPol, fill=(r,g,b,255))
    im = brightenImage(im, 3.0)
    ImageFile.MAXBLOCK = im.size[0] * im.size[1]
    im.save(filename, "JPEG", quality=100, optimize=True, progressive=True)
    print "Voronoi zeichnen: %.2fs" % (time.clock()-start)

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
            v = v**2.1 / float(2**18)
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

def autocontrastImage(filename):
    start = time.clock()
    im = Image.open(filename)
    im = ImageOps.autocontrast(im)
    im.save("autocontrasted_" + filename, "JPEG")
    print "Autocontrast Image: %.2fs" % (time.clock()-start)

def equalizeImage(filename):
    start = time.clock()
    im = Image.open(filename)
    im = ImageOps.equalize(im)
    im.save("equalized_" + filename, "JPEG")
    print "Equalize Image: %.2fs" % (time.clock()-start)

def resizeImage(filename, longestSide):
    im = Image.open(filename)
    (width, height) = im.size
    ratioX = float(longestSide) / width
    ratioY = float(longestSide) / height
    ratio = min(ratioX, ratioY)
    im.thumbnail((width*ratio, height*ratio), Image.ANTIALIAS)
    newFilename = "small_" + filename
    im.save(newFilename, "JPEG")
    return newFilename

# Wrapper.
def delaunayFromPoints(points):
    start = time.clock()
    triangles = delaunay(points)
    print "Delaunay-Triangulierung: %.2fs" % (time.clock()-start)
    return triangles

# Wrapper.
def voronoiFromTriangles(triangles):
    start = time.clock()
    polygons = createVoronoiFromDelaunay(triangles)
    print "Voronoi-Polygonalisierung: %.2fs" % (time.clock()-start)
    return polygons

if __name__ == '__main__':
    filename = "sunset_4.jpg"
    filename = resizeImage(filename, 1000)
    (colorIm, blackIm) = loadAndFilterImage(filename)
    (width, height) = colorIm.size
    multiplier = 10

    #points = findPointsFromImage(blackIm)
    points = generateRandomPoints(6000, width, height)
    triangles = delaunayFromPoints(points)
    polygons = voronoiFromTriangles(triangles)

    #drawTriangulation(triangles, "random_" + filename, width, height, multiplier)
    drawImageColoredTriangles(triangles, "delaunay_" + filename, colorIm, multiplier)
    drawImageColoredVoronoi(polygons, "voronoi_" + filename, colorIm, multiplier)

    autocontrastImage("voronoi_" + filename)
    autocontrastImage("delaunay_" + filename)
    #equalizeImage("voronoi_" + filename)




















