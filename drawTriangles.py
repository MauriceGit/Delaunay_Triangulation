from PIL import Image, ImageDraw
from delaunay import delaunay
import random as rand

x = 1920
y = 1080

points = []
for i in range(100):
	points.append((rand.randint(0,x),rand.randint(0,y)))
points.sort()

triangles = delaunay(points)

im = Image.new('RGB', (x, y))
draw = ImageDraw.Draw(im)

for t in triangles:
	draw.polygon(t, outline='red', fill=(rand.randint(0,255),rand.randint(0,255),rand.randint(0,255),255))
	#draw.polygon(t, outline='red')

im.save('triangle.jpg')
