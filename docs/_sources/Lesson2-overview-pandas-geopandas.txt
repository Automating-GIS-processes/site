Pandas and Geopandas -modules
=============================

`Pandas <http://pandas.pydata.org>`__ is a modern, powerful and
feature rich library that is designed for doing data analysis in Python.
It is a mature data analytics framework that is widely used among
different fields of science, thus there exists a lot of good examples
and documentation that can help you get going with your data analysis
tasks. In Pandas the data is typically stored into a **DataFrame** that
looks like a typical table with rows and columns (+ indices and column
names), where columns can contain data of different data types. Thus, it
reminds a little bit of how data is stored e.g. in Excel or in R that
also uses a concept of dataframe.

Pandas takes advantage of **numpy** -module which runs under the hood,
thus it is fast and powerful and can handle efficiently even large
datasets. Pandas, however, is much feature-rich module and it also makes
some of the same functionalities that numpy has much easier and more
intuitive to use, such as creating new empty columns and doing data
selections. Thus, it was useful to learn a little bit of how numpy works
since many features included in pandas uses the same syntax as numpy.
However, all numpy functions are not included in pandas, such as
``np.linspace()`` or ``np.arange()``, hence it is really common to see
that pandas and numpy -modules are both imported and used in a same
Python script.

Compared to numpy, pandas is also a more flexible and feature rich
module (or framework) as it combines functionalities from other
scientific Python -modules as well, such as `scipy <https://www.scipy.org/>`__ and
`matplotlib <http://matplotlib.org/>`__ for visualization purposes. Thus, you can use many
of the features included in those packages even without importing them
at all.

`Geopandas <http://geopandas.org/#description>`__ is a Python
module that is built on top of `Pandas <http://pandas.pydata.org/>`__
extending its functionalities.
data analysis library. Geopandas makes it possible to work with
spatial data stored e.g. in Shapefiles or PostGIS database. As
Geopandas is built on top of Pandas, it means that all functionalities
of pandas works also in geopandas. Geopandas has many nice built-in
spatial processing / analysis features such as overlay analysis,
geocoding, spatial aggregation methods and attribute / spatial joins
that are all fairly useful and commonly used GIS-functionalities.
It is also possible to do some simple processing with rasters using
geopandas with `rasterio <https://github.com/mapbox/rasterio>`__
module (see
`example <http://gis.stackexchange.com/questions/151339/rasterize-a-shapefile-with-geopandas-or-fiona-python>`__),
however there are more feature-rich Python modules for doing raster
analysis (will be covered during the Lesson 7.

