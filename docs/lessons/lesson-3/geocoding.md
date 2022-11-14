# Geocoding

## Overview of Geocoders

Geocoding is the process of transforming place names or addresses into
coordinates.  In this lesson we will learn how to geocode addresses using
Geopandas and [geopy](https://geopy.readthedocs.io/en/stable/).

Geopy and other geocoding libaries (such as
[geocoder](http://geocoder.readthedocs.io/)) make it easy to locate the
coordinates of addresses, cities, countries, and landmarks across the globe
using web services ("geocoders"). In practice, geocoders are often Application
Programming Interfaces (APIs) where you can send requests, and receive
responses in the form of place names, addresses and coordinates.

Geopy offers access to several geocoding services, including:

- [ESRI ArcGIS](https://developers.arcgis.com/rest/geocode/api-reference/overview-world-geocoding-service.htm)
- [Baidu Maps](http://lbsyun.baidu.com/index.php?title=webapi/guide/webservice-geocoding)
- [Bing](https://msdn.microsoft.com/en-us/library/ff701715.aspx)
- [GeocodeFarm](https://www.geocode.farm/geocoding/free-api-documentation/)
- [GeoNames](http://www.geonames.org/export/geonames-search.html)
- [Google Geocoding API (V3)](https://developers.google.com/maps/documentation/geocoding/)
- [HERE](https://developer.here.com/documentation/geocoder/)
- [IGN France](https://geoservices.ign.fr/documentation/geoservices/index.html)
- [Mapquest](https://developer.mapquest.com/documentation/open/)
- [OpenCage](https://opencagedata.com/api)
- [OpenMapQuest](http://developer.mapquest.com/web/products/open/geocoding-service)
- [Open Street Map Nominatim](https://wiki.openstreetmap.org/wiki/Nominatim)
- [What3words](https://developer.what3words.com/public-api/docsv2#overview)
- [Yandex](https://tech.yandex.com/maps/doc/geocoder/desc/concepts/input_params-docpage/)

Check the [geopy documentation](https://geopy.readthedocs.io/en/stable/) for
more details about how to use each service via Python.

As you see, there are plenty of geocoders where to choose from! The quality of
the geocoders might differ depending on the underlying data. For example, some
addresses might exists on OpenStreetMap, but not on Google Maps and thus they
can be geocoded using the Nominatim geocoder, but not using the Google
Geocoding API - and vice versa.

Geocoding services might require an **API key** in order to use them. (i.e. you
need to register for the service before you can access results from their API).
Furthermore, **rate limiting** also restrict the use of these services.  The
geocoding process might end up in an error if you are making too many requests
in a short time period (eg.  trying to geocode large number of addresses). See
hints for dealing with rate limiting when geocoding pandas DataFrames from the
[geopy documentation](https://geopy.readthedocs.io/en/stable/#usage-with-pandas). 
If you pay for the geocoding service, you can naturally make more requests to the
API.

In this lesson we will use the Nominatim geocoder for locating a relatively
small number of addresses.  Usage of the Nominatim geocoding service is
rate-limited to 1 request per second (3600 / hour). You can read more about
Nominatim usage policy in
[here](https://operations.osmfoundation.org/policies/nominatim/)

Luckily, Nominatim, which is a geocoder based on OpenStreetMap data does not
require a API key to use their service if it is used to geocode only a small
number of addresses.

:::{note}
Always check the terms of service of the geocoding service that you are using!
:::

:::{caution}
As noted in the [geopy documentation for the Nominatim geocoder](https://geopy.readthedocs.io/en/stable/#nominatim)
we need to specify a custom `user_agent` parameter when making requests not to violate the
[Nominatim Usage Policy](https://operations.osmfoundation.org/policies/nominatim/).
:::
