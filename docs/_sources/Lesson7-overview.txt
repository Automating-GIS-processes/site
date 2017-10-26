Lesson 7 Overview
=================

In this lesson we will learn basic techniques for automating raster data processing with Python and the Geospatial Data Abstraction Library `GDAL <http://www.gdal.org/>`_.

Raster files are commonly used to store terrain models and remote sensing data and their derivate products such as vegetation indices and other environmental datasets.
Raster files tend to be huge (imagine for example a raster dataset covering the globe in 30m x 30m resolution) and are often delivered and processed in smaller pieces
(tiles). Efficient processing and analysis of such large datasets consequently requires automatization. During this lesson you will learn how to read and write common
raster formats, and conduct basic raster data processes for a batch of files using the GDAL/OGR API in Python and GDAL command line utilities.

If you want to dive deeper into raster data processing in Python you might want to check out `Rasterio <https://mapbox.github.io/rasterio/>`_ which is a relatively new Python library for efficient raster
data analysis using more "Pythonic" syntax. Also remember that you can write Python scripts for using ArcGIS tools as introduced `last week <Lesson6-arcpy-script.html>`_.

For more information and examples with GDAL, please see these online resources:

  - `http://www.gdal.org/gdal_tutorial.html <http://www.gdal.org/gdal_tutorial.html>`_
  - `https://pypi.python.org/pypi/GDAL/ <http://www.gdal.org/gdal_tutorial.html>`_
  - `https://pcjericks.github.io/py-gdalogr-cookbook/raster_layers.html <http://www.gdal.org/gdal_tutorial.html>`_

Learning objectives
-------------------

After this week's lesson you should be able to:

 - Read / write raster data (e.g. ``.tif``) in Python
 - Extract some basic raster statistics from the data (min, max, mean, no-data-value etc.)
 - Clip the raster dataset by bounding box
 - Stack different bands together and create a false-color composite
 - Calculate with rasters

.. todo::

    Raster processing examples could take advantage of `Rasterio <https://mapbox.github.io/rasterio/>`_ which has a more Pythonic syntax for doing raster processing.