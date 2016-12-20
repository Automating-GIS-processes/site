Introduction to Geopandas
=========================

Reading a Shapefile
-------------------

Spatial data can be read easily with geopandas using ``gpd.from_file()``
-function:

.. ipython:: python

    @suppress
    import gdal
    
    # Import necessary modules
    import geopandas as gpd

    # Set filepath (fix path relative to yours)
    fp = "/home/geo/Data/DAMSELFISH_distributions.shp"

    @suppress
    import os

    @suppress
    """ NOTICE: Following is the real path to the data, the one above is for online documentation to reflect the situation at computing instance """

    @suppress
    fp = os.path.join(os.path.abspath('data'), "DAMSELFISH_distributions.shp")

    # Read file using gpd.read_file()
    data = gpd.read_file(fp)

- Let's see what datatype is our 'data' variable

.. ipython:: python

   type(data)

Okey so from the above we can see that our ``data`` -variable is a
**GeoDataFrame**. GeoDataFrame extends the functionalities of
**pandas.DataFrame** in a way that it is possible to use and handle
spatial data within pandas (hence the name geopandas). GeoDataFrame have
some special features and functions that are useful in GIS.

-  Let's take a look at our data and print the first 5 rows using the
   ``head()`` -function prints the first 5 rows by default

.. ipython:: python

    data.head()

-  Let's also take a look how our data looks like on a map. If you just
   want to explore your data on a map, you can use ``.plot()`` -function
   in geopandas that creates a simple map out of the data (uses
   matplotlib as a backend):

.. ipython:: python

   @savefig damselfish.png width=5in
   data.plot();

Coordinate reference system (CRS)
---------------------------------

GeoDataFrame that is read from a Shapefile contains *always* (well not
always but should) information about the coordinate system in which the
data is projected.

-  We can see the current coordinate reference system from ``.crs``
   attribute:

.. ipython:: python

    data.crs

Okey, so from this we can see that the data is something called
**epsg:4326**. The EPSG number (*"European Petroleum Survey Group"*) is
a code that tells about the coordinate system of the dataset. "`EPSG
Geodetic Parameter Dataset <http://www.epsg.org/>`__ is a collection of
definitions of coordinate reference systems and coordinate
transformations which may be global, regional, national or local in
application". EPSG-number 4326 that we have here belongs to the WGS84
coordinate system (i.e. coordinates are in decimal degrees (lat, lon)).
You can check easily different epsg-codes from `this
website <http://spatialreference.org/ref/epsg/>`__.

Writing a Shapefile
-------------------

Writing a new Shapefile is also something that is needed frequently.

-  Let's select 50 first rows of the input data and write those into a
   new Shapefile by first selecting the data using index slicing and
   then write the selection into a Shapefile with ``gpd.to_file()``
   -function:

.. code:: python

    # Create a output path for the data
    out = r"/home/geo/Data/DAMSELFISH_distributions_SELECTION.shp"

    # Select first 50 rows
    selection = data[0:50]

    # Write those rows into a new Shapefile (the default output file format is Shapefile)
    selection.to_file(out)

**Task:** Open the Shapefile now in QGIS that has been installed into
our computer instance, and see how the data looks like.

Geometries in Geopandas
-----------------------

Geopandas takes advantage of Shapely's geometric objects. Geometries are
stored in a column called *geometry* that is a default column name for
storing geometric information in geopandas.

-  Let's print the first 5 rows of the column 'geometry':

.. ipython:: python

    # It is possible to use only specific columns by specifying the column name within square brackets []
    data['geometry'].head()

Since spatial data is stored as Shapely objects, **it is possible to use
all of the functionalities of Shapely module** that we practiced
earlier.

-  Let's print the areas of the first 5 polygons:

.. ipython:: python

    # Make a selection that contains only the first five rows
    selection = data[0:5]

-  We can iterate over the selected rows using a specific
   ``.iterrows()`` -function in (geo)pandas:

