
Automating GIS-processes - Lecture 6: Python GIS
================================================

**What we have learned this far - Where to find help?**

At this point we have learned the basics of Python programming and used
Python to automate processes in ArcGIS using arcpy module. If you have
ArcGIS installation available (as we have at the University of Helsinki)
it is quite straightforward to continue working with arcpy module and
start building scripts that automatize and solve your own
GIS-tasks/problems. ArcGIS has good
`documentation <http://resources.arcgis.com/en/help/main/10.2/>`__ and
fairly active `user
community <https://geonet.esri.com/community/discussions-lobby>`__ that
can help you achieving your goals. You can also search answers for your
problems just by 'Googling' it. Highly active user community for coders
is `StackOverFlow <http://stackoverflow.com/>`__ from where you most
probably find answers/help to different problems or errors that you
might get while writing your own codes. Also
`gis.StackExchange <http://gis.stackexchange.com/>`__ is a user
community that is focused ecpecially on GIS stuff, thus it can be really
useful site to visit.

In addition to the online materials, there are various books that can
help you going especially in the beginning of your "programming career":

-  `Python Scripting for
   ArcGIS <http://www.amazon.com/Python-Scripting-ArcGIS-Paul-Zandbergen/dp/1589482824/ref=pd_bxgy_14_img_2/175-2574462-6134540?ie=UTF8&refRID=0HZHB9BQQWD4SKA1017A>`__
   (also `available in
   HELKA <https://helka.linneanet.fi/cgi-bin/Pwebrecon.cgi?BBID=2632928>`__)
-  `Learning Geospatial Analysis with
   Python <http://www.amazon.com/Learning-Geospatial-Analysis-Python-Lawhead/dp/1783281138>`__
-  `Python Geospatial
   Development <http://www.amazon.com/Python-Geospatial-Development-Second-Edition/dp/178216152X>`__
-  `Python for Data Analysis: Data wrangling with Pandas, NumPy and
   iPython <http://www.amazon.com/Python-Data-Analysis-Wrangling-IPython/dp/1449319793>`__

GIS with 'pure' Python
~~~~~~~~~~~~~~~~~~~~~~

***Why not to use specific GIS software for GIS programming?***

Using a specific GIS software such as ArcGIS can be a nice way to start
programming different GIS/geoprocessing functionalities with Python
since all the functionalities are gathered under a single module, i.e.
arcpy. However there are different reasons why you could want to move
away from using e.g. ArcGIS:

-  you don't have the lisence to use ArcGIS (which is fairly expensive)
-  you are not happy with some of the functionalities that ArcGIS has
   (yes, there are bugs in the software and some functionalities such as
   working with attribute-tables are extremely slow in ArcGIS)
-  you would like to support open source softwares/codes and open
   science that makes all of your work reproducible for everyone
-  you would like to more easily plug-in and chain all sorts of
   third-party softwares that makes it possible to build e.g. as fancy
   web-GIS applications as you want (using e.g.
   `GeoDjango <https://docs.djangoproject.com/en/1.8/ref/contrib/gis/>`__
   with `PostGIS <http://postgis.net/>`__ as a back-end)
-  you would like to LEARN and UNDERSTAND much more deeply how different
   geoprocessing operations work

Introduction to Python GIS
~~~~~~~~~~~~~~~~~~~~~~~~~~

When starting to do GIS analyses/operations using pure Python we move
away slightly from the *world of scripting*. When you are *scripting* it
means that you are programming using only a single software or framework
such as arcpy or R (statistical software). In *"real"* programming it is
fairly common that you are using multiple different
libraries/modules/softwares/frameworks that have been developed
independently by different companies, communities, groups of people or
just individual persons.

Thus, when doing data analysis or GIS with Python there are various
modules that can help you get going:

-  **Data analysis & visualization:**

   -  `numpy <http://www.numpy.org/>`__ --> Fundamental package for
      scientific computing with Python
   -  `pandas <http://pandas.pydata.org/>`__ --> High-performance,
      easy-to-use data structures and data analysis tools
   -  `scipy <http://www.scipy.org/about.html>`__ --> A collection of
      numerical algorithms and domain-specific toolboxes, including
      signal processing, optimization and statistics
   -  `matplotlib <http://matplotlib.org/>`__ --> Basic plotting library
      for Python
   -  `bokeh <http://bokeh.pydata.org/en/latest/>`__ --> Interactive
      visualizations (also maps) for the web

