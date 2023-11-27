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

# Interactive maps

[Online
maps](https://link.springer.com/referenceworkentry/10.1007/978-3-319-23519-6_1485-2)
have been interactive for a long time: virtually all online maps allow to zoom
in and out, to pan the map extent, and to select map features, or otherwise
query information about them.

Interactive content in web pages, such as online maps, are typically
implemented using
[*JavaScript*/*ECMAScript*](https://en.wikipedia.org/wiki/ECMAScript), a scripting
language originally targeted at web pages, primarily, but used for many other
applications.

In the open source realm, there exist a number of different *JavaScript*
libraries for interactive web cartography, including
[Leaflet](https://leafletjs.com/), which we will use in this lesson, and
[OpenLayers](https://openlayers.org/).

No worries, we will not have to write a single line of *JavaScript*; this is a
*Python* course, after all. Rather, we will take advantage of the
[*Folium*](https://python-visualization.github.io/folium/) Python package: it
helps create interactive *Leaflet* maps from data stored in
`geopandas.GeoDataFrame`s.


:::{admonition} *Folium* resources
:class: note

Find more information about the capabilities of the *Folium* package on its
official web pages:
- [Documentation](https://python-visualization.github.io/folium/)
- [Example gallery](https://nbviewer.org/github/python-visualization/folium/tree/main/examples/)
- [Quickstart tutorial](https://python-visualization.github.io/folium/quickstart.html#Getting-Started)
:::


## Create a simple interactive web map

We will start by creating a simple interactive web map that contains nothing
but a base map. This is so we get acustomed to how *Folium*’s syntax works, and
which steps we have to take.

We create a `folium.Map` object, and specify centred around which `location`
and at which initial zoom level (~0-20) a map shall be displayed. By setting
`control_scale` to `True`, we make *Folium* display a scale bar.


```{code-cell}
import pathlib
NOTEBOOK_PATH = pathlib.Path().resolve()
DATA_DIRECTORY = NOTEBOOK_PATH / "data"

# We will export HTML pages during this lesson,
# let’s also prepare an output directory for them:
HTML_DIRECTORY = NOTEBOOK_PATH / "html"
HTML_DIRECTORY.mkdir(exist_ok=True)
```


```{code-cell}
import folium

interactive_map = folium.Map(
    location=(60.2, 24.8),
    zoom_start=10,
    control_scale=True
)

interactive_map
```


### Save the resulting map

To save this map to an HTML file that can be opened in any web browser,
use [`folium.Map.save()`](https://python-visualization.github.io/branca/element.html#branca.element.Element.save):

```{code-cell}
interactive_map.save(HTML_DIRECTORY / "base-map.html")
```


### Change the base map

If you want to use a different base layer than the default OpenStreetMap,
`folium.Map` accepts a parameter `tiles`, that can either reference [one of the
built-in map providers](https://python-visualization.github.io/folium/modules.html#folium.folium.Map).

While we’re at it, let’s also vary the centre location and the zoom level
of the map:

```{code-cell}
interactive_map = folium.Map(
    location=(60.2, 25.00),
    zoom_start=12,
    tiles="cartodbpositron"
)
interactive_map
```

Or we can point to a custom *tileset URL*:

```{code-cell}
interactive_map = folium.Map(
    location=(60.2, 25.00),
    zoom_start=12,
    tiles="https://mt1.google.com/vt/lyrs=r&x={x}&y={y}&z={z}",
    attr="Google maps",
)
interactive_map
```

## Add a point marker

To add a single marker to a *Folium* map, create a
[`folium.Marker`](https://python-visualization.github.io/folium/modules.html#folium.map.Marker).
Supply a
[`folium.Icon`](https://python-visualization.github.io/folium/modules.html#folium.map.Icon)
as a parameter `icon` to influence how the marker is styled, and set `tooltip`
to display a text when the mouse pointer hovers over it.

```{code-cell}
interactive_map = folium.Map(
    location=(60.2, 25.0),
    zoom_start=12
)

kumpula = folium.Marker(
    location=(60.204, 24.962),
    tooltip="Kumpula Campus",
    icon=folium.Icon(color="green", icon="ok-sign")
)
kumpula.add_to(interactive_map)

interactive_map
```


## Add a layer of points

*Folium* also supports to add entire layers, for instance, as
`geopandas.GeoDataFrames`. *Folium* implements [*Leaflet*’s `geoJSON`
layers](https://leafletjs.com/reference.html#geojson) in its
`folium.features.GeoJson` class. We can initialise such a class (and layer)
with a geo-data frame, and add it to a map. In the example below, we use the
`addresses.gpkg` data set we create [in lesson
3](../lesson-3/geocoding-in-geopandas).

```{code-cell}
import geopandas

addresses = geopandas.read_file(DATA_DIRECTORY / "addresses.gpkg")
addresses.head()
```

```{code-cell}
interactive_map = folium.Map(
    location=(60.2, 25.0),
    zoom_start=12
)

addresses_layer = folium.features.GeoJson(
    addresses,
    name="Public transport stops"
)
addresses_layer.add_to(interactive_map)

interactive_map
```

We can also add a pop-up window to our map which would show the addresses at the point of interest upon clicking:

```{code-cell}
interactive_map = folium.Map(
    location=(60.2, 25.0),
    zoom_start=12
)

popup = folium.GeoJsonPopup(
    fields=["address"],
    aliases=["Address"],
    localize=True,
    labels=True,
    style="background-color: yellow;",
)

addresses_layer = folium.features.GeoJson(
    addresses,
    name="Public transport stops",
    popup=popup
)
addresses_layer.add_to(interactive_map)

interactive_map
```
## Add a polygon layer

In the following section we are going to revisit another data set with which we have worked before: the Helsinki Region population grid we got to know in [lesson 2](../lesson-2/vector-data-io), and which you used during [exercise 3](../lesson-3/exercise-3). We can load the layer directly from [HSY’s open data WFS endpoint](https://hri.fi/):

```{code-cell}
# To ignore the SSL certificate issue
import ssl
ssl._create_default_https_context = ssl._create_unverified_context
population_grid = (
    geopandas.read_file(
        "https://kartta.hsy.fi/geoserver/wfs"
        "?service=wfs"
        "&version=2.0.0"
        "&request=GetFeature"
        "&typeName=asuminen_ja_maankaytto:Vaestotietoruudukko_2020"
        "&srsName=EPSG:4326"
        "&bbox=24.6,60.1,25.2,60.4,EPSG:4326"
    )
    .set_crs("EPSG:4326")
)
population_grid.head()
```

Let’s first clean the data frame: drop all columns we don’t need, and
rename the remaining ones to English.

```{code-cell}
population_grid = population_grid[["index", "asukkaita", "geometry"]]
population_grid = population_grid.rename(columns={
    "asukkaita": "population"
})
```


:::{admonition} Index column for choropleth maps
:class: hint

We will use the `folium.Choropleth` to display the population grid. Choropleth
maps are more than simply polygon geometries, which could be displayed as a
`folium.features.GeoJson` layer, just like we used for the address points,
above. Rather, the class takes care of categorising data, adding a legend, and
a few more small tasks to quickly create beautiful thematic maps.

The class expects an input data set that has an explicit, `str`-type, index
column, as it treats the geospatial input and the thematic input as separate
data sets that need to be joined (see also, below, how we specify both
`geo_data` and `data`).

A good approach to create such a column is to copy the data frame’s index
into a new column, for instance `id`.
:::


```{code-cell}
population_grid["id"] = population_grid.index.astype(str)
```

Now we can create the polygon choropleth layer, and add it to a map object.
Due to the slightly complex architecture of *Folium*, we have to supply a
number of parameters:
- `geo_data` and `data`, the geospatial and thematic input data sets,
  respectively. Can be the same `geopandas.GeoDataFrame`.
- `columns`: a tuple of the names of relevant columns in `data`: a unique
  index column, and the column containing thematic data
- `key_on`: which column in `geo_data` to use for joining `data` (this is
  basically identical to `columns`, except it’s only the first value)

```{code-cell}
interactive_map = folium.Map(
    location=(60.17, 24.94),
    zoom_start=12
)

population_grid_layer = folium.Choropleth(
    geo_data=population_grid,
    data=population_grid,
    columns=("id", "population"),
    key_on="feature.id"
)
population_grid_layer.add_to(interactive_map)

interactive_map
```


To make the map slightly nicer, let’s still request more categories (`bins`),
change the colour range (using `fill_color`), set the line thickness to zero,
and add a layer name to the legend:


```{code-cell}
interactive_map = folium.Map(
    location=(60.17, 24.94),
    zoom_start=12
)

population_grid_layer = folium.Choropleth(
    geo_data=population_grid,
    data=population_grid,
    columns=("id", "population"),
    key_on="feature.id",

    bins=9,
    fill_color="YlOrRd",
    line_weight=0,
    legend_name="Population, 2020",

    highlight=True
)
population_grid_layer.add_to(interactive_map)

interactive_map
```


### Add a tooltip to a choropleth map

In such an interactive map, it would be nice to display the value of each
grid cell polygon when hovering the mouse over it. *Folium* does not support
this out-of-the-box, but with a simple trick, we can extend its functionality:
We add a transparent polygon layer using a ‘basic‘ `folium.features.GeoJson`,
and configure it to display tooltips.

We can keep the `map` we created above, and simply add another layer to it.

```{code-cell}
# folium GeoJson layers expect a styling function,
# that receives each of the map’s feature and returns
# an individual style. It can, however, also return a
# static style:
def style_function(feature):
    return {
        "color": "transparent",
        "fillColor": "transparent"
    }


# More complex tooltips can be created using the
# `folium.features.GeoJsonTooltip` class. Below, we use
# its most basic features: `fields` specifies which columns
# should be displayed, `aliases` how they should be labelled.
tooltip = folium.features.GeoJsonTooltip(
    fields=("population",),
    aliases=("Population:",)
)


tooltip_layer = folium.features.GeoJson(
    population_grid,
    style_function=style_function,
    tooltip=tooltip
)
tooltip_layer.add_to(interactive_map)

interactive_map
```


:::{admonition} Python packages for interactive (web) maps
:class: note

*Folium* is just one of many packages that provide an easy way to create interactive maps using data stored in (geo-)pandas data frames. Other interesting libraries include:

- [GeoViews](https://geoviews.org/),
- [Mapbox GL for Jupyter](https://github.com/mapbox/mapboxgl-jupyter),
- [Bokeh](https://docs.bokeh.org/en/latest/docs/gallery.html),
- [Plotly Express](https://plotly.com/python/maps/), and many more.
:::
