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
-  `Open Street Map
   Nominatim <https://wiki.openstreetmap.org/wiki/Nominatim>`__
-  `SmartyStreets <https://smartystreets.com/products/liveaddress-api>`__
-  `What3words <http://what3words.com/api/reference>`__
-  `Yandex <http://api.yandex.com/maps/doc/intro/concepts/intro.xml>`__

Thus, there is plenty of geocoders where to choose from! However, to be
able to use these services you might need to request so called API
access-keys from the service provider to be able to use the service. You
can get your access keys to e.g. Google Geocoding API from `Google APIs
console <https://code.google.com/apis/console>`__ by creating a Project
and enabling a that API from
`Library <https://console.developers.google.com/apis/library>`__. Read a
short introduction about using Google API Console from
`here <https://developers.googleblog.com/2016/03/introducing-google-api-console.html>`__.

.. note::

    There are also other Python modules in addition to geopy that can do
    geocoding such as `Geocoder <http://geocoder.readthedocs.io/>`__.

Geocoding in Geopandas
----------------------

It is possible to do geocoding in Geopandas using its integrated
functionalities of geopy. Geopandas has a function called ``geocode()``
that can geocode a list of addresses (strings) and return a GeoDataFrame
containing the resulting point objects in ``geometry`` column. Nice,
isn't it! Let's try this out.

Download a text file called `addresses.txt <https://raw.githubusercontent.com/Automating-GIS-processes/Lesson-3-Geocoding-Spatial-Queries/master/data/addresses.txt>`__ that
contains few addresses around Helsinki Region. The first rows of the
data looks like following:

.. parsed-literal::

    id;address
    1000;Itämerenkatu 14, 00101 Helsinki, Finland
    1001;Kampinkuja 1, 00100 Helsinki, Finland
    1002;Kaivokatu 8, 00101 Helsinki, Finland
    1003;Hermanstads strandsväg 1, 00580 Helsingfors, Finland

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

-  Now we have our data in a Pandas DataFrame and we can geocode our
   addresses

.. note::

    Here we use my API key that has a limitation of 2500 requests / hour. Because of this, only the computer instances of our course environment have access to Google Geocoding API for a short period of time. Thus, the following key will NOT work from your own computer, only from our cloud computers. If you wish, you can create your own API key to Google Geocoding API V3 from `Google APIs console <https://code.google.com/apis/console>`_. See the notes from `above <Lesson3-geocoding.html#overview-of-geocoders>`_.


.. ipython:: python

    # Import the geocoding tool
    from geopandas.tools import geocode
    
    # Key for our Google Geocoding API 
    # Notice: only the cloud computers of our course can access and
    # successfully execute the following
    key = 'AIzaSyAwNVHAtkbKlPs-EEs3OYqbnxzaYfDF2_8'
    
    # Geocode addresses
    geo = geocode(data['address'], api_key=key)
    
    geo.head(2)

And Voilà! As a result we have a GeoDataFrame that contains our original
address and a 'geometry' column containing Shapely Point -objects that
we can use for exporting the addresses to a Shapefile for example.
However, the ``id`` column is not there. Thus, we need to join the
information from ``data`` into our new GeoDataFrame ``geo``, thus making
a **Table Join**.