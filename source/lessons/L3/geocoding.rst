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
