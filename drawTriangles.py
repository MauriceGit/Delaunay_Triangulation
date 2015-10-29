from PIL import Image, ImageDraw
from delaunay import delaunay
import random as rand

points = []
for i in range(10):
	points.append((rand.randint(0,500),rand.randint(0,500)))

triangles = delaunay(points)
print triangles

im = Image.new('RGB', (500, 500))
draw = ImageDraw.Draw(im)

for t in triangles:
	#draw.polygon(t, outline='red', fill=(rand.randint(0,255),rand.randint(0,255),rand.randint(0,255),255))
	draw.polygon(t, outline='red')

im.save('triangle.jpg')
