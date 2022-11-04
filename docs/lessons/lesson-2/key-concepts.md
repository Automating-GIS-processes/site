# Key concepts

:::{admonition} **Check your understanding**
Before diving into this week's Python lesson, you should already be familiar with some basic
spatial data file formats and projection definitions, such as these:

- Shapefile
- GeoPackage
- CRS
- Datum
- EPSG
:::

:::{admonition} **Definitions**
**Shapefile:** a vector data format for storing location information and related attributes.
A shapefile consist of several files with a common prefix that need to be stored in the same directory.
`.shp`, `shx` and `.dbf` are required file extensions in a shapefile. Other file extensions are not required,
but for example the file extension `.prj` is often essential. More information about Shapefile file extensions
in [here](<http://help.arcgis.com/en/arcgisdesktop/10.0/help/index.html#/Shapefile_file_extensions/005600000003000000/)>).
The shapefile format is developed by ESRI.

**GeoPackage:** an open source format for storing and transferring geospatial information.
GeoPackages are able to store both vector data and raster data. In more detail, GeoPackage is a container for
an SQLite database with a `.gpkg` extension (all in one file!). The GeoPackage format is governed by the Open GeoSpatial Consortium.
More information at: <https://www.geopackage.org/>

**CRS:** Coordinate reference systems define how coordinates relate to real locations on the Earth.
*Geographic coordinate reference systems* commonly use latitude and longitude degrees.
*Projected coordinate reference systems* use  x and y coordinates to represent locations on a flat surface.
You will learn more about coordinate reference systems during this lesson!

**Datum:** defines the center point, orientation, and scale of the reference surface related to a coordinate reference system.
Same coordinates can relate to different locations depending on the Datum! For example, WGS84 is a widely used global datum.
ETRS89 is a datum used in Europe. Coordinate reference systems are often named based on the datum used.

**EPSG:** EPSG codes refer to specific reference systems.
EPSG stands for "European Petroleum Survey Group" that originally published a database for spatial reference systems.
For example, [EPSG:3067](https://spatialreference.org/ref/epsg/3067/) refers to coordinate reference system ETRS-TM35FIN which is commonly used in Finland.
[EPSG:4326](https://spatialreference.org/ref/epsg/4326/) refers to WGS84. You can search for EPSG codes at: <https://spatialreference.org/>
:::
