Exercise 2
==========

.. image:: https://img.shields.io/badge/launch-CSC%20notebook-blue.svg
   :target: https://notebooks.csc.fi/#/blueprint/d189695c52ad4c0d89ef72572e81b16c

.. admonition:: Start your assignment

    You can start working on your copy of Exercise 2 by `accepting the GitHub Classroom assignment <https://classroom.github.com/a/hkn1jd7L>`__.

    **Exercise 2 is due by 5pm on Thursday the 18th of November 2021** (day before the next practical session).

You can also take a look at the open course copy of `Exercise 2 in the course GitHub repository <https://github.com/AutoGIS-2021/Exercise-2>`__ (does not require logging in).
Note that you should not try to make changes to this copy of the exercise, but rather only to the copy available via GitHub Classroom.


.. admonition:: Pair programming (optional!)

    Students attending the course in Helsinki **can continue working in pairs**.
    See more information in Slack, and in week 2: `Why are we working in pairs? <https://geo-python-site.readthedocs.io/en/latest/lessons/L2/why-pairs.html>`_.
    However, each student should submit their own copy of the exercise.


Hints
-----

Converting Pandas DataFrame into a GeoDataFrame
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Quite often you are in a situation where you have read data e.g. from text file into a pandas DataFrame where you have latitude and longitude columns representing the location of a record. The first step is to create a column where with corresponding the shapely geometries:

.. code:: python

     >>> print(data)
         value  lat  lon     geometry
     0      0    2    4  POINT (4 2)
     1      5    1    6  POINT (6 1)
     2      2    6    1  POINT (1 6)
     3      6    6    3  POINT (3 6)
     4      5    5    1  POINT (1 5)


- Notice that the data is still a pandas **DataFrame**, not a GeoDataFrame:

.. code:: python

    >>> type(data)
    pandas.core.frame.DataFrame


- We need to convert the DataFrame into a GeoDataFrame, so that we can e.g. save it into a Shapefile. It is easily done by passing the DataFrame into a GeoDataFrame object. We need to determine which column contains the geometry information (needs to be always a column called 'geometry'), and optionally we can also determine the coordinate reference system when creating the GeoDataFrame:

.. code:: python

    import geopandas as gpd
    from pyproj import CRS

    # Convert DataFrame into a GeoDataFrame
    geo = gpd.GeoDataFrame(data, geometry='geometry', crs=CRS.from_epsg(4326).to_wkt())

    >>> type(geo)
    geopandas.geodataframe.GeoDataFrame

Now we have converted Pandas DataFrame into a proper GeoDataFrame that we can export into a Shapefile for instance.



Alternatives for iterrows
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

In exercise 2, problem 2 you need to create Shapely Points for each row of data. Our input data set is rather large, so the iterrows-approach will be rather slow. You can try this approach, but prepare to wait for a while for the code to run!

.. code:: python

    #-----------------------------------------

    # OPTION 1: Iterate over dataframe rows:
    for idx, row in df.iterrows():

        # create a point based on x and y column values on this row:
        point = Point(row['x'], row['y'])

        # Add the point object to the geometry column on this row:
        df.at[idx, 'geometry'] = point



There are other **faster** solutions for this. Check out the following examples, and try to understand what happens in them. Pick one of these solutions and use it in problem 2 :) You'll need to change the variable and column names.

.. code:: python

    #-----------------------------------------

    # OPTION 2: apply a function

    # Define a function for creating points from row values
    def create_point(row):
        '''Returns a shapely point object based on values in x and y columns'''

        point = Point(row['x'], row['y'])

        return point

    # Apply the function to each row
    df['geometry'] = df.apply(create_point, axis=1)

    #-----------------------------------------


    # OPTION 3: apply a lambda function
    # see: https://docs.python.org/3.5/tutorial/controlflow.html#lambda-expressions

    df['geometry'] = df.apply(lambda row: Point(row['x'], row['y']), axis=1)

    #-----------------------------------------

    # OPTION 4: zip and for-loop

    geom = []
    for x, y in zip(df['x'], df['y']):
        geom.append(Point(x, y))

    df['geometry'] = geom
    

Setting userid as index (optional!)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ 
When creating the `movements` geodataframe, it might be useful to pre-define the index like this: `index = data["userid"].unique()` when using the `gpd.GeoDataFrame()` constructor. Later on, you can use this index when adding geometries to that geodataframe.

Adding items to a (Geo)DataFrame
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ 

In this exercise, you need to add/append items to a (geo)dataframe iteratively (one row at a time). When adding new information to a dataframe, you can use the `.at` or `.loc` indexer like in this example: 

.. code:: python

    # Add a point object into the geometry-column on the first row (here, the row-label is 0)
    df.at[0, 'geometry'] = point
    

As an alternative, you can also add new rows of data using the `append method <http://pandas.pydata.org/pandas-docs/stable/generated/pandas.DataFrame.append.html>`__.