-  **GIS:**

   -  `gdal <http://www.gdal.org/>`__ --> Fundamental package for
      processing vector and raster data formats (many modules below
      depend on this)
   -  `geopandas <http://geopandas.org/#description>`__ --> Working with
      geospatial data in Python made easier, combines the capabilities
      of pandas and shapely.
   -  `shapely <http://toblerity.org/shapely/manual.html>`__ --> Python
      package for manipulation and analysis of planar geometric objects
      (based on widely deployed `GEOS <https://trac.osgeo.org/geos/>`__)
   -  `fiona <https://pypi.python.org/pypi/Fiona>`__ --> Reading and
      writing spatial data (alternative for geopandas)
   -  `pyproj <https://pypi.python.org/pypi/pyproj?>`__ --> Performs
      cartographic transformations and geodetic computations (based on
      `PROJ.4 <http://trac.osgeo.org/proj>`__)
   -  `pysal <https://pysal.readthedocs.org/en/latest/>`__ --> Library
      of spatial analysis functions written in Python
   -  `cartopy <http://scitools.org.uk/cartopy/docs/latest/index.html>`__
      --> Make drawing maps for data analysis and visualisation as easy
      as possible
   -  `scipy.spatial <http://docs.scipy.org/doc/scipy/reference/spatial.html>`__
      --> Spatial algorithms and data structures
   -  `rtree <http://toblerity.org/rtree/>`__ --> Spatial indexing for
      Python for quick spatial lookups
   -  `rasterio <https://github.com/mapbox/rasterio>`__ --> Clean and
      fast and geospatial raster I/O for Python
   -  `RSGISLib <http://www.rsgislib.org/index.html#python-documentation>`__
      --> Remote Sensing and GIS Software Library for Python

Geometric Objects - Spatial Data Model
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

 *Fundamental geometric objects that can be used in Python with
**Shapely ** module*

The most fundamental geometric objects are **Points**, **Lines** and
**Polygons** which are the basic ingredients when working with spatial
data in vector format. Python has a specific module called **Shapely**
that can be used to create and work with *Geometric Objects*. There are
many useful functionalities that you can do with Shapely such as:

-  Create **Line**\ (s) or **Polygon**\ (s) from a ***Collection*** of
   **Point** geometries
-  Calculate areas/length/bounds etc. of input geometries
-  Make geometric operations based on the input geometries such as
   **Union**, **Difference**, **Distance** etc.
-  Make spatial queries between geometries such **Intersects**,
   **Touches**, **Crosses**, **Within** etc.

**Geometric Objects consist of coordinate tuples where:**

-  ***Point*** object consists of a single coordinate-tuple (
   examplePoint = Point(x-coord, y-coord) )
-  ***LineString*** object (i.e. a line) consists of a list of at least
   two coordinate tuples ( exampleLine = LineString([(x1, y1), (x2,
   y2)]) )
-  ***Polygon*** object consists of a list of at least three coordinate
   tuples that forms the outerior ring ( examplePoly = Polygon([(x1,
   y1), (x2, y2), (x3,y3)]) ) and a (possible) list of hole polygons.

**It is also possible to have collections of geometric objects (e.g.
Polygons with multiple parts):**

-  ***MultiPoint*** object consists of a list of coordinate-tuples (
   examplePoints = MultiPoint([(-2.2, 24.5), (12.9, -43.7)]) )
-  ***MultiLineString*** object consists of a list of line-like
   sequences ( exampleLines = MultiLineString([((0, 0), (1, 1)), ((-1,
   0), (1, 0))]) )
-  ***MultiPolygon*** object consists of a list of polygon-like
   sequences that construct from exterior ring and (possible) hole list
   tuples ( [((a1, ..., aM), [(b1, ..., bN), ...]), ...] )

Creating Geometric Objects with Shapely
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Following examples show how geometric objects can be created in Python
using **Shapely** module, and how different properties of those
geometric objects can be accessed.

*Point*
-------

.. code:: python

    # Import necessary geometric objects from shapely module
    from shapely.geometry import Point, LineString, Polygon
    
    # Create Point geometric object(s) with coordinates
    point1 = Point(2.2, 4.2)
    point2 = Point(7.2, -25.1)
    point3 = Point(9.7, -2.456)
    
    # Let's see what the variables look like
    print(point1)
    print(point2)
    
    # Outputs:


