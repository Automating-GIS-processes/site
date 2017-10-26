Download datasets
=================

For this lesson we are using data that you can download from `here <https://github.com/Automating-GIS-processes/Lesson-2-Geo-DataFrames/raw/master/data/Data.zip>`_.
Once you have downloaded the Data.zip file into your home directory, you can unzip the file using the ``unzip`` command in the Terminal window.

 .. code:: bash

    $ cd $HOME
    $ unzip Data.zip
    $ ls Data
    DAMSELFISH_distributions.dbf   DAMSELFISH_distributions.prj
    DAMSELFISH_distributions.sbn   DAMSELFISH_distributions.sbx
    DAMSELFISH_distributions.shp   DAMSELFISH_distributions.shp.xml
    DAMSELFISH_distributions.shx

The Data folder includes a Shapefile called **DAMSELFISH_distribution.shp** (and files related to it).

Let's start now working with spatial data using geopandas.