Nearest Neighbour Analysis
==========================

One commonly used GIS task is to be able to find the nearest neighbour. For instance, you might have a single Point object
representing your home location, and then another set of locations representing e.g. public transport stops. Then, quite typical question is *"which of the stops is closest one to my home?"*
This is a typical nearest neighbour analysis, where the aim is to find the closest geometry to another geometry.

In Python this kind of analysis can be done with shapely function called ``nearest_points()`` that `returns a tuple of the nearest points in the input geometrie <https://shapely.readthedocs.io/en/latest/manual.html#shapely.ops.nearest_points>`__.

Nearest point using Shapely
---------------------------

Let's start by testing how we can find the nearest Point using the ``nearest_points()`` function of Shapely.

Let's create an origin Point and a few destination Points and find out the closest destination.

.. ipython:: python

    from shapely.geometry import Point, MultiPoint
    from shapely.ops import nearest_points

    orig = Point(1, 1.67)
    dest1, dest2, dest3 = Point(0, 1.45), Point(2, 2), Point(0, 2.5)

To be able to find out the closest destination point from the origin, we need to create a MultiPoint object from the destination points.

.. ipython:: python

    destinations = MultiPoint([dest1, dest2, dest3])
    print(destinations)

Okey, now we can see that all the destination points are represented as a single MultiPoint object.

- Now we can find out the nearest destination point by using ``nearest_points()`` function.

.. ipython:: python

    nearest_geoms = nearest_points(orig, destinations)
    near_idx0 = nearest_geoms[0]
    near_idx1 = nearest_geoms[1]
    print(nearest_geoms)
    print(near_idx0)
    print(near_idx1)

As you can see the ``nearest_points()`` function returns a tuple of geometries where the first item is the geometry
of our origin point and the second item (at index 1) is the actual nearest geometry from the destination points.
Hence, the closest destination point seems to be the one located at coordinates (0, 1.45).

This is the basic logic how we can find the nearest point from a set of points.

Nearest points using Geopandas
------------------------------

Of course, the previous example is not really useful yet. Hence, next I show, how it is possible to find nearest points
from a set of origin points to a set of destination points using GeoDataFrames. If you don't already have the addresses and PKS_suuralueet.kml datasets,
you can find and download them from :doc:`geocoding <geocoding>` and :doc:`Point in Polygon <point-in-polygon>` tutorials.

- First we need to create a function that takes advantage of the previous function but is tailored to work with two GeoDataFrames.

.. code:: python

    def nearest(row, geom_union, df1, df2, geom1_col='geometry', geom2_col='geometry', src_column=None):
        """Find the nearest point and return the corresponding value from specified column."""
        # Find the geometry that is closest
        nearest = df2[geom2_col] == nearest_points(row[geom1_col], geom_union)[1]
        # Get the corresponding value from df2 (matching is based on the geometry)
        value = df2[nearest][src_column].get_values()[0]
        return value

.. ipython:: python
    :suppress:

        def nearest(row, geom_union, df1, df2, geom1_col='geometry', geom2_col='geometry', src_column=None):
            nearest = df2[geom2_col] == nearest_points(row[geom1_col], geom_union)[1]
            value = df2[nearest][src_column].get_values()[0]
            return value

Next we read the address data and the Helsinki districts data and find out the closest address to the centroid of each district.

.. ipython:: python
    :suppress:

        import geopandas as gpd
        fp1 = r"C:\HY-DATA\HENTENKA\KOODIT\Opetus\Automating-GIS-processes\2017\data\PKS_suuralue.kml"
        fp2 = r"C:\HY-DATA\HENTENKA\KOODIT\Opetus\Automating-GIS-processes\2017\data\addresses.shp"
        gpd.io.file.fiona.drvsupport.supported_drivers['KML'] = 'rw'

        df1 = gpd.read_file(fp1, driver='KML')
        df2 = gpd.read_file(fp2)

.. code:: python

    In [7]: import geopandas as gpd

    In [8]: fp1 = "/home/geo/PKS_suuralue.kml"
    In [9]: fp2 = "/home/geo/addresses.shp"
    In [10]: gpd.io.file.fiona.drvsupport.supported_drivers['KML'] = 'rw'

    In [11]: df1 = gpd.read_file(fp1, driver='KML')
    In [12]: df2 = gpd.read_file(fp2)

Create unary union from Points, which basically creates a MultiPoint object from the Point geometries.

.. ipython:: python

    unary_union = df2.unary_union
    print(unary_union)

Calculate the centroids for each district area.

.. ipython:: python

    df1['centroid'] = df1.centroid
    df1.head()

Okey now we are ready to use our function and find closest Points (taking the value from id column) from df2 to df1 centroids

.. ipython:: python

    df1['nearest_id'] = df1.apply(nearest, geom_union=unary_union, df1=df1, df2=df2, geom1_col='centroid', src_column='id', axis=1)
    df1.head(20)

That's it! Now we found the closest point for each centroid and got the ``id`` value from our addresses into the ``df1`` GeoDataFrame.


