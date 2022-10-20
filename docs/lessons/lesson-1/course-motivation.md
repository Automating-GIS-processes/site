---
kernelspec:
  name: python3
  display_name: python3
jupytext:
  text_representation:
    extension: .md 
    format_name: myst
    format_version: '0.13'
    jupytext_version: 1.14.1
---

# Motivation behind this course

## General overview

Now that you are familiar with [the basics of Python
programming](https://geopython.readthedocs.io/), it is time to apply those
skills to geographic data analysis. During the ‘Automating GIS processes’
course, you will learn how to handle spatial data and analyse it using Python.
In the course, you also will get to know some of the many Python packages that
have been written specifically for GIS-related applications.


## Learning objectives

At the end of the course you will be able to:

- **read and write spatial data** from and to different file formats,
- work with **coordinate reference systems**,
- use **geocoding** to convert addresses to coordinates, and vice versa,
- use **overlay functions** to combine geometries (intersect, union),
- **reclassify data** based on their value,
- carry out **spatial queries**,
- conduct simple **spatial analysis**, and
- **visualise data** and create (interactive) maps, such as following:



% The following is copied from 
% https://docs.bokeh.org/en/latest/docs/gallery/texas.html
%
% Split into two cells, so we can hide the super-verbose
% output of the sample data download function, and the input
% (code) of both cells
%
% TODO: This is currently causing a warning from myst-nb:
%
% WARNING: skipping unknown output mime type: 
% application/vnd.bokehjs_load.v0+json [mystnb.unknown_mime_type]
%
% I haven’t really had the time to look into it. In the long run,
% it would be great if sphinx-build would run without any warnings
% (this here is the only one, right now)


```{code-cell}
:tags: ["remove-input", "remove-output"]

import bokeh.sampledata
bokeh.sampledata.download(progress=False)
```

```{code-cell}
:tags: ["remove-input"]

from bokeh.io import show
from bokeh.io import output_notebook
output_notebook(hide_banner=True)

from bokeh.models import LogColorMapper
from bokeh.palettes import Viridis6 as palette
from bokeh.plotting import figure

from bokeh.sampledata.unemployment import data as unemployment
from bokeh.sampledata.us_counties import data as counties


palette = tuple(reversed(palette))

counties = {
    code: county for code, county in counties.items() if county["state"] == "tx"
}

county_xs = [county["lons"] for county in counties.values()]
county_ys = [county["lats"] for county in counties.values()]

county_names = [county['name'] for county in counties.values()]
county_rates = [unemployment[county_id] for county_id in counties]
color_mapper = LogColorMapper(palette=palette)

data=dict(
    x=county_xs,
    y=county_ys,
    name=county_names,
    rate=county_rates,
)

TOOLS = "pan,wheel_zoom,reset,hover,save"

p = figure(
    title="Texas Unemployment, 2009", tools=TOOLS,
    x_axis_location=None, y_axis_location=None,
    tooltips=[
        ("Name", "@name"), ("Unemployment rate", "@rate%"), ("(Long, Lat)", "($x, $y)")
    ])
p.grid.grid_line_color = None
p.hover.point_policy = "follow_mouse"

p.patches('x', 'y', source=data,
          fill_color={'field': 'rate', 'transform': color_mapper},
          fill_alpha=0.7, line_color="white", line_width=0.5)

show(p)
```



<!-- CONTINUE UPDATING FROM HERE -->

## Why Python for GIS?

Python is an extremely useful language to learn in terms of GIS since many
(or most) of the different GIS Software packages (such as ArcGIS, QGIS,
PostGIS etc.) provide an interface to do analysis using Python
scripting. During this course, we will mostly focus on doing GIS without
any third party softwares such as ArcGIS. **Why?** There are several
reasons for doing GIS using Python without any additional software:

- **Everything is free**: you don't need to buy and expensive license
  for ArcGIS (for example)
- You will **learn and understand** much more deeply how different
  geoprocessing operations work
- Python is **highly efficient**: used for analysing Big Data
- Python is **highly flexible**: supports all data formats that you can
  imagine
- Using Python (or any other open-source programming language)
  **supports open source softwares/codes and open science** by making
  it possible for everyone to reproduce your work, free-of-charge.
- **Plug-in and chain different third-party softwares** to build e.g. a
  fancy web-GIS applications as you want (using e.g.
  [GeoDjango](https://docs.djangoproject.com/en/1.8/ref/contrib/gis/)
  with [PostGIS](http://postgis.net/) as a back-end)

## What sort of tools are available for doing GIS in pure Python?

We have already used few Python modules for conducting different tasks,
such as **numpy** for doing mathematical calculations or **matplotlib**
for visualizing our data. From now on, we will familiarize ourselves
with punch of other Python modules that are useful when doing data
analysis or different GIS tasks.

One drawback when compared to using a specific GIS-software such as
[ArcGIS](http://arcgis.com/), is that GIS tools are spread under different Python modules and
created by different developers. This means that you need to familiarize
yourself with many different modules (and their documentation), whereas
e.g. in ArcGIS everything is packaged under a same module called
[arcpy](http://desktop.arcgis.com/en/arcmap/10.3/analyze/arcpy/what-is-arcpy-.htm).

Below we have listed most of the crucial modules (and links to their
docs) that helps you get going when doing data analysis or GIS in
Python. If you are interested or when you start using these modules in
your own work, you should read the documentation from the web pages of
the module that you need:

- **Data analysis & visualization:**

  - [Numpy](http://www.numpy.org/) --> Fundamental package for
    scientific computing with Python
  - [Pandas](http://pandas.pydata.org/) --> High-performance,
    easy-to-use data structures and data analysis tools
  - [Scipy](http://www.scipy.org/about.html) --> A collection of
    numerical algorithms and domain-specific toolboxes, including
    signal processing, optimization and statistics
  - [Matplotlib](http://matplotlib.org/) --> Basic plotting library
    for Python
  - [Bokeh](http://bokeh.pydata.org/en/latest/) --> Interactive
    visualizations for the web (also maps)
  - [Plotly](https://plot.ly/python/) --> Interactive
    visualizations (also maps) for the web (commercial - free for
    educational purposes)

- **GIS:**

  - [GDAL](http://www.gdal.org/) --> Fundamental package for
    processing vector and raster data formats (many modules below
    depend on this). Used for raster processing.
  - [Geopandas](http://geopandas.org/#description) --> Working with
    geospatial data in Python made easier, combines the capabilities
    of pandas and shapely.
  - [Shapely](http://toblerity.org/shapely/manual.html) --> Python
    package for manipulation and analysis of planar geometric objects
    (based on widely deployed
    [GEOS](https://trac.osgeo.org/geos/)).
  - [Fiona](https://pypi.python.org/pypi/Fiona) --> Reading and
    writing spatial data (alternative for geopandas).
  - [Pyproj](https://pypi.python.org/pypi/pyproj?) --> Performs
    cartographic transformations and geodetic computations (based on
    [PROJ.4](http://trac.osgeo.org/proj)).
  - [Pysal](https://pysal.readthedocs.org/en/latest/) --> Library
    of spatial analysis functions written in Python.
  - [Geopy](http://geopy.readthedocs.io/en/latest/) --> Geocoding
    library: coordinates to address \<-> address to coordinates.
  - [Contextily](https://github.com/darribas/contextily) --> Add background basemaps for your (static) map visualizations
  - [GeoViews](http://geo.holoviews.org/index.html) --> Interactive
    Maps for the web.
  - [Geoplot](https://github.com/ResidentMario/geoplot) --> High-level geospatial data visualization library for Python.
  - [Dash](https://plot.ly/products/dash/) --> Dash is a Python framework for building analytical web applications.
  - [OSMnx](https://github.com/gboeing/osmnx) --> Python for street networks. Retrieve, construct, analyze, and visualize street networks from OpenStreetMap
  - [Networkx](https://networkx.github.io/documentation/networkx-1.10/overview.html)
    --> Network analysis and routing in Python (e.g. Dijkstra and A\*
    -algorithms), see [this
    post](http://gis.stackexchange.com/questions/65056/is-it-possible-to-route-shapefiles-using-python-and-without-arcgis-qgis-or-pgr).
  - [Cartopy](http://scitools.org.uk/cartopy/docs/latest/index.html)
    --> Make drawing maps for data analysis and visualisation as easy
    as possible.
  - [Scipy.spatial](http://docs.scipy.org/doc/scipy/reference/spatial.html)
    --> Spatial algorithms and data structures.
  - [Rtree](http://toblerity.org/rtree/) --> Spatial indexing for
    Python for quick spatial lookups.
  - [Rasterio](https://github.com/mapbox/rasterio) --> Clean and
    fast and geospatial raster I/O for Python.
  - [RSGISLib](http://www.rsgislib.org/index.html#python-documentation)
    --> Remote Sensing and GIS Software Library for Python.

:::{admonition} Install to your own computer!
See **directions how to install these modules to your own computer under** [the course info](Installing_Anacondas_GIS.html)
:::
