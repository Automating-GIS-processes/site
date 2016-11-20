Point in Polygon & Intersect
============================

Finding out if a certain point is located inside or outside of an area,
or finding out if a line intersects with another line or polygon are
fundamental geospatial operations that are often used e.g. to select
data based on location. Such spatial queries are one of the typical
first steps of the workflow when doing spatial analysis. Performing a
spatial join (will be introduced later) between two spatial datasets is
one of the most typical applications where Point in Polygon (PIP) query
is used.

**Sources**

Following materials are partly based on documentation of `Shapely <http://toblerity.org/shapely/manual.html>`_, `Geopandas <http://geopandas.org/geocoding.html>`__ and `Lawhead, J. (2013), Chapters I and V <https://www.packtpub.com/application-development/learning-geospatial-analysis-python>`_.

How to check if point is inside a polygon?
------------------------------------------

Computationally, detecting if a point is inside a polygon is most
commonly done using a specific formula called `Ray Casting
algorithm <https://en.wikipedia.org/wiki/Point_in_polygon#Ray_casting_algorithm>`__.
Luckily, we do not need to create such a function ourselves for
conducting the Point in Polygon (PIP) query. Instead, we can take
advantage of `Shapely's binary
predicates <http://toblerity.org/shapely/manual.html#binary-predicates>`__
that can evaluate the topolocical relationships between geographical
objects, such as the PIP as we're interested here.

There are basically two ways of conducting PIP in Shapely:

1. using a function called
   `.within() <http://toblerity.org/shapely/manual.html#object.within>`__
   that checks if a point is within a polygon
2. using a function called
   `.contains() <http://toblerity.org/shapely/manual.html#object.contains>`__
   that checks if a polygon contains a point

Notice: even though we are talking here about **Point** in Polygon
operation, it is also possible to check if a LineString or Polygon is
inside another Polygon.

-  Let's first create a Polygon using a list of coordinate-tuples and a
   couple of Point objects

.. ipython:: python
   :suppress:

    import gdal
    from shapely.geometry import Point, Polygon
    p1 = Point(24.952242, 60.1696017)
    p2 = Point(24.976567, 60.1612500)
    coords = [(24.950899, 60.169158), (24.953492, 60.169158), (24.953510, 60.170104), (24.950958, 60.169990)]
    poly = Polygon(coords)

.. code:: python

    from shapely.geometry import Point, Polygon

    # Create Point objects
    p1 = Point(24.952242, 60.1696017)
    p2 = Point(24.976567, 60.1612500)

    # Create a Polygon
    coords = [(24.950899, 60.169158), (24.953492, 60.169158), (24.953510, 60.170104), (24.950958, 60.169990)]
    poly = Polygon(coords)


.. ipython:: python

    # Let's check what we have
    print(p1)
    print(p2)
    print(poly)

-  Let's check if those points are ``within`` the polygon

.. ipython:: python

    # Check if p1 is within the polygon using the within function
    p1.within(poly)
    
    # Check if p2 is within the polygon
    p2.within(poly)

Okey, so we can see that the first point seems to be inside that polygon
and the other one doesn't.

-  In fact, the first point is close to the center of the polygon as we
   can see:

.. ipython:: python

    # Our point
    print(p1)

    # The centroid
    print(poly.centroid)

-  It is also possible to do PIP other way around, i.e. to check if
   polygon contains a point:

.. ipython:: python

    # Does polygon contain p1?
    poly.contains(p1)

    # Does polygon contain p2?
    poly.contains(p2)

Thus, both ways of checking the spatial relationship results in the same way.

Which one should you use then? Well, it depends:

-  if you have many points and just one polygon and you try to find out
   which one of them is inside the polygon:

   -  you need to iterate over the points and check one at a time if it
      is **within()** the polygon specified

-  if you have many polygons and just one point and you want to find out
   which polygon contains the point

    -  you need to iterate over the polygons until you find a polygon that
       **contains()** the point specified (assuming there are no overlapping
       polygons)

Intersect
---------

Another typical geospatial operation is to see if a geometry
`intersect <http://toblerity.org/shapely/manual.html#object.intersects>`__
or `touches <http://toblerity.org/shapely/manual.html#object.touches>`__
another one. The difference between these two is that:

-  if objects intersect, the boundary and interior of an object needs to
   intersect in any way with those of the other.

-  If an object touches the other one, it is only necessary to have (at
   least) a single point of their boundaries in common but their
   interiors shoud NOT intersect.

Let's try these out.

-  Let's create two LineStrings

.. ipython:: python
   :suppress:

    # THIS CODE WILL NOT BE SHOWN, THE ONE BELOW IS!
    from shapely.geometry import LineString, MultiLineString
    line_a = LineString([(0, 0), (1, 1)])
    line_b = LineString([(1, 1), (0, 2)])

.. code:: python

    from shapely.geometry import LineString, MultiLineString

    # Create two lines
    line_a = LineString([(0, 0), (1, 1)])
    line_b = LineString([(1, 1), (0, 2)])

-  Let's see if they intersect

.. ipython:: python

    line_a.intersects(line_b)

-  Do they also touch each other?

.. ipython:: python

    line_a.touches(line_b)

Indeed, they do and we can see this by plotting the features together

.. ipython:: python

    # Create a MultiLineString
    multi_line = MultiLineString([line_a, line_b])
    multi_line;

.. image:: Lesson3-point-in-polygon_files/Lesson3-point-in-polygon_16_0.svg

Thus, the ``line_b`` continues from the same node ( (1,1) ) where ``line_a`` ends.

However, if the lines overlap fully, they don't touch due to the spatial relationship rule, as we can see:

- Check if line_a touches itself

.. ipython:: python

    # Does the line touch with itself?
    line_a.touches(line_a)

- It does not. However, it does intersect

.. ipython:: python

    # Does the line intersect with itself?
    line_a.intersects(line_a)
