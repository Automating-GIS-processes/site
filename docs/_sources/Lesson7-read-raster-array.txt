Reading raster as a numerical array
===================================

GDAL is a powerful library when it comes to accessing geospatial raster data, but it does not provide many functionalities for doing calculations.
For more advanced computing, we will read in the raster data as a numerical array in order to use the capabilities in the NumPy-library.

In case you want to convert and existing Gdal Dataset or a Band into a numpy array you can convert it with ``ReadAsArray()`` -function:

.. code:: python

    # Read raster data as numeric array from GDAL Dataset
    rasterArray = raster.ReadAsArray()

So what is the difference?

.. code:: python

    #Check the datatype of variables
    type(rasterArray)

.. code:: python

    type(raster)


As you can see, we have now stored the same raster data into two different types of variables:

 - **raster** is a ``Gdal Dataset``

 - **rasterArray** is a ``numpy array``

The GDAL library also comes with a module gdal_array that works as an interface between NumPy and GDAL.
Gdal_array reads and writes raster files to and from NumPy arrays directly from file:

.. code:: python

    from osgeo import gdal_array

    # Read raster data as numeric array from file
    rasterArray = gdal_array.LoadFile(filepath)

Excluding NoData values
-----------------------

What is the minimum value of our array?

.. code:: python

    rasterArray.min()

As you can see, the numpy array still contains the original nodata values. Any calculations will be wrong if these are not taken care of.

.. code:: python

    import numpy as np

    # Get nodata value from the GDAL band object
    nodata = band.GetNoDataValue()

    #Create a masked array for making calculations without nodata values
    rasterArray = np.ma.masked_equal(rasterArray, nodata)
    type(rasterArray)

    # Check again array statistics
    rasterArray.min()

Now you have a two-dimensional array ready for further calculations.
However, for completing our exercise for this week we will use a very simple command line tool ``gdal_calc.py``.

Closing raster dataset
----------------------

It might be useful to close an existing GDAL object in the middle of the code if you want to free resources and remove unnecessary variables from memory.

.. code:: python

    raster = None
    band = None

It is however not necessary to close raster datasets or bands at the end of the python script as Python will automatically take care of this.

