#!/usr/bin/python
# -*- coding: utf-8 -*-

from PIL import Image, ImageDraw
from delaunay import delaunay
import random as rand
import time

x = 10000
y = 10000

start = time.clock()

points = []
for i in range(2000):
	p = (rand.randint(0,x),rand.randint(0,y))
	if not p in points:
		points.append(p)

#points.append((0,0))
#points.append((0,y))
#points.append((x,0))
#points.append((x,y))

print "Punkte generieren: %.2fs" % (time.clock()-start)
start = time.clock()

triangles = delaunay(points)

print "Delaunay-Triangulierung: %.2fs" % (time.clock()-start)
start = time.clock()

im = Image.new('RGB', (x, y))
draw = ImageDraw.Draw(im)

for t in triangles:
	draw.polygon((t[0],t[1],t[2]), fill=(rand.randint(0,255),rand.randint(0,255),rand.randint(0,255),255))
	#draw.polygon(t, outline='red')

print "Dreiecke zeichnen: %.2fs" % (time.clock()-start)

im.save('triangle_fast.jpg')
