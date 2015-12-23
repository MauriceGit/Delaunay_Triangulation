# Delaunay-Triangulation
This project consists of several parts which are joined together.

* **Triangulation**

I always wanted to properly implement a delaunay triangulation. So here it is. It runs in
Omega(n logn) and maybe also in O(n logn). The performance tends to tell that, some outputs
as well but I can't really prove it.
Anyway. You provide a list of points (tuples with x,y-coordinates!) and get back a list of
triangles (also tuples with three points per triangle!).

* **Image-Triangulation**:

This is the actual application of the delaunay-triangulation. You can specify a .jpg-Image
and the program will perform some gauss-filtering and edge detection. Based on the contrast
difference of the image there is a propability that a point is set on that spot (per pixel).
With that there will be more points generated in areas with high contrast differences than
in areas with equal colors and contrasts.
These points will then be triangulated.
After that each triangle will get colored with the approximate color of the pixels inside
the triangle. Approximate because only the Vertices and the center of the triangle will be
considered.
These colored triangles will then be rendered into an new jpg-image.

* **Voronoi-Diagrams:**

The voronoi-diagram-part of the program is still to be done.
The idea is to take the delaunay-triangulation and transform it to voronoi-regions.
The regions will then be rendered and colored just like the triangles before.
It might look a little better or at least interesting :)

