Map projections
===============

A map projection (or coordinate reference system, CRS) is a systematic transformation of the latitudes and
longitudes into a plain surface. As map projections of gis-layers are
fairly often defined differently (i.e. they do not match), it is a
common procedure to redefine the map projections to be identical in both
layers. It is important that the layers have the same projection as it
makes it possible to analyze the spatial relationships between layer,
such as conduct the Point in Polygon spatial query (which we will try
next).

Luckily, defining and changing projections is easy in Geopandas. In this tutorial we will see how to retrieve the
coordinate reference system information from the data, and how to change it. We will re-project a data file from
WGS84 (lat, lon coordinates) into a Lambert Azimuthal Equal Area projection which is the `recommended projection for
Europe <http://mapref.org/LinkedDocuments/MapProjectionsForEurope-EUR-20120.pdf>`__ by European Commission.

.. note::

   Choosing an appropriate projection for your map is not always straightforward because it depends on what you actually want
   to represent with your map, and what is the spatial scale of your data. In fact, there does not exist a "perfect projection"
   since each one of them has some strengths and weaknesses, and you should choose such projection that fits best for your needs.
   You can read more about `how to choose a map projection from here <http://www.georeference.org/doc/guide_to_selecting_map_projections.htm>`__,
   and a nice `blog post about the strengths and weaknesses of few commonly used projections <http://usersguidetotheuniverse.com/index.php/2011/03/03/whats-the-best-map-projection/>`__.

Download data
-------------

For this tutorial we will be using a Shapefile representing Europe. Download and extract Europe_borders.zip file
that contains a Shapefile with following files:

.. code:: bash

   $ cd $HOME
   $ unzip Europe_borders.zip
   $ cd Europe_borders
   $ ls
   Europe_borders.cpg  Europe_borders.prj  Europe_borders.sbx  Europe_borders.shx
   Europe_borders.dbf  Europe_borders.sbn  Europe_borders.shp

Checking the coordinate reference system of data
------------------------------------------------

Coordinate reference systems (CRS) are important because the geometric shapes in a GeoDataFrame are simply a collection of coordinates
in an arbitrary space. A CRS tells Python how those coordinates related to places on the Earth.

Let's start by reading the data from the ``Europe_borders.shp`` file.

.. ipython:: python

    import geopandas as gpd
    
    # Filepath to the Europe borders Shapefile
    fp = "/home/geo/Europe_borders.shp"

    @suppress
    import os

    @suppress
    fp = os.path.join(os.path.abspath('data'), "Europe_borders.shp")

    # Read data
    data = gpd.read_file(fp)

Let's check what is the current CRS of our layer.

.. ipython:: python

    data.crs

Okey, so it is WGS84 (i.e. EPSG: 4326).

Let's also check the values in our ``geometry`` column

.. ipython:: python

    data['geometry'].head()

Okey, so the coordinate values indeed look like lat-lon values.

Let's convert those geometries into Lambert Azimuthal Equal Area projection (`EPSG: 3035 <http://spatialreference.org/ref/epsg/etrs89-etrs-laea/>`__).
Changing the projection is really easy to `do in Geopandas <http://geopandas.org/projections.html#re-projecting>`__
with ``.to_crs()`` -function. As an input for the function, you
should define the column containing the geometries, i.e. ``geometry``
in this case, and a ``epgs`` value of the projection that you want to use.

.. ipython:: python

    # Let's take a copy of our layer
    data_proj = data.copy()
    
    # Reproject the geometries by replacing the values with projected ones
    data_proj['geometry'] = data_proj['geometry'].to_crs(epsg=3035)

Let's see how they look now.

.. ipython:: python

    data_proj['geometry'].head()

And here we go, the numbers have changed! Now we have successfully
changed the projection of our layer into a new one.

.. note::

   There is also possibility to pass the projection information as proj4 strings or dictionaries, see more `here <http://geopandas.org/projections.html#coordinate-reference-systems>`__

Let's still compare the layers visually

.. code:: python

    import matplotlib.pyplot as plt

    # Plot the WGS84
    data.plot(facecolor='gray');

    # Add title
    plt.title("WGS84 projection");

    # Remove empty white space around the plot
    plt.tight_layout()
    
    # Plot the one with ETRS-LAEA projection
    data_proj.plot(facecolor='blue');

    # Add title
    plt.title("ETRS Lambert Azimuthal Equal Area projection");

    # Remove empty white space around the plot
    plt.tight_layout()

.. ipython:: python
   :suppress:

       import matplotlib.pyplot as plt;
       data.plot(facecolor='gray');
       plt.title("WGS84 projection");
       @savefig wgs84.png width=3.5in
       plt.tight_layout();

       data_proj.plot(facecolor="blue");
       plt.title("ETRS Lambert Azimuthal Equal Area projection");
       @savefig projected.png width=3.5in
       plt.tight_layout();

Indeed, they look quite different and our re-projected one looks much better
in Europe as the areas in the north especially are more realistic and not so stretced as in WGS84.

Now we still need to change the crs of our GeoDataFrame into EPSG
3035 as now we only modified the values of the ``geometry`` column.
We can take use of fiona's ``from_epsg`` -function.

.. ipython:: python

    from fiona.crs import from_epsg
    
    # Determine the CRS of the GeoDataFrame
    data_proj.crs = from_epsg(3035)
    
    # Let's see what we have
    data_proj.crs

.. note::

   The above works for most EPSG codes but as ETRS GK-25
   projection is a rather rare one, we still need to make sure
   that .prj file is having correct coordinate system information. We do that by
   passing a proj4 dictionary (below) into it (otherwise the ``.prj`` file of the Shapefile
   might be empty):

.. ipython:: python

    # Pass the coordinate information
    #data_proj.crs = {'y_0': 0, 'no_defs': True, 'x_0': 25500000, 'k': 1, 'lat_0': 0, 'units': 'm', 'lon_0': 25, 'ellps': 'GRS80', 'proj': 'tmerc'}

    # Check that it changed
    #data_proj.crs

Finally, let's save our projected layer into a Shapefile so that we
can use it later.

.. code:: python

    # Ouput file path
    outfp = r"/home/geo/Europe_borders_epsg3035.shp"
    
    # Save to disk
    data_proj.to_file(outfp)

