import math

# http://totologic.blogspot.de/2014/01/accurate-point-in-triangle-test.html
def pointInTriangle(p, t):
	x  = p[0]
	y  = p[1]
	x1 = t[0][0]
	y1 = t[0][1]
	x2 = t[1][0]
	y2 = t[1][1]
	x3 = t[2][0]
	y3 = t[2][1]
	
	a = ((y2 - y3)*(x - x3) + (x3 - x2)*(y - y3)) / \
	    ((y2 - y3)*(x1 - x3) + (x3 - x2)*(y1 - y3))
	b = ((y3 - y1)*(x - x3) + (x1 - x3)*(y - y3)) / \
	    ((y2 - y3)*(x1 - x3) + (x3 - x2)*(y1 - y3))
	c = 1 - a - b	
	return (0<=a<=1) and (0<=b<=1) and (0<=c<=1)

def findTriangleIndex(point, triangles):
	for i in range(len(triangles)):
		if pointInTriangle(point, triangles[i]):
			return i

def dist(p1, p2):
	return math.sqrt((p2[0]-p1[0])**2 + (p2[1]-p1[1])**2)

def pointOnLine2(p, p1, p2):
	d1 = dist(p, p1)
	d2 = dist(p, p2)
	return dist(p1, p2)-(d1+d1) <= 0.001

def pointOnLine(p, t):
	# Ich nehm den Abstand von t0-p und t1-p und
	# wenn das zusammenaddiert t1-t0 ergibt, liegts drauf.
	if pointOnLine2(p, t[0], t[1]):
		return 0
	if pointOnLine2(p, t[1], t[2]):
		return 1
	if pointOnLine2(p, t[2], t[0]):
		return 2
	return -1

def insertPointIntoTriangles(point, triangles):
	i = findTriangleIndex(point, triangles)
	line = pointOnLine(point, triangles[i])
	#if line == -1:
		# Hier ganz normal in das Dreieck einfuegen:
	#else:
		# Hier der Sonderfall: Punkt auf der Kante:
	return triangles

def createDelaunayTriangulation(points, triangles):
	for point in points:
		triangles = insertPointIntoTriangles(point, triangles)
	return triangles	

###################################################

# read or create Points out of thin air:
points = [(3,2), (1,3), (5,2), (6,4)]
# maximale Ausdehnung der Koordinaten:
m = 12
# Initiales Dreieck:
firstTriangle = [((-3*m,-3*m), (3*m,0), (0,3*m))]

triangles = createDelaunayTriangulation(points, firstTriangle)

print triangles

# Ich glaub hier sind noch Fehler...
print pointOnLine2((1,0),(0,0),(2,0))
