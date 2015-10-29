from PIL import Image, ImageDraw
from delaunay import delaunay
import random as rand
import time

x = 1920
y = 1080

start = time.clock()

points = []
for i in range(1000):
	points.append((rand.randint(0,x),rand.randint(0,y)))
points.sort()

print "Punkte generieren: %.2gs" % (time.clock()-start)
start = time.clock()

triangles = delaunay(points)

print "Delaunay-Triangulierung: %.2gs" % (time.clock()-start)
start = time.clock()

im = Image.new('RGB', (x, y))
draw = ImageDraw.Draw(im)

for t in triangles:
	draw.polygon(t, outline='red', fill=(rand.randint(0,255),rand.randint(0,255),rand.randint(0,255),255))
	#draw.polygon(t, outline='red')

print "Dreiecke zeichnen: %.2gs" % (time.clock()-start)

im.save('triangle.jpg')
