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

.. ipython:: python
  :suppress:

    # THIS CODE WILL BE RUNNING IN BACKGROUND
    # ---------------------------------------
    import gdal
    import pandas as pd
    import geopandas as gpd
    from shapely.geometry import Point
    from geopandas.tools import geocode
    import os
    fp = os.path.join(os.path.abspath('data'), "addresses.txt")
    data = pd.read_csv(fp, sep=';')
    key = 'AIzaSyAwNVHAtkbKlPs-EEs3OYqbnxzaYfDF2_8'
    geo = geocode(data['address'], api_key=key)

.. ipython:: python

    # Join tables by using a key column 'address'
    join = geo.merge(data, on='address')

    # Let's see what we have
    join.head()

- Let's also check the data type of our new ``join`` table

.. ipython:: python

    type(join)

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


.. todo::

  **Task**:

  Make a map out of the points. What do you think that the
  addresses are representing?
