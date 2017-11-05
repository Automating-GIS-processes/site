Exercise 2 hints
================

Converting Pandas DataFrame into a GeoDataFrame
-----------------------------------------------

Quite often you are in a situation where you have read data e.g. from text file into a Pandas DataFrame where you have latitude and longitude columns representing the location of a record.

- Let's continue with the previous example and consider that we have a column where we have stored the shapely geometries:

.. code:: python

     >>> print(data)
         value  lat  lon     geometry
     0      0    2    4  POINT (4 2)
     1      5    1    6  POINT (6 1)
     2      2    6    1  POINT (1 6)
     3      6    6    3  POINT (3 6)
     4      5    5    1  POINT (1 5)


- Notice that now our data is still a Pandas **DataFrame**, not a GeoDataFrame:

.. code:: python

    >>> type(data)
    pandas.core.frame.DataFrame


- We need to convert the DataFrame into a GeoDataFrame, so that we can e.g. save it into a Shapefile. It is easily done by passing the DataFrame into a GeoDataFrame object. We need to determine
 which column contains the geometry information (needs to be always a column called 'geometry'), and optionally we can also determine the coordinate reference system when creating the GeoDataFrame:

.. code:: python

    # Convert DataFrame into a GeoDataFrame
    geo = gpd.GeoDataFrame(data, geometry='geometry', crs=from_epsg(4326))

    >>> type(geo)
    geopandas.geodataframe.GeoDataFrame

    >>> geo.crs
    {'init': 'epsg:4326', 'no_defs': True}

Now we have converted Pandas DataFrame into a proper GeoDataFrame that we can export into a Shapefile for instance.