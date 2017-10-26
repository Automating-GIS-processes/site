GDAL command line tools
=======================

We have now tested some of the basic functions from the Python `GDAL/OGR API <https://pcjericks.github.io/py-gdalogr-cookbook/index.html>`_ for reading and inspecting
raster files. However, GDAL also includes
other powerful functions for data translation and processing which are not directly implemented in the library. We will have a closer look on a couple of such
functions:

    - `gdalwarp <http://www.gdal.org/gdalwarp.html>`_ for clipping, mosaicing, reprojection and other processes

    - `gdal_merge.py <http://www.gdal.org/gdal_merge.html>`_ for mosaicing / stacking images

    - `gdal_calc.py <http://www.gdal.org/gdal_calc.html>`_ for raster calculations

These tools **need to be run from the Terminal/Command Prompt** or as a **subprocess in Python**. We will now quickly test out these tools in the Terminal window.

Clipping image with gdalwarp
----------------------------

Among other tricks, gdalwarp is a very handy tool for quickly clipping your image. We will now practice how to clip the satellite image band based on a bounding box.
Desired extent for the output file is specified using the option ``-te``:

.. code:: bash

    gdalwarp -te xmin ymin xmax ymax inputfile.tif outputfile.tif

.. todo::

    **Task**

    Clip band 4 of the satellite image so that it covers cloud-free areas in the Turku archipelago (in the North-East corner of the scene).

    You can open the band 4 manually in QGIS for defining the corner coordinates.

Next, let's repeat the clipping for all the rest of the bands all at once. For doing this, we will use Python for generating the command for each spectral band in
our scene.

.. code:: python

    import glob
    import os

    # List filepaths for all bands in the scence
    FileList = glob.glob(os.path.join(r'/home/geo/LandsatData','*band*.tif'))

    # Define clipping extent
    xmin, ymin, xmax,ymax = (0, 0, 0, 0) # INSERT HERE THE CORRECT COORDINATES

    # Generate gdalwarp command for each band
    command = ""

    for fp in FileList:
        inputfile = fp
        outputfile = inputfile[:-4] + "_clip.tif"

        command += "gdalwarp -te %s %s %s %s %s %s \n" % (xmin, ymin, xmax, ymax, inputfile, outputfile)

    # Write the commands to an .sh file
    cmd_file = "ClipTurkufromLandsat.sh"
    f = open(os.path.join(cmd_file), 'w')

    f.write(command)
    f.close()

.. note::

     If you are working in an windows environment, change the ``.sh`` extension to ``.bat`` which is the Windows equivalent of a **batch** -file with similar
     functionalities.

After running the above script, you should have a file ``ClipTurkufromLandsat.sh`` in your working directory. Open the file (with a text editor) and
check that the commands have been written correctly to the file.

Next, run the file in the Terminal window:

.. code:: bash

    bash ClipTurkufromLandsat.sh

Now you should have a bunch of clipped ``.tif`` files ready and you might want to open a few of them in QGIS to check that the process was successful.

Stacking layers with gdal_merge.py
----------------------------------

After clipping the image you can for example stack bands 3 (green), 4 (red), and 5 (nir) for visualizing a false-color composite. Merge the layers
with ``gdal_merge.py`` and use the ``-separate`` option for indicating that you wish to save the inputs as separate bands in the output file.

Let's try running the command as a subprocess in python:

.. code:: python

    import os

    # Define input and output files
    inputfiles =  "band3_clip.tif band4_clip.tif band5_clip.tif"
    outputfile =  "Landsat8_GreenRedNir.tif"

    # Generate the command
    command = "gdal_merge.py -separate %s -o %s" % (inputfiles, outputfile)

    # Run the command. os.system() returns value zero if the command was executed succesfully
    os.system(command)

As a result, you have three bands stacked together in the file ``Landsat8_GreenRedNir.tif``.

Calculations with rasters using gdal_calc.py
--------------------------------------------

``Gdal_calc.py`` is a command line raster calculator which can be useful for competing simple repetitive calculations for raster data.

Open the terminal window and execute following command:

.. code:: bash

    Gdal_calc.py

You should see instructions on the usage and options for the tool. The basic syntax for ``gdal_calc.py`` is the following:

.. code::

    gdal_calc.py -A input1.tif - B input2.tif [other_options] --outfile=outputfile.tif

From other options, it is useful to notice at least the parameters ``--calc`` for specifying the calculation syntax and ``--creation-option`` (or ``--co``)
for controlling the output file size:

   - In the case of two input files ``--calc="A+B"`` would add files A and B together.
   - By default output files tend to be huge which will quickly result in problems with disk size and memory. With ``gdal_calc.py`` you can add parameter
     ``--co="COMPRESS=LZW"`` in order to reduce output file size.

