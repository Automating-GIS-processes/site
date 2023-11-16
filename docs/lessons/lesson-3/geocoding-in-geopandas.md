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

# Geocoding in geopandas

Geopandas supports geocoding via a library called
[geopy](http://geopy.readthedocs.io/), which needs to be installed to use
[geopandas’ `geopandas.tools.geocode()`
function](https://geopandas.org/en/stable/docs/reference/api/geopandas.tools.geocode.html).
`geocode()` expects a `list` or `pandas.Series` of addresses (strings) and
returns a `GeoDataFrame` with resolved addresses and point geometries.

Let’s try this out.

We will geocode addresses stored in a semicolon-separated text file called
`addresses.txt`. These addresses are located in the Helsinki Region in Southern
Finland.

```{code-cell}
import pathlib
NOTEBOOK_PATH = pathlib.Path().resolve()
DATA_DIRECTORY = NOTEBOOK_PATH / "data"
```

```{code-cell}
import pandas
addresses = pandas.read_csv(
    DATA_DIRECTORY / "helsinki_addresses" / "addresses.txt",
    sep=";"
)

addresses.head()
```

We have an `id` for each row and an address in the `addr` column.


## Geocode addresses using *Nominatim*

In our example, we will use *Nominatim* as a *geocoding provider*. [*Nominatim*](https://nominatim.org/) is a library and service using OpenStreetMap data, and run by the OpenStreetMap Foundation. Geopandas’
[`geocode()`
function](hhttps://geopandas.org/en/stable/docs/reference/api/geopandas.tools.geocode.html) supports it natively.


:::{admonition} Fair-use
:class: note

[Nominatim’s terms of use](https://operations.osmfoundation.org/policies/nominatim/)
require that users of the service make sure they don’t send more frequent
requests than one per second, and that a custom **user-agent** string is
attached to each query.

Geopandas’ implementation allows us to specify a `user_agent`; the library also
takes care of respecting the rate-limit of Nominatim.

Looking up an address is a quite expensive database operation. This is why,
sometimes, the public and free-to-use Nominatim server takes slightly longer to
respond. In this example, we add a parameter `timeout=10` to wait up to 10
seconds for a response.
:::


```{code-cell}
import geopandas

geocoded_addresses = geopandas.tools.geocode(
    addresses["addr"],
    provider="nominatim",
    user_agent="autogis2023",
    timeout=10
)
geocoded_addresses.head()
```

Et voilà! As a result we received a `GeoDataFrame` that contains a parsed
version of our original addresses and a `geometry` column of
`shapely.geometry.Point`s that we can use, for instance, to export the data to
a geospatial data format.

However, the `id` column was discarded in the process. To combine the input
data set with our result set, we can use pandas’ [*join*
operations](https://pandas.pydata.org/docs/user_guide/merging.html).


## Join data frames

:::{admonition} Joining data sets using pandas
:class: note

For a comprehensive overview of different ways of combining DataFrames and
Series based on set theory, have a look at pandas documentation about [merge,
join and
concatenate](https://pandas.pydata.org/pandas-docs/stable/user_guide/merging.html).
:::


Joining data from two or more data frames or tables is a common task in many
(spatial) data analysis workflows. As you might remember from our earlier
lessons, combining data from different tables based on common **key** attribute
can be done easily in pandas/geopandas using the [`merge()`
function](https://pandas.pydata.org/pandas-docs/stable/generated/pandas.DataFrame.merge.html).
We used this approach in [exercise 6 of the Geo-Python
course](https://geo-python-site.readthedocs.io/en/latest/lessons/L6/exercise-6.html#joining-data-from-one-dataframe-to-another).

However, sometimes it is useful to join two data frames together based on their
**index**. The data frames have to have the **same number of records** and
**share the same index** (simply put, they should have the same order of rows).

We can use this approach, here, to join information from the original data
frame `addresses` to the geocoded addresses `geocoded_addresses`, row by row.
The `join()` function, by default, joins two data frames based on their index.
This works correctly for our example, as the order of the two data frames is
identical.

```{code-cell}
geocoded_addresses_with_id = geocoded_addresses.join(addresses)
geocoded_addresses_with_id
```

The output of `join()` is a new `geopandas.GeoDataFrame`:

```{code-cell}
type(geocoded_addresses_with_id)
```

The new data frame has all original columns plus new columns for the `geometry`
and for a parsed `address` that can be used to spot-check the results.

:::{note}
If you would do the join the other way around, i.e. `addresses.join(geocoded_addresses)`, the output would be a `pandas.DataFrame`, not a `geopandas.GeoDataFrame`.
:::


---


It’s now easy to save the new data set as a geospatial file, for instance, in
*GeoPackage* format:

```{code-cell}
:tags: ["remove-input", "remove-output"]

# delete a possibly existing file, as it creates
# troubles in case sphinx is run repeatedly
try:
    (DATA_DIRECTORY / "addresses.gpkg").unlink()
except FileNotFoundError:
    pass
```

```{code-cell}
geocoded_addresses.to_file(DATA_DIRECTORY / "addresses.gpkg")
```