.. ipython:: python

    for index, row in selection.iterrows():
        # Calculate the area of the polygon
        poly_area = row['geometry'].area
        # Print information for the user
        print("Polygon area at index {0} is: {1:.3f}".format(index, poly_area))

-  Let's create a new column into our GeoDataFrame where we calculate
   and store the areas individual polygons:

.. ipython:: python

    # Empty column for area
    data['area'] = None

-  Let's iterate over the rows and calculate the areas

.. code:: python

    # Iterate rows one at the time
    for index, row in data.iterrows():
        # Update the value in 'area' column with area information at index
        data.loc[index, 'area'] = row['geometry'].area

.. ipython:: python
   :suppress:

    # THIS CODE RUNS IN BACKGROUND AND IS HIDDEN
    for index, row in data.iterrows():
        data.loc[index, 'area'] = row['geometry'].area

-  Let's see the first 2 rows of our 'area' column

.. ipython:: python

    data['area'].head(2)

-  Let's check what is the min and the max of those areas using
   familiar functions from our previous numpy lessions

.. ipython:: python

    # Maximum area
    max_area = data['area'].max()

    # Minimum area
    min_area = data['area'].mean()

    print("Max area: %s\nMean area: %s" % (round(max_area, 2), round(min_area, 2)))


Creating geometries into a GeoDataFrame
---------------------------------------

Since geopandas takes advantage of Shapely geometric objects it is
possible to create a Shapefile from a scratch by passing Shapely's
geometric objects into the GeoDataFrame. This is useful as it makes it
easy to convert e.g. a text file that contains coordinates into a
Shapefile.


-  Let's create an empty ``GeoDataFrame``.

.. code:: python

    # Import necessary modules first
    import pandas as pd
    import geopandas as gpd
    from shapely.geometry import Point, Polygon
    import fiona

    # Create an empty geopandas GeoDataFrame
    newdata = gpd.GeoDataFrame()

.. ipython:: python
   :suppress:

    # Import necessary modules first
    import pandas as pd
    import geopandas as gpd
    from shapely.geometry import Point, Polygon
    import fiona

    # Create an empty geopandas GeoDataFrame
    newdata = gpd.GeoDataFrame()

.. ipython:: python

    # Let's see what's inside
    newdata

The GeoDataFrame is empty since we haven't placed any data inside.

-  Let's create a new column called ``geometry`` that will contain our
   Shapely objects:

.. ipython:: python

    # Create a new column called 'geometry' to the GeoDataFrame
    newdata['geometry'] = None

    # Let's see what's inside
    newdata


Now we have a geometry column in our GeoDataFrame but we don't have any
data yet.

-  Let's create a Shapely Polygon repsenting the Helsinki Senate square
   that we can insert to our GeoDataFrame:

.. ipython:: python

    # Coordinates of the Helsinki Senate square in Decimal Degrees
    coordinates = [(24.950899, 60.169158), (24.953492, 60.169158), (24.953510, 60.170104), (24.950958, 60.169990)]

    # Create a Shapely polygon from the coordinate-tuple list
    poly = Polygon(coordinates)

    # Let's see what we have
    poly

Okey, so now we have appropriate Polygon -object.

-  Let's insert the polygon into our 'geometry' column in our
   GeoDataFrame:

.. ipython:: python

    # Insert the polygon into 'geometry' -column at index 0
    newdata.loc[0, 'geometry'] = poly

    # Let's see what we have now
    newdata

Now we have a GeoDataFrame with Polygon that we can export to a
Shapefile.

-  Let's add another column to our GeoDataFrame called ``Location`` with
   text *Senaatintori*.

.. ipython:: python

    # Add a new column and insert data
    newdata.loc[0, 'Location'] = 'Senaatintori'

    # Let's check the data
    newdata

Okey, now we have additional information that is useful to be able to
recognice what the feature represents.

