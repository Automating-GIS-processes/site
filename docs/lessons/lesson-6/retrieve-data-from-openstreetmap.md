---
jupytext:
  text_representation:
    extension: .md
    format_name: myst
    format_version: 0.13
    jupytext_version: 1.14.1
kernelspec:
  display_name: Python 3
  language: python
  name: python3
---

# Retrieving data from OpenStreetMap

## What is OpenStreetMap?

:::{figure} ../../static/images/lesson-6/osm-logo_256x256px.svg
:name: osm-logo
:alt: The logo of OpenStreetMap (OSM)

OpenStreetMap is a free and open map service, but - first and foremost - it is
a collaborative global effort to collect free and open geodata. *Source:
[wiki.openstreetmap.org](https://wiki.openstreetmap.org/wiki/Logos)*
:::

OpenStreetMap (OSM) is a global collaborative (crowd-sourced) database and
project that aims at creating a free editable map of the world containing of
information about our environment. It contains data about streets, buildings,
different services, and landuse, to mention but a few.
The collected data is also basis for the map at [openstreetmap.org](https://openstreetmap.org/). 


:::{admonition} Contribute!
:class: note

You can also sign up as a contributor if you want to add to the database and
map or correct and improve existing data. Read more in the  [OpenStreetMap
Wiki](https://wiki.openstreetmap.org/wiki/Main_Page).
:::


OSM has more than 8 million registered users who contribute around 4 million
changes daily.  Its database contains data that is described by [more than 7
billion nodes](http://wiki.openstreetmap.org/wiki/Stats) (that make up lines,
polygons and other objects).

While the most well-known side of OpenStreetMap is the map itself, that [we
have used as a background map](../lesson-5/static-maps), the project is much
more than that. OSM’s data can be used for many other purposes such as
**routing**, **geocoding**, **education**, and **research**. OSM is also widely
used for humanitarian response, e.g., in crisis areas (e.g. after natural
disasters) and for fostering economic development. Read more about humanitarian
projects that use OSM data from the [Humanitarian OpenStreetMap Team (HOTOSM)
website](https://www.hotosm.org).



## Main tools in this lesson

### OSMnx

This week we will explore a Python package called
[OSMnx](https://github.com/gboeing/osmnx) that can be used to retrieve street
networks from OpenStreetMap, and construct, analyse, and visualise them. OSMnx
can also fetch data about Points of Interest, such as restaurants, schools, and
different kinds of services.  The package also includes tools to find routes on
a network downloaded from OpenStreetMap, and implements algorithms for finding
shortest connections for walking, cycling, or driving.


To get an overview of the capabilities of the package, watch the introductory
video given by the lead developer of the package, Prof. Geoff Boeing: ["Meet
the developer: Introduction to OSMnx package by Geoff
Boeing"](https://www.youtube.com/watch?v=Q0uxu25ddc4&list=PLs9D4XVqc6dCAhhvhZB7aHGD8fCeCC_6N).

There is also a scientific article available describing the package:

> Boeing, G. 2017. ["OSMnx: New Methods for Acquiring, Constructing, Analyzing,
> and Visualizing Complex Street
> Networks."](https://www.researchgate.net/publication/309738462_OSMnx_New_Methods_for_Acquiring_Constructing_Analyzing_and_Visualizing_Complex_Street_Networks)
> Computers, Environment and Urban Systems 65, 126-139.
> doi:10.1016/j.compenvurbsys.2017.05.004

[This
tutorial](https://github.com/gboeing/osmnx-examples/blob/master/notebooks/01-overview-osmnx.ipynb)
provides a practical overview of OSMnx functionalities, and has also inspired
this AutoGIS lesson.


### NetworkX

We will also use [NetworkX](https://networkx.github.io/documentation//)
to manipulate and analyse the street network data retrieved from
OpenStreetMap. NetworkX is a Python package that can be used to create,
manipulate, and study the structure, dynamics, and functions of complex
networks. 


---


## Download and visualise OpenStreetMap data with OSMnx

A useful feature of OSMnx is its easy-to-use tools to download
[OpenStreetMap](http://www.openstreetmap.org) data via the project’s [OverPass
API](http://wiki.openstreetmap.org/wiki/Overpass_API).
In this section, we will learn how to download and visualise the street network
and additional data from OpenStreetMap covering an area of interest.


### Street network

The [`osmnx.graph`
module](https://osmnx.readthedocs.io/en/stable/osmnx.html#module-osmnx.graph)
downloads data to construct a routable road network graph, based on an
user-defined area of interest. This area of interest can be specified, for
instance, using a place name, a bounding box, or a polygon.  Here, we will use
a placename for fetching data covering the Kamppi area in Helsinki, Finland. 

In the place name query, OSMnx uses the Nominatim Geocoding API. This means
that place names should exist in the OpenStreetMap database (run a test search
at [openstreetmap.org](https://www.openstreetmap.org/) or
[nominatim.openstreetmap.org](https://nominatim.openstreetmap.org/ui/search.html)).

We will read an OSM street network using OSMnx’s
[graph_from_place()](https://osmnx.readthedocs.io/en/stable/osmnx.html#osmnx.graph.graph_from_place) function:


```{code-cell}
import osmnx

PLACE_NAME = "Kamppi, Helsinki, Finland"
graph = osmnx.graph_from_place(PLACE_NAME)
```

Check the data type of the graph:

```{code-cell} 
type(graph)
```

What we have here is a
[`networkx.MultiDiGraph`](https://networkx.org/documentation/stable/reference/classes/multidigraph.html) object.


OSMnx’s graphs do not have a built-in method to plot them, but the package
comes with a function to do so:

```{code-cell}
figure, ax = osmnx.plot_graph(graph)
```

Just as its GeoPandas and Pandas equivalents, `osmnx.plot_graph()` uses
matplotlib. The function returns a `(figure, axes)` tuple, that can be used to
modify the figure using all matplotlib functions we already got to know.

We can see that our graph contains nodes (the points) and edges (the
lines) that connects those nodes to each other.



### Convert a graph to `GeoDataFrame`s

The street network we just downloaded is a *graph*, more specifically a
`networkx.MultiDiGraph`. Its main purpose is to represent the topological
relationships between nodes and the links (edges) between them. Sometimes, it
is more convenient to have the underlying geodata in `geopandas.GeoDataFrame`s.
OSMnx comes with a convenient function that converts a graph into two geo-data
frames, one for nodes, and one for edges:
[`osmnx.graph_to_gdfs()`](https://osmnx.readthedocs.io/en/stable/osmnx.html#osmnx.utils_graph.graph_to_gdfs).


```{code-cell}
nodes, edges = osmnx.graph_to_gdfs(graph)
```

```{code-cell}
nodes.head()
```

```{code-cell}
edges.head()
```

Nice! Now, as we can see, we have our graph as GeoDataFrames and we can plot
them using the same functions and tools as we have used before.



### Place polygon

Let’s also plot the polygon that represents our area of interest (Kamppi,
Helsinki). We can retrieve the polygon geometry using the
[osmnx.geocode_to_gdf()](https://osmnx.readthedocs.io/en/stable/osmnx.html?highlight=geocode_to_gdf(#osmnx.geocoder.geocode_to_gdf)
function.

```{code-cell}
# Get place boundary related to the place name as a geodataframe
area = osmnx.geocode_to_gdf(PLACE_NAME)
```

As the name of the function already tells us, it returns a GeoDataFrame object
based on the specified place name query.  Let’s still verify the data type: 

```{code-cell}
# Check the data type
type(area)
```

Let’s also have a look at the data:

```{code-cell}
# Check data values
area
```

```{code-cell}
# Plot the area:
area.plot()
```



### Building footprints

Besides network data, OSMnx can also download any other data contained in the OpenStreetMap database. This includes, for instance, building footprints, and different points-of-interests (POIs). To download arbitrary geometries, filtered by [OSM tags](https://wiki.openstreetmap.org/wiki/Map_features) and a place name, use [`osmnx.geometries_from_place()`](https://osmnx.readthedocs.io/en/stable/osmnx.html#osmnx.geometries.geometries_from_place) [geometries is soon deprecated - Let's already use features instead]. The tag to retrieve all [buildings](https://wiki.openstreetmap.org/wiki/Buildings) is `building = yes`.


```{code-cell} 
buildings = osmnx.geometries_from_place(
    PLACE_NAME,
    {"building": True},
)
```

```{code-cell} 
len(buildings) 
```

```{code-cell} 
buildings.head() 
```

As you can see, there are several columns in `buildings`. Each column contains
information about a specific tag that OpenStreetMap contributors have added.
Each tag consists of a key (the column name), and a values (for example
`building=yes` or `building=school`). Read more about tags and tagging
practices in the [OpenStreetMap
wiki](https://wiki.openstreetmap.org/wiki/Tags). 

```{code-cell} 
buildings.columns 
```



### Points-of-interest

Point-of-interest (POI) is a generic concept that describes point locations
that represent places of interest. As `osmnx.geometries_from_place()` can download any geometry data contained in the OpenStreetMap database, it can also be used to download any kind of POI data. [geometries is soon deprecated - Let's already use features instead]


In OpenStreetMap, many POIs are described using the [`amenity`
tag](https://wiki.openstreetmap.org/wiki/Key:amenity).  We can, for example,
retrieve all restaurant locations by querying `amenity=restaurant`. 

```{code-cell}
restaurants = osmnx.geometries_from_place(
    PLACE_NAME,
    {
        "amenity": "restaurant"
    }
)
len(restaurants) 
```

As we can see, there are quite many restaurants in the area.

Let’s explore what kind of attributes we have in our restaurants GeoDataFrame:

```{code-cell}
# Available columns
restaurants.columns.values 
```

As you can see, there is quite a lot of (potential) information related to the
amenities. Let’s subset the columns and inspect the data further. Can we
extract all restaurants’ names, address, and opening hours?

```{code-cell}
# Select some useful cols and print
interesting_columns = [
    "name",
    "opening_hours",
    "addr:city",
    "addr:country",
    "addr:housenumber",
    "addr:postcode",
    "addr:street"
]

# Print only selected cols
restaurants[interesting_columns].head(10) 
```

:::{tip}
if some of the information needs an update, head over to [openstreetmap.org](https://openstreetmap.org) and edit the source data!
:::



### Parks and green areas

Let’s try to fetch all public parks in the Kamppi area. In OpenStreetMap,
[parks hould be tagged](https://wiki.openstreetmap.org/wiki/Map_features) as
`leisure = park`.  Smaller green areas (*puistikot*) are sometimes also tagged
`landuse = grass`. We can combine multiple tags in one data query.

```{code-cell}
parks = osmnx.geometries_from_place(
    PLACE_NAME,
    {
        "leisure": "park",
        "landuse": "grass",
    },
)
```

```{code-cell}
parks.head()
```

```{code-cell} 
parks.plot(color="green") 
```


### Plotting the data

Let’s create a map out of the streets, buildings, restaurants, and the area polygon.


```{code-cell} 
import matplotlib
figure, ax = matplotlib.pyplot.subplots(figsize=(12,8))

# Plot the footprint
area.plot(ax=ax, facecolor="black")

# Plot parks
parks.plot(ax=ax, facecolor="green")

# Plot street ‘edges’
edges.plot(ax=ax, linewidth=1, edgecolor="dimgray")

# Plot buildings
buildings.plot(ax=ax, facecolor="silver", alpha=0.7)

# Plot restaurants
restaurants.plot(ax=ax, color="yellow", alpha=0.7, markersize=10)
```

Cool! Now we have a map where we have plotted the restaurants, buildings,
streets and the boundaries of the selected region of ‘Kamppi’ in Helsinki. And
all of this required only a few lines of code. Pretty neat! 



:::{admonition} Check your understanding
:class: hint

Retrieve OpenStreetMap data from some other area! Download these elements using
OSMnx functions from your area of interest:
    
- Extent of the area using `geocode_to_gdf()`
- Street network using `graph_from_place()`, and convert to geo-data frame using
  `graph_to_gdfs()`
- Building footprints (and other geometries) using `geometries_from_place()`
  and appropriate tags.
    
*Note, the larger the area you choose, the longer it takes to retrieve data
from the API!*


```{code}
# Specify the name that is used to seach for the data. Check that the place
# name is valid from https://nominatim.openstreetmap.org/ui/search.html
MY_PLACE = ""
```

```{code}
# Get street network
```

```{code}
# Get building footprints
```

```{code}
# Plot the data
```
:::


## Advanced reading

To analyse OpenStreetMap data over large areas, it is often more efficient and
meaningful to download the data all at once, instead of separate queries to the
API. Such data dumps from OpenStreetMap are available in various file formats,
OSM [Protocolbuffer Binary
Format](https://wiki.openstreetmap.org/wiki/PBF_Format) (PBF) being one of
them. Data extracts covering whole countries and continents are available, for
instance, at [download.geofabrik.de](https://download.geofabrik.de/).

[Pyrosm](https://pyrosm.readthedocs.io/) is a Python package for reading
OpenStreetMap data from PBF files into `geopandas.GeoDataFrames`. Pyrosm makes
it easy to extract road networks, buildings, Points of Interest (POI), landuse,
natural elements, administrative boundaries and much more - similar to OSMnx,
but taylored to analyses of large areas.  While OSMnx reads the data from the
Overpass API, pyrosm reads the data from a local PBF file.

Read more about fetching and using pbf files as a source for analysing
OpenStreetMap data in Python from the [pyrosm
documentation](https://pyrosm.readthedocs.io/en/latest/basics.html#protobuf-file-what-is-it-and-how-to-get-one).
