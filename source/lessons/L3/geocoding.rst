Geocoding
=========

Overview of Geocoders
---------------------

Geocoding is the process of transforming place names or addresses into coordinates.
In this lesson we will learn how to geocode addresses using Geopandas and
`geopy <https://geopy.readthedocs.io/en/stable/>`__. Geopy makes it easy to
locate the coordinates of addresses, cities, countries, and landmarks
across the globe using different geocoding web services ("geocoders").

Several different geocoding services are available via geopy, including these:

-  `ESRI ArcGIS <https://developers.arcgis.com/rest/geocode/api-reference/overview-world-geocoding-service.htm>`__
-  `Baidu Maps <http://lbsyun.baidu.com/index.php?title=webapi/guide/webservice-geocoding>`__
-  `Bing <https://msdn.microsoft.com/en-us/library/ff701715.aspx>`__
-  `GeocodeFarm <https://www.geocode.farm/geocoding/free-api-documentation/>`__
-  `GeoNames <http://www.geonames.org/export/geonames-search.html>`__
-  `Google Geocoding API (V3) <https://developers.google.com/maps/documentation/geocoding/>`__
-  `IGN France <https://geoservices.ign.fr/documentation/geoservices/index.html>`__
-  `Mapquest <https://developer.mapquest.com/documentation/open/>`__
-  `OpenCage <https://opencagedata.com/api>`__
-  `OpenMapQuest <http://developer.mapquest.com/web/products/open/geocoding-service>`__
-  `Open Street Map Nominatim <https://wiki.openstreetmap.org/wiki/Nominatim>`__
-  `What3words <https://developer.what3words.com/public-api/docsv2#overview>`__
-  `Yandex <https://tech.yandex.com/maps/doc/geocoder/desc/concepts/input_params-docpage/>`__

Chec the `Geopy documentation <https://geopy.readthedocs.io/en/stable/>`__ for more details
about how to use each service.

As you see, there are plenty of geocoders where to choose from! However, for most of these services you might need to
request API access-keys from the service provider to be able to use the service.

Luckily, Nominatim, which is a geocoder based on OpenStreetMap data does not require a API key to use their service
if it is used for small scale geocoding jobs as the service is rate-limited to 1 request per second (3600 / hour).
As we are only making a small set of queries, we can do the geocoding by using Nominatim.

.. note::

   - **Note 1:** If you need to do larger scale geocoding jobs, use and request an API key to some of the
   geocoders listed above.

   - **Note 2:** There are also other Python modules in addition to geopy that can do geocoding such as `Geocoder <http://geocoder.readthedocs.io/>`__.

.. hint::

    You can get your access keys to e.g. Google Geocoding API from `Google APIs console <https://code.google.com/apis/console>`__ by creating a Project
    and enabling a that API from `Library <https://console.developers.google.com/apis/library>`__. Read a
    short introduction about using Google API Console from `here <https://developers.googleblog.com/2016/03/introducing-google-api-console.html>`__.
