Installing Python + GIS
=======================

**How to start doing GIS with Python on your own computer?**

Well, first you need to install Python and necessary Python modules that are used to perform various GIS-tasks. The purpose of this page is to help you
out installing Python and all those modules into your own computer. Even though it is possible to install Python from their `homepage <https://www.python.org/>`_,
**we highly recommend using** `Anaconda <https://www.continuum.io/anaconda-overview>`_ which is an open source distribution of the Python and R programming
languages for large-scale data processing, predictive analytics, and scientific computing, that aims to simplify package management and deployment. In short,
it makes life much easier when installing new tools on your Python to play with.

Install Python + GIS on Windows
-------------------------------

Following steps have been tested to work on Windows 7 and 10 with Anaconda3 version 4.2.0 (19th November 2016).

`Download Anaconda installer (64 bit) <https://www.continuum.io/downloads>`_ for Windows.

Install Anaconda to your computer by double clicking the installer and install it into a directory you want (needs admin rights).
Install it to **all users** and use default settings.

.. note::

    Note for University of Helsinki workers: you need to set the installation location as ``C:\HYapp`` so that it can be used easily by anyone without the need to
    pass admin credentials all the time. If you don't have ``C:\HYapp`` -folder, create one with admin rights.


Test that the Anaconda´s package manage called ``conda`` works by `opening a command prompt as a admin user <http://www.howtogeek.com/194041/how-to-open-the-command-prompt-as-administrator-in-windows-8.1/>`_
and running command ``conda --version``.


Install GIS related packages with conda by running in command prompt following commands (in the same order as they are listed):

.. code::

    conda install -y psycopg2 matplotlib bokeh holoviews
    conda install -y -c conda-forge basemap=1.0.8.dev0 --no-deps
    conda install -y -c ioos geopandas=0.2.1
    conda install -y -c conda-forge rasterio=1.0a3
    conda install -y -c ioos iris=1.10.0
    conda install -y -c ioam geoviews=1.1.0
    conda install -y -c anaconda flake8=2.5.1
    conda install -y -c conda-forge seawater
    conda install -y -c conda-forge gpxpy=1.1.1
    conda install -y -c ioos gdal=2.1.2

    # Following one will be installed using pip as we want to install the
    # development version of the folium module with more features

    pip install https://github.com/python-visualization/folium/archive/master.zip


Let's also upgrade few packages:

.. code::

    conda upgrade spyder pandas scipy

Install Python + GIS on Linux / Mac
-----------------------------------

The following have been tested on Ubuntu 16.04. Might work also on Mac (not tested yet).

**Install Anaconda 3 and add it to system path**

.. code::

    # Download and install Anaconda
    sudo wget https://repo.continuum.io/archive/Anaconda3-4.1.1-Linux-x86_64.sh
    sudo bash Anaconda3-4.1.1-Linux-x86_64.sh

    # Add Anaconda installation permanently to PATH variable
    nano ~/.bashrc

    # Add following line at the end of the file and save (EDIT ACCORDING YOUR INSTALLATION PATH)
    export PATH=$PATH:/PATH_TO_ANACONDA/anaconda3/bin:/PATH_TO_ANACONDA/anaconda3/lib/python3.5/site-packages

**Install Python packages**

.. code::

    conda install numpy pandas scipy gdal fiona shapely pyproj psycopg2 matplotlib bokeh holoviews sphinx
    conda install -y -c conda-forge geopandas
    conda install -y -c conda-forge basemap=1.0.8.dev0 --no-deps
    conda install -y -c activisiongamescience tweepy=3.5.0
    conda install -y -c anaconda rasterio=0.36.0
    conda install -y -c scitools/label/dev -c conda-forge iris cartopy
    conda install -y xarray
    conda install -y -c ioam geoviews=1.1.0
    conda install -y -c ioos mplleaflet=0.0.5
    conda install -y -c anaconda flake8=2.5.1
    conda install -y -c conda-forge seawater
    conda install -y -c conda-forge gpxpy=1.1.1
    conda install -y -c conda-forge branca=0.1.2
    pip install https://github.com/python-visualization/folium/archive/master.zip


How to find out which conda -command to use when installing a package?
----------------------------------------------------------------------

The easiest way
~~~~~~~~~~~~~~~

The first thing to try when installing a new module ``X`` is to run in a command prompt (as admin) following command (here we try to install a hypothetical
module called X)

.. code::

    conda install X

In most cases this approach works but sometimes you get errors like (example when installing a module called shapely):

.. code::

    C:\WINDOWS\system32>conda install shapely
    Using Anaconda API: https://api.anaconda.org
    Fetching package metadata .........
    Solving package specifications: .
    Error: Package missing in current win-64 channels:
      - shapely

    You can search for packages on anaconda.org with

        anaconda search -t conda shapely

Okey, so conda couldn't find the shapely module from the typical channel it uses for downloading the module.


Alternative way to install if typical doesn't work
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

How to find a way to install a module if it cannot be installed on a typical way?
Well, the answer is the same is in many other cases nowadays, **Google it!**

Let's find our way to install the Shapely module by typing following query to Google:

.. image:: img/google_query_conda.PNG

Okey, we have different pages showing how to install Shapely using conda package manager.

**Which one of them is the correct one to use?**

We need to check the operating system banners and if you find a logo of the operating system of your computer,
that is the one to use! Thus, in our case the first page that Google gives does not work in Windows but the second one does, as it has Windows logo on it:

.. image:: img/conda_shapely_windows.PNG

From here we can get the correct installation command for conda and it works!

.. image:: img/install_shapely.PNG

You can follow these steps similarly for all of the other Python modules that you are interested to install.


