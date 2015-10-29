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
    a = (p2[0]-p1[0])**2 + (p2[1]-p1[1])**2
    return math.sqrt(a)

def pointOnLine2(p, p1, p2):
    d1 = dist(p, p1)
    d2 = dist(p, p2)
    d3 = dist(p1,p2)
    return math.fabs(d3 - (d1+d2)) <= 0.001

# Ich nehm den Abstand von t0-p und t1-p und
# wenn das zusammenaddiert t1-t0 ergibt, liegts drauf.
# Zurueck gegeben wird der Index (0..2) des entfernten Punktes!
def pointOnLine(p, t):
    if pointOnLine2(p, t[0], t[1]):
        return 2
    if pointOnLine2(p, t[1], t[2]):
        return 0
    if pointOnLine2(p, t[2], t[0]):
        return 1
    return -1

# Verifiziert die Kante des Dreiecks gegenüber des Index i.
def legalize(t, i):
    
    

def insertPointIntoTriangles(point, triangles):
    i = findTriangleIndex(point, triangles)
    line = pointOnLine(point, triangles[i])
    if line == -1:
        # Hier ganz normal in das Dreieck einfuegen:
        t = triangles[i]
        triangles.remove(t)
        triangles.append((point, t[0], t[1]))
        triangles.append((point, t[1], t[2]))
        triangles.append((point, t[2], t[0]))
    else:
        # Hier der Sonderfall: Punkt auf der Kante:
        t1 = triangles[i]
        triangles.remove(t1)
        # Jetzt muss er theoretisch automatisch das richtige zweite Dreieck finden!
        i2 = findTriangleIndex(point, triangles)
        line2 = pointOnLine(point, triangles[i2])
        t2 = triangles[i2]
        triangles.remove(t2)
        
        triangles.append((point, t1[line], t1[(line+1)%3]))
        triangles.append((point, t1[(line+2)%3], t1[line]))
        triangles.append((point, t2[line2], t2[(line2+1)%3]))
        triangles.append((point, t2[(line2+2)%3], t2[line2]))
        
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
















