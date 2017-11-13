
Spatial join
============

`Spatial join <http://wiki.gis.com/wiki/index.php/Spatial_Join>`__ is
yet another classic GIS problem. Getting attributes from one layer and
transferring them into another layer based on their spatial relationship
is something you most likely need to do on a regular basis.

The previous materials focused on learning how to perform a `Point in Polygon query <Lesson3-point-in-polygon.html#how-to-check-if-point-is-inside-a-polygon>`__.
We could now apply those techniques and create our
own function to perform a spatial join between two layers based on their
spatial relationship. We could for example join the attributes of a
polygon layer into a point layer where each point would get the
attributes of a polygon that ``contains`` the point.

Luckily, `spatial join <http://geopandas.org/mergingdata.html#spatial-joins>`__
(``gpd.sjoin()`` -function) is already implemented in Geopandas, thus we
do not need to create it ourselves. There are three possible types of
join that can be applied in spatial join that are determined with ``op``
-parameter:

-  ``"intersects"``
-  ``"within"``
-  ``"contains"``

Sounds familiar? Yep, all of those spatial relationships were discussed
in the `previous materials <Lesson3-point-in-polygon.html>`__, thus you should know how they work.

Let's perform a spatial join between the address-point Shapefile that we
`created <Lesson3-table-join.html>`__ and then `reprojected <Lesson3-projections.html>`__
and a Polygon layer that is a
250m x 250m grid showing the amount of people living in Helsinki Region.

Download and clean the data
~~~~~~~~~~~~~~~~~~~~~~~~~~~

For this lesson we will be using publicly available population data from
Helsinki that can be downloaded from `Helsinki Region Infroshare
(HRI) <http://www.hri.fi/en/dataset/vaestotietoruudukko>`__ which is an
excellent source that provides all sorts of open data from Helsinki,
Finland.

From HRI **download a** `Population grid for year
2015 <https://www.hsy.fi/sites/AvoinData/AvoinData/SYT/Tietoyhteistyoyksikko/Shape%20(Esri)/V%C3%A4est%C3%B6tietoruudukko/Vaestotietoruudukko_2015.zip>`__
that is a dataset (.shp) produced by Helsinki Region Environmental
Services Authority (HSY) (see `this
page <https://www.hsy.fi/fi/asiantuntijalle/avoindata/Sivut/AvoinData.aspx?dataID=7>`__
to access data from different years).

-  Unzip the file in Terminal into a folder called Pop15 (using -d flag)

.. code:: bash

    $ cd
    $ unzip Vaestotietoruudukko_2015.zip -d Pop15
    $ ls Pop15
    Vaestotietoruudukko_2015.dbf  Vaestotietoruudukko_2015.shp
    Vaestotietoruudukko_2015.prj  Vaestotietoruudukko_2015.shx

You should now have a folder ``/home/geo/Pop15`` with files listed
above.

-  Let's read the data into memory and see what we have.

.. ipython:: python
  :suppress:

    import os
    import gdal
    fp = os.path.join(os.path.abspath('data'), "Vaestotietoruudukko_2015.shp")
    pop = gpd.read_file(fp)

.. code:: python

    import geopandas as gpd

    # Filepath
    fp = "/home/geo/Pop15/Vaestotietoruudukko_2015.shp"

    # Read the data
    pop = gpd.read_file(fp)

.. ipython:: python

    # See the first rows
    pop.head()

Okey so we have multiple columns in the dataset but the most important
one here is the column ``ASUKKAITA`` (*population in Finnish*) that
tells the amount of inhabitants living under that polygon.

-  Let's change the name of that columns into ``pop15`` so that it is
   more intuitive. Changing column names is easy in Pandas / Geopandas
   using a function called ``rename()`` where we pass a dictionary to a
   parameter ``columns={'oldname': 'newname'}``.

.. ipython:: python

    # Change the name of a column
    pop = pop.rename(columns={'ASUKKAITA': 'pop15'})
    
    # See the column names and confirm that we now have a column called 'pop15'
    pop.columns

-  Let's also get rid of all unnecessary columns by selecting only
   columns that we need i.e. ``pop15`` and ``geometry``

.. ipython:: python

    # Columns that will be sected
    selected_cols = ['pop15', 'geometry']
    
    # Select those columns
    pop = pop[selected_cols]

    # Let's see the last 2 rows
    pop.tail(2)

Now we have cleaned the data and have only those columns that we need
for our analysis.

Join the layers
~~~~~~~~~~~~~~~

Now we are ready to perform the spatial join between the two layers that
we have. The aim here is to get information about **how many people live
in a polygon that contains an individual address-point** . Thus, we want
to join attributes from the population layer we just modified into the
addresses point layer ``addresses_epsg3879.shp``.

-  Read the addresses layer into memory

.. ipython:: python

    # Addresses filpath
    addr_fp = r"/home/geo/addresses_epsg3879.shp"

    @suppress
    import os

    @suppress
    "NOTICE: Following is the real path to the data, the one above is for online documentation to reflect the situation at computing instance"

    @suppress
    addr_fp = os.path.join(os.path.abspath('data'), "addresses_epsg3879.shp")
    
    # Read data
    addresses = gpd.read_file(addr_fp)
    
    # Check the head of the file
    addresses.head(2)

-  Let's make sure that the coordinate reference system of the layers
   are identical

.. ipython:: python

    # Check the crs of address points
    addresses.crs
    
    # Check the crs of population layer
    pop.crs
    
    # Do they match? - We can test that
    addresses.crs == pop.crs

Indeed they are identical. Thus, we can be sure that when doing spatial
queries between layers the locations match and we get the right results
e.g. from the spatial join that we are conducting here.

-  Let's now join the attributes from ``pop`` GeoDataFrame into
   ``addresses`` GeoDataFrame by using ``gpd.sjoin()`` -function

.. ipython:: python

    # Make a spatial join
    join = gpd.sjoin(addresses, pop, how="inner", op="within")
    
    # Let's check the result
    join.head()

Awesome! Now we have performed a successful spatial join where we got
two new columns into our ``join`` GeoDataFrame, i.e. ``index_right``
that tells the index of the matching polygon in the ``pop`` layer and
``pop15`` which is the population in the cell where the address-point is
located.

-  Let's save this layer into a new Shapefile

.. code:: python

    # Output path
    outfp = r"/home/geo/addresses_pop15_epsg3979.shp"
    
    # Save to disk
    join.to_file(outfp)

Do the results make sense? Let's evaluate this a bit by plotting the
points where color intensity indicates the population numbers.

-  Plot the points and use the ``pop15`` column to indicate the color.
   ``cmap`` -parameter tells to use a sequential colormap for the
   values, ``markersize`` adjusts the size of a point, ``scheme`` parameter can be used to adjust the classification method based on `pysal <http://pysal.readthedocs.io/en/latest/library/esda/mapclassify.html>`_, and ``legend`` tells that we want to have a legend.

.. ipython:: python

    import matplotlib.pyplot as plt

    # Plot the points with population info
    join.plot(column='pop15', cmap="Reds", markersize=7, scheme='natural_breaks', legend=True);

    # Add title
    plt.title("Amount of inhabitants living close the the point");

    # Remove white space around the figure
    @savefig population_points.png width=7in
    plt.tight_layout()

By knowing approximately how population is distributed in Helsinki, it
seems that the results do make sense as the points with highest
population are located in the south where the city center of Helsinki
is.
