Geocoding
=========

Overview of Geocoders
---------------------

Geocoding, i.e. converting addresses into coordinates or vice versa, is
a really common GIS task. Luckily, in Python there are nice libraries
that makes the geocoding really easy. One of the libraries that can do
the geocoding for us is
`geopy <http://geopy.readthedocs.io/en/1.11.0/>`__ that makes it easy to
locate the coordinates of addresses, cities, countries, and landmarks
across the globe using third-party geocoders and other data sources.

As said, **Geopy** uses third-party geocoders - i.e. services that does
the geocoding - to locate the addresses and it works with multiple
different service providers such as:

-  `ESRI
   ArcGIS <http://resources.arcgis.com/en/help/arcgis-rest-api/>`__
-  `Baidu
   Maps <http://developer.baidu.com/map/webservice-geocoding.htm>`__
-  `Bing <http://www.microsoft.com/maps/developers/web.aspx>`__
-  `geocoder.us <http://geocoder.us/>`__
-  `GeocodeFarm <https://www.geocodefarm.com/>`__
-  `GeoNames <http://www.geonames.org/>`__
-  `Google Geocoding API
   (V3) <https://developers.google.com/maps/documentation/geocoding/>`__
-  `IGN
   France <http://api.ign.fr/tech-docs-js/fr/developpeur/search.html>`__
-  `Mapquest <http://www.mapquestapi.com/geocoding/>`__
-  `Mapzen Search <https://mapzen.com/projects/search/>`__
-  `NaviData <http://navidata.pl>`__
-  `OpenCage <http://geocoder.opencagedata.com/api.html>`__
-  `OpenMapQuest <http://developer.mapquest.com/web/products/open/geocoding-service>`__
-  `Open Street Map Nominatim <https://wiki.openstreetmap.org/wiki/Nominatim>`__
-  `SmartyStreets <https://smartystreets.com/products/liveaddress-api>`__
-  `What3words <http://what3words.com/api/reference>`__
-  `Yandex <http://api.yandex.com/maps/doc/intro/concepts/intro.xml>`__

Thus, there are plenty of geocoders where to choose from! However, for most of these services you might need to
request so called API access-keys from the service provider to be able to use the service.

Luckily, Nominatim, which is a geocoder based on OpenStreetMap data does not require a API key to use their service
if it is used for small scale geocoding jobs as the service is rate-limited to 1 request per second (3600 / hour).
As we are only making a small set of queries, we can do the geocoding by using Nominatim.

.. note::

   - **Note 1:** If you need to do larger scale geocoding jobs, use and request an API key to some of the geocoders listed above.

   - **Note 2:** There are also other Python modules in addition to geopy that can do geocoding such as `Geocoder <http://geocoder.readthedocs.io/>`__.

.. hint::

    You can get your access keys to e.g. Google Geocoding API from `Google APIs console <https://code.google.com/apis/console>`__ by creating a Project
    and enabling a that API from `Library <https://console.developers.google.com/apis/library>`__. Read a
    short introduction about using Google API Console from `here <https://developers.googleblog.com/2016/03/introducing-google-api-console.html>`__.

Geocoding in Geopandas
----------------------

It is possible to do geocoding in Geopandas using its integrated
functionalities of geopy. Geopandas has a function called ``geocode()``
that can geocode a list of addresses (strings) and return a GeoDataFrame
containing the resulting point objects in ``geometry`` column. Nice,
isn't it! Let's try this out.

Download a text file called `addresses.txt <../../_static/data/L3/addresses.txt>`__ that
contains few addresses around Helsinki Region. The first rows of the
data looks like following:

.. parsed-literal::

    id;addr
    1000;Itämerenkatu 14, 00101 Helsinki, Finland
    1001;Kampinkuja 1, 00100 Helsinki, Finland
    1002;Kaivokatu 8, 00101 Helsinki, Finland
    1003;Hermannin rantatie 1, 00580 Helsinki, Finland

We have an ``id`` for each row and an address on column ``addr``.

-  Let's first read the data into a Pandas DataFrame using
   ``read_csv()`` -function:

.. code:: python

    # Import necessary modules
    import pandas as pd
    import geopandas as gpd
    from shapely.geometry import Point
    
    # Filepath
    fp = r"addresses.txt"

    # Read the data
    data = pd.read_csv(fp, sep=';')

.. ipython:: python
   :suppress:

    # THIS CODE WILL BE RUNNING IN BACKGROUND
    # ---------------------------------------
    import gdal
    import pandas as pd
    import geopandas as gpd
    from shapely.geometry import Point
    from geopandas.tools import geocode
    import os
    fp = os.path.join(os.path.abspath('data'), "addresses.txt")
    data = pd.read_csv(fp, sep=';')

.. ipython:: python

    # Let's take a look of the data
    data.head()

Now we have our data in a Pandas DataFrame and we can geocode our addresses.

- Let's
.. ipython:: python

    # Import the geocoding tool
    from geopandas.tools import geocode
    
    # Geocode addresses with Nominatim backend
    geo = geocode(data['addr'], provider='nominatim')
    geo.head(2)

And Voilà! As a result we have a GeoDataFrame that contains our original
address and a 'geometry' column containing Shapely Point -objects that
we can use for exporting the addresses to a Shapefile for example.
However, the ``id`` column is not there. Thus, we need to join the
information from ``data`` into our new GeoDataFrame ``geo``, thus making
a **Table Join**.

Table join
----------

Table joins are really common procedures when
doing GIS analyses. As you might remember from our earlier lessons, combining data from different tables based on common
``key`` attribute can be done easily in Pandas/Geopandas using `.merge() <https://geo-python.github.io/2017/lessons/L6/exercise-6-hints.html?highlight=merge#joining-data-from-one-dataframe-to-another>`__
-function.

However, sometimes it is useful to join two tables together based on the **index** of those DataFrames. In such case, we assume
that there is **same number of records** in our DataFrames and that the **order of the records should be the same** in both DataFrames.
In fact, now we have such a situation as we are geocoding our addresses where the order of the geocoded addresses in ``geo`` DataFrame is the same
as in our original ``data`` DataFrame.

Hence, we can join those tables together with ``join()`` -function which merges the two DataFrames together
based on index by default.

.. ipython:: python

    join = geo.join(data)
    join.head()

- Let's also check the data type of our new ``join`` table.

.. ipython:: python

    type(join)

As a result we have a new GeoDataFrame called ``join`` where we now have
all original columns plus a new column for ``geometry``.

-  Now it is easy to save our address points into a Shapefile

.. code:: python

    # Output file path
    outfp = r"/home/geo/addresses.shp"

    # Save to Shapefile
    join.to_file(outfp)

That's it. Now we have successfully geocoded those addresses into Points
and made a Shapefile out of them. Easy isn't it!

.. hint::

    Nominatim works relatively nicely if you have well defined and well-known addresses such as the ones that we used in this tutorial.
    However, in some cases, you might not have such well-defined addresses, and you might have e.g. only the name of a museum available.
    In such cases, Nominatim might not provide such good results, and in such cases you might want to use e.g. `Google Geocoding API (V3) <https://developers.google.com/maps/documentation/geocoding/>`__.
    Take a look from last year, `where we show how to use Google Geocoding API <https://automating-gis-processes.github.io/2016/Lesson3-geocoding.html#geocoding-in-geopandas>`__ in a similar manner as we used Nominatim here.