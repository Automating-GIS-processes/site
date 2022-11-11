---
jupytext:
  text_representation:
    extension: .md
    format_name: myst
    format_version: 0.13
    jupytext_version: 1.14.1
kernelspec:
  display_name: Python 3 (ipykernel)
  language: python
  name: python3
---

+++ {"deletable": true, "editable": true}

# Geocoding in Geopandas

It is possible to do [geocoding in Geopandas](http://geopandas.org/geocoding.html) through [geopy](
). Geopandas has a function called `geocode()` that can geocode a list of addresses (strings) and return a GeoDataFrame containing the resulting point objects in ``geometry`` column. 

Let's try this out.

We will geocode addresses stored in a text file called `addresses.txt`. These addresses are located in the Helsinki Region in Southern Finland.

The first rows of the data look like this:

```
id;addr
1000;Itämerenkatu 14, 00101 Helsinki, Finland
1001;Kampinkuja 1, 00100 Helsinki, Finland
1002;Kaivokatu 8, 00101 Helsinki, Finland
1003;Hermannin rantatie 1, 00580 Helsinki, Finland
```

We have an `id` for each row and an address on column `addr`.

Let's first read the data into a Pandas DataFrame using the `read_csv()` -function:

```{code-cell} ipython3
:deletable: true
:editable: true

# Import necessary modules
import pandas as pd
import geopandas as gpd
from shapely.geometry import Point

# Filepath
fp = r"data/addresses.txt"

# Read the data
data = pd.read_csv(fp, sep=';')
```

Let's check that we imported the file correctly:

```{code-cell} ipython3
len(data)
```

```{code-cell} ipython3
---
deletable: true
editable: true
jupyter:
  outputs_hidden: false
---
data.head()
```

+++ {"deletable": true, "editable": true}

## Geocode addresses using Nominatim

Now we have our data in a pandas DataFrame and we can geocode our addresses using the [geopandas geocoding function](http://geopandas.org/reference/geopandas.tools.geocode.html#geopandas-tools-geocode) that uses `geopy` package in the background. 

- Let's import the geocoding function and geocode the addresses (column `addr`) using Nominatim. 
- Remember to provide a custom string (name of your application) in the `user_agent` parameter.
- If needed, you can add the `timeout`-parameter which specifies how many seconds we will wait for a response from the service.

```{code-cell} ipython3
---
deletable: true
editable: true
jupyter:
  outputs_hidden: false
---
# Import the geocoding tool
from geopandas.tools import geocode

# Geocode addresses using Nominatim. Remember to provide a custom "application name" in the user_agent parameter!
geo = geocode(data['addr'], provider='nominatim', user_agent='autogis_xx', timeout=4)
```

```{code-cell} ipython3
geo.head()
```

+++ {"deletable": true, "editable": true}

And Voilà! As a result we have a GeoDataFrame that contains our original
address and a 'geometry' column containing Shapely Point -objects that
we can use for exporting the addresses to a Shapefile for example.
However, the ``id`` column is not there. Thus, we need to join the
information from ``data`` into our new GeoDataFrame ``geo``, thus making
a **Table Join**.

+++

<div class="alert alert-info">

**Rate-limiting**

When geocoding a large dataframe, you might encounter an error when geocoding. In case you get a time out error, try first using the `timeout` parameter as we did above (allow the service a bit more time to respond). In case of Too Many Requests error, you have hit the rate-limit of the service, and you should slow down your requests. To our convenience, geopy provides additional tools for taking into account rate limits in geocoding services. This script adapts the usage of [geopy RateLimiter](https://geopy.readthedocs.io/en/stable/#geopy.extra.rate_limiter.RateLimiter) to our input data:

```
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter
from shapely.geometry import Point

# Initiate geocoder
geolocator = Nominatim(user_agent='autogis_xx')

# Create a geopy rate limiter:
geocode_with_delay = RateLimiter(geolocator.geocode, min_delay_seconds=1)

# Apply the geocoder with delay using the rate limiter:
data['temp'] = data['addr'].apply(geocode_with_delay)

# Get point coordinates from the GeoPy location object on each row:
data["coords"] = data['temp'].apply(lambda loc: tuple(loc.point) if loc else None)

# Create shapely point objects to geometry column:
data["geometry"] = data["coords"].apply(Point)
```
All in all, remember that Nominatim is not meant for super heavy use. 
</div>

+++ {"deletable": true, "editable": true}

## Table join

<div class="alert alert-info">

**Table joins in pandas**
    
For a comprehensive overview of different ways of combining DataFrames and Series based on set theory, have a look at pandas documentation about [merge, join and concatenate](https://pandas.pydata.org/pandas-docs/stable/user_guide/merging.html).


</div>


Joining data between two or several tables is a common task in many (spatial) data analysis workflows. As you might remember from our earlier lessons, combining data from different tables based on common
**key** attribute can be done easily in pandas/geopandas using the [merge()](https://pandas.pydata.org/pandas-docs/stable/generated/pandas.DataFrame.merge.html) -function. We used this approach in the geo-python course [exercise 6](https://geo-python-site.readthedocs.io/en/latest/lessons/L6/exercise-6.html#joining-data-from-one-dataframe-to-another).

However, sometimes it is useful to join two tables together based on the **index** of those DataFrames. In such case, we assume
that there is **same number of records** in our DataFrames and that the **order of the records should be the same** in both DataFrames.

We can use this approach to join information from the original data to our geocoded addresses row-by-row 
``join()`` -function which merges the two DataFrames together
based on index by default. This approach works correctly because the order of the geocoded addresses in ``geo`` DataFrame is the same as in our original ``data`` DataFrame.

```{code-cell} ipython3
---
deletable: true
editable: true
jupyter:
  outputs_hidden: false
---
join = geo.join(data)
join.head()
```

+++ {"deletable": true, "editable": true}

Let's also check the data type of our new ``join`` table.

```{code-cell} ipython3
---
deletable: true
editable: true
jupyter:
  outputs_hidden: false
---
type(join)
```

+++ {"deletable": true, "editable": true}

As a result we have a new GeoDataFrame called ``join`` where we now have
all original columns plus a new column for ``geometry``. **Note!** If you would do the join the other way around, i.e. `data.join(geo)`, the output would be a pandas DataFrame, not a GeoDataFrame!


+++

Now it is easy to save our address points into a Shapefile

```{code-cell} ipython3
:deletable: true
:editable: true

# Output file path
outfp = r"data/addresses.shp"

# Save to Shapefile
join.to_file(outfp)
```

+++ {"deletable": true, "editable": true}

That's it. Now we have successfully geocoded those addresses into Points
and made a Shapefile out of them. Easy isn't it!

+++ {"deletable": true, "editable": true}

### Notes about Nominatim

Nominatim works relatively nicely if you have well defined and well-known addresses such as the ones that we used in this tutorial. In practice, the address needs to exist in the OpenStreetMap database. Sometimes, however, you might want to geocode a "point-of-interest", such as a museum, only based on it's name. If the museum name is not on OpenStreetMap, Nominatim won't provide any results for it, but you might be able to geocode the place using some other geocoder such as the [Google Geocoding API (V3)](https://developers.google.com/maps/documentation/geocoding/), which requires an API key. [Take a look from past year's materials where we show how to use Google Geocoding API](https://automating-gis-processes.github.io/2016/Lesson3-geocoding.html#geocoding-in-geopandas) in a similar manner as we used Nominatim here.