Before exporting the data it is useful to **determine the spatial
reference system for the GeoDataFrame.**

As was shown earlier, GeoDataFrame has a property called *.crs* that
shows the coordinate system of the data which is empty (None) in our
case since we are creating the data from the scratch:

.. ipython:: python

    print(newdata.crs)

-  Let's add a crs for our GeoDataFrame. A Python module called
   **fiona** has a nice function called ``from_epsg()`` for passing
   coordinate system for the GeoDataFrame. Next we will use that and
   determine the projection to WGS84 (epsg code: 4326):

.. ipython:: python

    # Import specific function 'from_epsg' from fiona module
    from fiona.crs import from_epsg

    # Set the GeoDataFrame's coordinate system to WGS84
    newdata.crs = from_epsg(4326)

    # Let's see how the crs definition looks like
    newdata.crs

-  Finally, we can export the data using GeoDataFrames ``.to_file()``
   -function. The function works similarly as numpy or pandas, but here
   we only need to provide the output path for the Shapefile. Easy isn't
   it!:

.. code:: python

    # Determine the output path for the Shapefile
    outfp = r"/home/geo/Data/Senaatintori.shp"

    # Write the data into that Shapefile
    newdata.to_file(out)

Now we have successfully created a Shapefile from the scratch using only
Python programming. Similar approach can be used to for example to read
coordinates from a text file (e.g. points) and create Shapefiles from
those automatically.

**Task:** check the output Shapefile in QGIS and make sure that the
attribute table seems correct.

Pro -tips (optional but recommended)
------------------------------------

Grouping data
~~~~~~~~~~~~~

One really useful function that can be used in Pandas/Geopandas is `.groupby() <http://pandas.pydata.org/pandas-docs/stable/generated/pandas.DataFrame.groupby.html>`_.
This function groups data based on values on selected column(s).

- Let's group individual fishes in ``DAMSELFISH_distribution.shp`` and export the species to individual Shapefiles.

  - *Note: If your `data` -variable doesn't contain the Damselfish data anymore, read the Shapefile again into memory using `gpd.read_file()` -function*

.. ipython:: python

    # Group the data by column 'binomial'
    grouped = data.groupby('binomial')

    # Let's see what we got
    grouped

- ``groupby`` -function gives us an object called ``DataFrameGroupBy`` which is similar to list of keys and values (in a dictionary) that we can iterate over.

.. ipython:: python

    # Iterate over the group object

    for key, values in grouped:
        individual_fish = values

    # Let's see what is the LAST item that we iterated
    individual_fish

From here we can see that an individual_fish variable now contains all the rows that belongs to a fish called ``Teixeirichthys jordani``. Notice that the index numbers refer to the row numbers in the
original data -GeoDataFrame.

- Let's check the datatype of the grouped object and what does the ``key`` variable contain

.. ipython:: python

    type(individual_fish)

    print(key)

As can be seen from the example above, each set of data are now grouped into separate GeoDataFrames that we can export into Shapefiles using the variable ``key``
for creating the output filepath names. Let's now export those species into individual Shapefiles.

.. code:: python

    # Determine outputpath
    outFolder = r"/home/geo/Data"

    # Create a new folder called 'Results' (if does not exist) to that folder using os.makedirs() function
    resultFolder = os.path.join(outFolder, 'Results')
    if not os.path.exists(resultFolder):
        os.makedirs(resultFolder)

    # Iterate over the
    for key, values in grouped:
        # Format the filename (replace spaces with underscores)
        outName = "%s.shp" % key.replace(" ", "_")

        # Print some information for the user
        print("Processing: %s" % key)

        # Create an output path
        outpath = os.path.join(resultFolder, outName)

        # Export the data
        values.to_file(outpath)

Now we have saved those individual fishes into separate Shapefiles and named the file according to the species name. These kind of grouping operations can be really
handy when dealing with Shapefiles. Doing similar process manually would be really laborious and error-prone.