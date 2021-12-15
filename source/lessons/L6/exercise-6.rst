Exercise 6
==========

.. admonition:: Start your assignment

    You can start working on your copy of Exercise 6 by `accepting the GitHub Classroom assignment <https://classroom.github.com/a/AdmQdIHc>`__.

 **Exercise 6 is due by Thursday 23rd of December at 5pm**.

You can also take a look at the open course copy of `Exercise 6 in the course GitHub repository <https://github.com/AutoGIS-2021/Exercise-6>`__ (does not require logging in).
Note that you should not try to make changes to this copy of the exercise, but rather only to the copy available via GitHub Classroom.

Hints
-----

Defining the graph extent
~~~~~~~~~~~~~~~~~~~~~~~~~~~~
First, combine the point data sets, for example, by using the Pandas `append() <https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.append.html>`__ method (adds rows from one DataFrame to the other).
Then, specify the extent Polygon using a convex hull or a bounding box + a little buffer (the buffer enables the routes to go beyond the extent of the point layers!).
When creating the buffer, remember that the coordinates are in decimal degrees!

**Option 2 - Bounding box:**
Specify a Polygon that represents the **bounding box** of the combined points;

- First, define the bounds:
    - Once you have all origin and destination points in one GeoDataFrame,
you can get the corner coordinates of the bounding box from the `total_bounds <http://geopandas.org/reference.html#geopandas.GeoSeries.total_bounds>`__ of the geometry-column.
    - Note: the resulting coordinates from the `total_bounds` are in this order: `[xmin, ymin, xmax, ymax]`
- Next, you need to define a shapely polygon based on the bounding box coordinates.
    - In order to create the shapely Polygon, we need to organize the bbox coordinates into a list of coordinate pairs for example like this:
`bbox_coords = [[xmin, ymax], [xmin, ymin], [xmax, ymin], [xmax, ymax]]`
    - You can create the list of coordinate pairs based on the total bounds. Store the total bounds first into a list, and then create the coordinate pairs.
    - You can insert the coordinates into the list one by one. If `bounds` is a list that contains the total bounds of our input coordinates, then we can get xmin like this: `bounds[0]`.
- Finally, buffer the bounding box polygon (eg. adding 0.05 decimal degrees to the extent using Shapely's `buffer <https://shapely.readthedocs.io/en/stable/manual.html#object.buffer>`__ method)

**Option 2 - Convex hull:**
- Specify a Polygon that represents the **convex hull** of the combined points like we did in `Lesson 1 <https://autogis-site.readthedocs.io/en/latest/notebooks/L1/geometric-objects.html#convex-hull-and-envelope>`__
    - First, create a MultiPolygon of the points (eg. using `unary_union`)
    - Then, you can access the `convex_hull` of that MultiPolygon object
- Finally, buffer the convex hull polygon (eg. adding 0.1 decimal degrees to the extent using Shapely's `buffer <https://shapely.readthedocs.io/en/stable/manual.html#object.buffer>`__ method)

