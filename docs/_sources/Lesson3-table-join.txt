Table join
==========

Table joins are again something that you need to really frequently when
doing GIS analyses. Combining data from different tables based on common
``key`` attribute can be done easily in Pandas/Geopandas using
`.merge() <http://pandas.pydata.org/pandas-docs/stable/generated/pandas.DataFrame.merge.html>`__
-function.

-  Let's continue with our `geocoding task <Lesson3-geocoding.html#geocoding-in-geopandas>`_ and join the ``data`` and ``geo`` DataFrames together based on
   common column ``address``. Parameter ``on`` is used to determine the
   common key in the tables. If your key in the first table would be
   named differently than in the other one, you can also specify them
   separately for each table by using ``left_on`` and ``right_on``
   -parameters.

.. code:: python

    # Join tables by using a key column 'address'
    join = geo.merge(data, on='address')

    # Let's see what we have
    >>> print(join.head())
                                                 address
    0              Kampinkuja 1, 00100 Helsinki, Finland
    1               Kaivokatu 8, 00101 Helsinki, Finland
    2  Hermanstads strandsväg 1, 00580 Helsingfors, F...
    3                  Itäväylä, 00900 Helsinki, Finland
    4         Tyynenmerenkatu 9, 00220 Helsinki, Finland

                                   geometry    id
    0         POINT (24.9301701 60.1683731)  1001
    1         POINT (24.9418933 60.1698665)  1002
    2  POINT (24.9774004 60.18735880000001)  1003
    3  POINT (25.0919641 60.21448089999999)  1004
    4         POINT (24.9214846 60.1565781)  1005


- Let's also check the data type of our new ``join`` table

.. code:: python

    >>> type(join)
    geopandas.geodataframe.GeoDataFrame

As a result we have a new GeoDataFrame called ``join`` where we now have
all original columns plus a new column for ``geometry``.

-  Now it is easy to save our address points into a Shapefile

.. code:: python

    # Output file path
    outfp = r"/home/geo/addresses.shp"

    # Save to Shapefile
    join.to_file(outfp)

That's it. Now we have successfully geocoded those addresses into Points
and made a Shapefile out of them.

**Task**: Make a map out of the points. What do you think that the
addresses are representing?
