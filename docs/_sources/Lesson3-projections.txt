
Re-projecting data
==================

A map projection is a systematic transformation of the latitudes and
longitudes into a plain surface. As map projections of gis-layers are
fairly often defined differently (i.e. they do not match), it is a
common procedure to redefine the map projections to be identical in both
layers. It is important that the layers have the same projection as it
makes it possible to analyze the spatial relationships between layer,
such as conduct the Point in Polygon spatial query (which we will try
next).

Defining a projection and changing it is easy in Geopandas. Let's
continue working with our `address points <Lesson3-geocoding.html>`__, and change the
Coordinate Reference System (CRS) from WGS84 into a projection called
`ETRS GK-25 <http://www.maanmittauslaitos.fi/ammattilaisille/maastotiedot/koordinaatti-korkeusjarjestelmat/karttaprojektiot-tasokoordinaatistot/tasokoordinaatistot/etrs-gkn>`__
(EPSG:3879) which uses a Gauss-Krüger projection that is (sometimes)
used in Finland.

-  Let's first read the data from the Shapefile that we `created previously <Lesson3-table-join.html>`__

.. ipython:: python

    @suppress
    import gdal

    import geopandas as gpd
    
    # Filepath to the addresses Shapefile
    fp = "/home/geo/addresses.shp"

    @suppress
    import os

    @suppress
    fp = os.path.join(os.path.abspath('data'), "addresses.shp")

    # Read data
    data = gpd.read_file(fp)

-  Let's check what is the current CRS of our layer

.. ipython:: python

    data.crs

Okey, so it is WGS84 (i.e. EPSG: 4326).

-  Let's also check the values in our ``geometry`` column

.. ipython:: python

    data['geometry'].head()

Okey, so they indeed look like lat-lon values.

-  Let's convert those geometries into ETRS GK-25 projection (EPSG:
   3879). Changing the projection is really easy to `do in
   Geopandas <http://geopandas.org/projections.html#re-projecting>`__
   with ``.to_crs()`` -function. As an input for the function, you
   should define the column containing the geometries, i.e. ``geometry``
   in this case, and a ``epgs`` value of the projection that you want to
   use.

-  Note: there is also possibility to pass the projection information as
   proj4 strings or dictionaries, see more
   `here <http://geopandas.org/projections.html#coordinate-reference-systems>`__

.. ipython:: python

    # Let's take a copy of our layer
    data_proj = data.copy()
    
    # Reproject the geometries by replacing the values with projected ones
    data_proj['geometry'] = data_proj['geometry'].to_crs(epsg=3879)

-  Let's see how they look now

.. ipython:: python

    data_proj['geometry'].head()

And here we go, the numbers have changed! Now we have successfully
changed the projection of our layer into a new one.

-  Let's still compare the layers visually

.. code:: python

    import matplotlib.pyplot as plt

    # Plot the WGS84
    data.plot(markersize=6, color="red");

    # Add title
    plt.title("WGS84 projection");

    # Remove empty white space around the plot
    plt.tight_layout()
    
    # Plot the one with ETRS GK-25 projection
    data_proj.plot(markersize=6, color="blue");

    # Add title
    plt.title("ETRS GK-25 projection");

    # Remove empty white space around the plot
    plt.tight_layout()

.. ipython:: python
   :suppress:

       import matplotlib.pyplot as plt;
       data.plot(markersize=6, color="red");
       plt.title("WGS84 projection");
       @savefig wgs84.png width=3.5in
       plt.tight_layout();

       data_proj.plot(markersize=6, color="blue");
       plt.title("ETRS GK-25 projection");
       @savefig projected.png width=3.5in
       plt.tight_layout();

Indeed, they look different and our re-projected one looks much better
in Finland (not so stretced as in WGS84).

-  Now we still need to change the crs of our GeoDataFrame into EPSG
   3879 as now we only modified the values of the ``geometry`` column.
   We can take use of fiona's ``from_epsg`` -function.

.. ipython:: python

    from fiona.crs import from_epsg
    
    # Determine the CRS of the GeoDataFrame
    data_proj.crs = from_epsg(3879)
    
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
    data_proj.crs = {'y_0': 0, 'no_defs': True, 'x_0': 25500000, 'k': 1, 'lat_0': 0, 'units': 'm', 'lon_0': 25, 'ellps': 'GRS80', 'proj': 'tmerc'}
    
    # Check that it changed
    data_proj.crs

-  Finally, let's save our projected layer into a Shapefile so that we
   can use it later.

.. code:: python

    # Ouput file path
    outfp = r"/home/geo/addresses_epsg3879.shp"
    
    # Save to disk
    data_proj.to_file(outfp)
