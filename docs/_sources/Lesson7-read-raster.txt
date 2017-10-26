Reading raster files with GDAL
==============================

With GDAL, you can read and write `several different raster formats <http://www.gdal.org/formats_list.html>`_ in Python. Python automatically registers all known GDAL drivers for reading supported
formats when the importing the GDAL module. Most common file formats include for example `TIFF and GeoTIFF <http://www.gdal.org/frmt_gtiff.html>`_,
`ASCII Grid <http://www.gdal.org/frmt_various.html#AAIGrid>`_ and `Erdas Imagine .img <http://www.gdal.org/frmt_hfa.html>`_ -files.

`Landsat 8 <http://landsat.gsfc.nasa.gov/landsat-8/landsat-8-bands/>`_ bands are stored as separate GeoTIFF -files in the original package.
Each band contains information of surface reflectance from different ranges
of the electromagnetic spectrum.

Let's start with inspecting one of the files we downloaded:

.. code:: python

    from osgeo import gdal

    filepath = r"LandsatData/LC81910182016153LGN00_sr_band4.tif"

    # Open the file:
    raster = gdal.Open(filepath)

    # Check type of the variable 'raster'
    type(raster)

Read raster file properties
---------------------------

The satellite image is now stored as a GDAL Dataset object in the variable ``raster``. Let's have a closer look at the properties of the file:

.. code:: python

    # Projection
    raster.GetProjection()

    # Dimensions
    raster.RasterXSize
    raster.RasterYSize

    # Number of bands
    raster.RasterCount

    # Metadata for the raster dataset
    raster.GetMetadata()

Get raster bands
----------------

In our case, all bands of the Landsat 8 scene are stored as separate files. ``rasterCount`` is 1 as we have only opened one GeoTiff containing Landsat 8 band 4.
However, different bands of a satellite images are often stacked together in one raster dataset in which case ``rasterCount`` would be greater than one.

In order to have a closer look at the values stored in the band, we will take advantage of the `GDAL Band API <http://gdal.org/python/osgeo.gdal.Band-class.html>`_.

.. code:: python

    # Read the raster band as separate variable
    band = raster.GetRasterBand(1)

    # Check type of the variable 'band'
    type(band)

    # Data type of the values
    gdal.GetDataTypeName(band.DataType)

Now we have a GDAL Raster Band object stored in the variable band.

Data type of the band can be interpreted with the help of GDAL documentation on `Pixel data types <http://www.gdal.org/gdal_8h.html#a22e22ce0a55036a96f652765793fb7a4>`_.
Unsigned integer is always equal or greater than zero and signed integer can store also negative values. For example, an unsigned 16-bit integer can
store 2^16 (=65,536) values ranging from 0 to 65,535.

Band statistics
---------------

Next, let's have a look at the values that are stored in the band. You might need to calculate statistics for the raster before being able to print out any information.

.. code:: python

    # Compute statistics if needed
    if band.GetMinimum() is None or band.GetMaximum()is None:
        band.ComputeStatistics(0)
        print("Statistics computed.")

    # Fetch metadata for the band
    band.GetMetadata()

    # Print only selected metadata:
    print ("[ NO DATA VALUE ] = ", band.GetNoDataValue()) # none
    print ("[ MIN ] = ", band.GetMinimum())
    print ("[ MAX ] = ", band.GetMaximum())