.. parsed-literal::

    POINT (2.2 4.2)
    POINT (7.2 -25.1)
    

***It is possible to calculate the distance between the points:***

.. code:: python

    # Calculate the distance between point1 and point2
    point_dist = point1.distance(point2)
    print("Distance between the points is {0:.2f} decimal degrees".format(point_dist))
    
    # Outputs:


.. parsed-literal::

    Distance between the points is 29.72 decimal degrees
    

*LineString*
~~~~~~~~~~~~

.. code:: python

    # Create a LineString from those points
    line = LineString([point1, point2, point3])
    
    # OR use coordinate tuples --> same outcome
    line2 = LineString([(2.2, 4.2), (7.2, -25.1), (9.7, -2.456)])
    
    # Let's see how our LineString looks like
    print(line)
    
    # Outputs:


.. parsed-literal::

    LINESTRING (2.2 4.2, 7.2 -25.1, 9.699999999999999 -2.456)
    

***It is possible to calculate e.g. the length or centroid of the
line***

.. code:: python

    # Get the length of our line
    line_length = line.length
    print("Length of our line: ", line_length)
    
    # Get the centroid of the line
    line_centroid = line.centroid
    print("Centroid of our line: ", line_centroid)
    
    # Outputs:


.. parsed-literal::

    Length of our line:  52.5051473323406
    Centroid of our line:  POINT (6.327096733177681 -11.89399411413742)
    

*Polygon*
~~~~~~~~~

.. code:: python

    # Create a Polygon from coordinates
    poly = Polygon([(2.2, 4.2), (7.2, -25.1), (9.7, -2.456)])
    
    # OR use our previously created Point objects (same outcome) --> notice that Polygon object requires x,y coordinates as input
    poly2 = Polygon([[p.x, p.y] for p in [point1, point2, point3]])
    
    # Let's see how our Polygon looks like
    print(poly)


.. parsed-literal::

    POLYGON ((2.2 4.2, 7.2 -25.1, 9.699999999999999 -2.456, 2.2 4.2))
    

***Access different geometric properties of the Polygon - centroid,
area, bounds, exterior etc.***

.. code:: python

    # Get the centroid of the Polygon
    poly_centroid = poly.centroid
    print("Poly centroid: ", poly_centroid)
    
    # Get the area of the Polygon
    poly_area = poly.area
    print("Poly Area: ", poly_area)
    
    # Get the bounds of the Polygon (i.e. bounding box)
    poly_bbox = poly.bounds
    print("Poly Bounding Box: ", poly_bbox)
    
    # Get the exterior of the Polygon
    poly_ext = poly.exterior
    print("Poly Exterior: ", poly_ext)
    
    # Get the length of the exterior
    poly_ext_length = poly_ext.length
    print("Poly Exterior Length: ", poly_ext_length)
    
    # Outputs:


.. parsed-literal::

    Poly centroid:  POINT (6.366666666666667 -7.785333333333333)
    Poly Area:  93.23499999999999
    Poly Bounding Box:  (2.2, -25.1, 9.7, 4.2)
    Poly Exterior:  LINEARRING (2.2 4.2, 7.2 -25.1, 9.699999999999999 -2.456, 2.2 4.2)
    Poly Exterior Length:  62.53272610291129
    

*Collections of Geometric Objects*
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

It is possible to have a collection of geometric objects, such as
MultiPoint:

.. code:: python

    # Import collections of geometric objects
    from shapely.geometry import MultiPoint, MultiLineString, MultiPolygon
    
    # Create a MultiPoint object of our points 1,2 and 3
    multiP = MultiPoint([point1, point2, point3])
    
    # Let's see what's inside
    print(multiP)
    
    # It is possible to get the Convex Hull of those points --> https://en.wikipedia.org/wiki/Convex_hull
    convex = multiP.convex_hull
    print("Convex hull of the points: ", convex)
    
    # Outputs:


.. parsed-literal::

    MULTIPOINT (2.2 4.2, 7.2 -25.1, 9.699999999999999 -2.456)
    Convex hull of the points:  POLYGON ((7.2 -25.1, 2.2 4.2, 9.699999999999999 -2.456, 7.2 -25.1))
    

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
### Practice constructing Geometric Objects in Python by doing Exercise
8 in Moodle
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
