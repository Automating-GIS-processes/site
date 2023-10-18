---
jupytext:
  text_representation:
    extension: .md
    format_name: myst
    format_version: 0.13
    jupytext_version: 1.14.0
kernelspec:
  display_name: Python 3 (ipykernel)
  language: python
  name: python3
---

# Vector Data I/O

One of the first steps of many analysis workflow is to read data from a file,
one of the last steps often writes data to an output file.  To the horror of
many geoinformatics scholars, there exist many file formats for GIS data: the
old and hated but also loved and established [ESRI
Shapefile](https://en.wikipedia.org/wiki/Shapefile), the universal [Geopackage
(GPKG)](https://en.wikipedia.org/wiki/GeoPackage), and the web-optimised
[GeoJSON](https://en.wikipedia.org/wiki/GeoJSON) are just a few of the more
well-known examples.

Fear not, Python can read them all (no guarantees, though)! 

Most of the current Python GIS packages rely on the
[GDAL/OGR](https://gdal.org/) libraries, for which modern interfaces exist in
the form of the [fiona](https://fiona.readthedocs.io) and
[rasterio](https://rasterio.readthedocs.io) Python packages. 

Today, we’ll concentrate on vector data, so let’s first take a closer look at
fiona’s capabilities, and then import and export data using
[geopandas](https://geopandas.org/), which uses fiona under its hood.


---


:::{admonition} Defining a data directory constant
:class: note

To make it easier to manage the paths of input and output data files, it is a
good habit to [define a constant pointing to the data
directory](managing-file-paths) at the top of a notebook:

:::

```{code-cell}
import pathlib 
NOTEBOOK_PATH = pathlib.Path().resolve()
DATA_DIRECTORY = NOTEBOOK_PATH / "data"
```


---


## File formats

Fiona can read (almost) any geospatial file format, and write many of them. To
find out which ones exactly (it might depend on the local installation and
version, as well), we can print its list of file format drivers:

```{code-cell}
import fiona
fiona.supported_drivers
```

:::{hint}
In this list, `r` marks file formats fiona can *r*ead, and `w` formats it can
*w*rite. An `a` marks formats for which fiona can *a*ppend new data to existing
files.

Note that each of the listed ‘formats’ is, in fact, the name of the driver
implementation, and many of the drivers can open several related file formats.

Many more ‘exotic’ file formats might not show up in this list of your local
installation, because you would need to install additional libraries. You can
find a full list of file formats supported by GDAL/OGR (and fiona) on its
webpage: [gdal.org/drivers/vector/](https://gdal.org/drivers/vector/).
:::


### Reading and writing geospatial data

Fiona allows very low-level access to geodata files. This is sometimes
necessary, but in typical analysis workflows, it is more convenient to use a
higher-level library. The most commonly used one for geospatial vector data is
[geopandas](https://geopandas.org). As mentioned above, it uses fiona for
reading and writing files, and thus supports the same file formats.

To read data from a *GeoPackage* file into a `geopandas.GeoDataFrame` (a
geospatially-enabled version of a `pandas.DataFrame`), use
`geopandas.read_file()`:

```{code-cell}
import geopandas
municipalities = geopandas.read_file(
    DATA_DIRECTORY / "finland_municipalities" / "finland_municipalities_2021.gpkg"
)
municipalities.head()
```

Reading a local GPKG file is most likely the easiest task for a GIS package.
However, in perfect Python ‘Swiss pocket knife’ manner, geopandas can also read
Shapefiles **inside a ZIP archive**, and/or straight **from an Internet URL**.
For example, downloading, unpacking and opening a data set of NUTS regions from
the [European Union’s GISCO/eurostat download
page](https://ec.europa.eu/eurostat/web/gisco/geodata/reference-data/administrative-units-statistical-units/nuts)
is one line of code:


% ----------- TODO --------------
% GISCO starting blocking requests from geopandas 2022-12, responding
% with a HTTP 403 (Forbidden) error. Faking this for now, but for next
% year, we should find a new example

```{code}
nuts_regions = geopandas.read_file("https://gisco-services.ec.europa.eu/distribution/v2/nuts/shp/NUTS_RG_60M_2021_3035.shp.zip")
nuts_regions.head()
```

```{code-cell}
:tags: ["remove-input", "remove-output"]
nuts_regions = geopandas.read_file(DATA_DIRECTORY / "europe_nuts_regions.geojson")
nuts_regions.head()
```


#### Writing geospatial data to a file

Writing data to a file is equally straight-forward: simply use the [`to_file()`
method](https://geopandas.org/en/stable/docs/reference/api/geopandas.GeoDataFrame.to_file.html#geopandas.GeoDataFrame.to_file)
of a `GeoDataFrame`.

If we want to keep a local copy of the NUTS region data set we just opened
on-the-fly from an internet address, the following saves the data to a GeoJSON
file (the file format is guessed from the file name):

```{code-cell}
nuts_regions.to_file(DATA_DIRECTORY / "europe_nuts_regions.geojson")
```

:::{note}

Reading and writing geospatial data from or to a file is almost identical for
all file formats supported by geopandas, fiona, and GDAL. Check out [geopandas’
documentation](https://geopandas.org/en/stable/docs/user_guide/io.html) for
hints on how to fine-tune reading or writing a file, and how to apply different
filters (e.g., bounding boxes).
:::


### Reading and writing from and to databases (RDBMS)

Geopandas has native support for read/write access to PostgreSQL/PostGIS
databases, using its
[`geopandas.read_postgis()`](https://geopandas.org/en/stable/docs/reference/api/geopandas.read_postgis.html) function and the
[`GeoDataFrame.to_postgis()`](https://geopandas.org/en/stable/docs/reference/api/geopandas.GeoDataFrame.to_postgis.html)
method. For the database connection, you can use, for instance, the
`sqlalchemy` package.

```{code}
import sqlalchemy
DB_CONNECTION_URL = "postgresql://myusername:mypassword@myhost:5432/mydatabase";
db_engine = sqlalchemy.create_engine(DB_CONNECTION_URL)

countries = geopandas.read_postgis(
    "SELECT name, geometry FROM countries",
    db_engine
)
countries.to_postgis(
    "new_table", 
    db_engine
)
```


### Reading data directly from a WFS (Web feature service) endpoint

Geopandas can also read data directly from a WFS endpoint, such as, for instance the geodata APIs of [Helsinki Region Infoshare](https://hri.fi). Constructing a valid WFS URI (address) is not part of this course (but check, for instance, the properties of a layer added to QGIS).

The following code loads a population grid of Helsinki from 2022. The parameters encoded into the WFS address specify the layer name, a bounding box, and the requested reference system.


```{code}
population_grid = geopandas.read_file(
    "https://kartta.hsy.fi/geoserver/wfs"
    "?service=wfs"
    "&version=2.0.0"
    "&request=GetFeature"
    "&typeName=asuminen_ja_maankaytto:Vaestotietoruudukko_2022"
    "&srsName=EPSG:3879"
    "&bbox=25494767,6671328,25497720,6673701,EPSG:3879",
    crs="EPSG:3879"
)
population_grid.head()
```

```{code-cell}
:tags: ["remove-input"]

population_grid = geopandas.read_file(
    "https://avoidatastr.blob.core.windows.net/avoindata/AvoinData/"
    "6_Asuminen/Vaestotietoruudukko/Shp/Vaestotietoruudukko_2021_shp.zip"
)
population_grid.head()
```
