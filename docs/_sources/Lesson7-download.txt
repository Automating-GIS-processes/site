Download data
=============

Download data for this lesson from this `link <http://www.helsinki.fi/science/accessibility/opetus/autogis/LC81910182016153-SC20161208043748.tar.gz>`_.

n this lesson, we will use a Landsat 8 satellite scene for practicing how to read raster data with Python and Gdal.
Landsat images are distributed as gzipped TAR archives *.tar.gz when downloading from the `USGS Earth Explorer <https://earthexplorer.usgs.gov/>`_.
For the purposes of this exercise, we have pre-downloaded a scene covering South-West Finland which you can download from the above link.
In order to get started, you need to extract the contents of the TAR archive either in the Terminal window or with a Python script.

Option 1: Extract files in terminal
-----------------------------------

Navigate to the directory where you downloaded the data, and extract files into a new folder:

.. code:: bash

    mkdir LandsatData
    tar -zxvf LC81910182016153-SC20161208043748.tar.gz -C LandsatData/

Option 2: Extract files using Python
------------------------------------

It is also possible to extract the files in python using the ``tarfile`` module. First, open the file with ``tarfile.open()```.
The parameter ``r:gz`` specifies that we want to open the gzipped file in reading mode. Then, extract the files using ``tarifile.extractall()`` method:

.. code:: python

    import os
    import tarfile

    #Create output folder
    newFolder = "LandsatData"
    os.makedirs(newFolder)

    #Extract files
    tar = tarfile.open("LC81910182016153-SC20161208043748.tar.gz", "r:gz")
    tar.extractall(newFolder)
    tar.close()

