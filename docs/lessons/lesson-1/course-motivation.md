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


## Why Python for GIS?

When it comes to data science, and especially spatial data science and spatial
data analysis, Python currently is the most useful programming or scripting 
language to learn. On the one hand, the Python ecosystem, which allows people to
share their libraries easily with others, is very rich, and has packages for
almost any task imaginable. Researchers who find that a particular tool does not
exist, often go ahead and create it themselves. Python’s packages cover such a
broad range of applications, that its `import` statement has become the trope of
many jokes:


:::{figure} https://imgs.xkcd.com/comics/python.png
:name: xkcd-353-Python
:alt: I wrote 20 short programs in Python yesterday. It was wonderful. Perl, I'm leaving you.

Learning to do *anything* is easy in Python: there is a package for everything. *Source: [xkcd.com/353](https://xkcd.com/353/)*
:::


There are more advantages more specifically for geographers and spatial data:
most desktop GIS (e.g., QGIS, ESRI ArcGIS) have language bindings or programming
interfaces for Python: that means that you can write Python programs that
interact with data, libraries, and user interface of these applications, and
create custom plugins to extend their functionality. Beyond that, here are 
powerful Python packages for virtually any task regarding spatial data
management and spatial analysis.

During this course, we will focus on the latter: carrying GIS analysis and data
management tasks _without_ a desktop GIS, let alone a proprietary third-party
software package such as ESRI ArcGIS. **Why?** There’s more than one reason:

- Python itself, and most packages for it, is open source. It means it’s **free
  to use** (as in *free beer*), and **free to modify** for your own purposes (as
  in *free speech*). Open source and *libre software* is inherently democratic:
  you don’t have to rely on access to a license, and anybody across the globe can
  use them. [Read more about *free beer* vs. *free speech* at the Free Software
  Foundation’s web page](https://www.gnu.org/philosophy/free-sw.en.html)
- Writing a script that solves a problem makes you **learn and understand more
  deeply** how geo-processing operations work, and how they work together. In
  this course, you will gain a deeper understanding of GIS.
- Python is **efficient** and **scales** very well: You can use a Python script
  to analyse *Big Data* and other large datasets, and it is likely to outperform
  any desktop GIS tool.
- Python is **highly flexible**: it can read and write almost any data format,
  and its [package ecosystem](../../course-info/installing-python)
  provides libraries for almost any programming task imaginable.
- Using Python, or any other open source software, for what it’s worth, supports
  the ideas of **open science** and **reproducable research**. Anyone can take
  your code and repeat your experiment or analysis to verify your claims and to
  learn from your example.
- **Combining the functionality of different Python packages** you can achieve
  surprising results with comparably low effort: e.g., building fancy web-GIS
  applications by chaining
  [GeoDjango](https://docs.djangoproject.com/en/4.1/ref/contrib/gis/tutorial/)
  with a PostGIS backend.


## Which GIS packages are available in Python?

During the [GeoPython course](https://geo-python.github.io/), we have already
used a few Python modules for carrying out different tasks, such as **numpy**
for mathematical calculations, and **matplotlib** for data visualisation. In
’AutoGIS’, we will get to know a range of other Python packages that are useful
for data analysis and the handling of geo-spatial data sets.

Below we listed most of the most common Python packages for GIS and data
analysis (and links to their documentation). This list helps you get started
when you approach a data analysis or GIS problem (but be sure to also use your
favourite search engine to see if better alternatives have become available). 

Even if you learnt about a package from a blog post, or from this course, always
check the package’s own documentation page for its recommended use.


- **Data analysis & visualization:**

  - [NumPy](http://www.numpy.org/): Fundamental package for scientific
    computing with Python
  - [Pandas](http://pandas.pydata.org/): High-performance, easy-to-use data
    structures and data analysis tools
  - [SciPy](http://www.scipy.org/about.html): A collection of numerical
    algorithms and domain-specific toolboxes, including signal processing,
    optimization and statistics
  - [MatplotLib](http://matplotlib.org/): Basic plotting library for Python
  - [Bokeh](http://bokeh.pydata.org/en/latest/): Interactive visualizations for
    the web (also maps)
  - [Plotly](https://plot.ly/python/): Interactive visualizations (also maps)
    for the web (commercial - free for educational purposes)

- **GIS:**

  - [GDAL](https://www.gdal.org/): Fundamental package for processing vector
    and raster data formats (many modules below depend on this). Used for
    raster processing.
  - [Geopandas](https://geopandas.org/): Working with geospatial data in Python
    made easier, combines the capabilities of pandas and shapely.
  - [Shapely](https://shapely.readthedocs.io/): Python package for manipulation
    and analysis of planar geometric objects (based on widely deployed
    [GEOS](https://www.osgeo.org/projects/geos/)
  - [Fiona](https://fiona.readthedocs.io): Reading and writing spatial data
    (alternative for geopandas).
  - [Pyproj](https://pyproj4.github.io/pyproj/): Performs cartographic
    transformations and geodetic computations (based on
    [PROJ.4](https://proj.org/)).
  - [Pysal](https://pysal.readthedocs.io): Library of spatial analysis
    functions written in Python.
  - [Geopy](http://geopy.readthedocs.io/): Geocoding library: coordinates to
    address \<-> address to coordinates.
  - [Contextily](https://contextily.readthedocs.io/): Add background basemaps
    for your (static) map visualizations
  - [GeoViews](https://geoviews.org/): Interactive Maps for the web.
  - [Geoplot](https://github.com/ResidentMario/geoplot): High-level geospatial
    data visualization library for Python.
  - [Dash](https://plot.ly/products/dash/): Dash is a Python framework for
    building analytical web applications.
  - [OSMnx](https://osmnx.readthedocs.io): Python for street networks.
    Retrieve, construct, analyze, and visualize street networks from
    OpenStreetMap
  - [Networkx](https://networkx.org/): Network analysis and routing in Python
    (e.g. Dijkstra and A\* -algorithms), see [this
    post](https://gis.stackexchange.com/q/65056).
  - [Cartopy](https://scitools.org.uk/cartopy/): Make drawing maps for data
    analysis and visualisation as easy as possible.
  - [Scipy.spatial](https://docs.scipy.org/doc/scipy/reference/spatial.html):
    Spatial algorithms and data structures.
  - [Rtree](https://rtree.readthedocs.io/): Spatial indexing for Python for
    quick spatial lookups.
  - [Rasterio](https://rasterio.readthedocs.io): Clean and fast and geospatial
    raster I/O for Python.
  - [RSGISLib](http://www.rsgislib.org/): Remote Sensing and GIS Software
    Library for Python.


:::{tip}

If you look through the list of links above, you will notice that many projects
host their documentation on [readthedocs.io](https://readthedocs.io/) (RTD),
more specifically at the URL `https://{PROJECT_NAME}.readthedocs.io/`. RTD has
become the de-facto standard service for hosting documentation for Python
packages; if you are looking for documentation for a Python package, quickly
trying its (assumed) readthedocs address often works.

:::


<figure id="pythongis-ecosystem" class="align-default">
    <iframe src="https://ecosystem.pythongis.org/_static/pythongis-ecosystem.html" style="width:100%; height:500px; border:none;">
    </iframe>
    <figcaption>
        <p>
            <span class="caption-text">
                In the Python ecosystem, there are tools and libraries for
                almost any GIS-related task.
                <em>Source: <a href="https://ecosystem.pythongis.org/">Tenkanen, 2022</a></em>.
            </span>
        </p>
    </figcaption>
</figure>


:::{note}
If you want to install Python and Python packages on your own computer, see the
instructions on the [course information pages](../../course-info/installing-python)
:::
