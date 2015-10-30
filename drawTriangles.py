from PIL import Image, ImageDraw
from delaunay import delaunay
import random as rand
import time

x = 800
y = 800

start = time.clock()

points = []
for i in range(500):
	points.append((rand.randint(0,x),rand.randint(0,y)))

points.append((0,0))
points.append((0,y))
points.append((x,0))
points.append((x,y))

print "Punkte generieren: %.2fs" % (time.clock()-start)
start = time.clock()

triangles = delaunay(points, 0, 0, x, y)

print "Delaunay-Triangulierung: %.2fs" % (time.clock()-start)
start = time.clock()

im = Image.new('RGB', (x, y))
draw = ImageDraw.Draw(im)

for t in triangles:
	draw.polygon(t, fill=(rand.randint(0,255),rand.randint(0,255),rand.randint(0,255),255))
	#draw.polygon(t, outline='red')

print "Dreiecke zeichnen: %.2fs" % (time.clock()-start)

im.save('triangle.jpg')
