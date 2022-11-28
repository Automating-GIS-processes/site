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

# Static maps

Over the course of the last weeks, we have already become familiar to plotting
basic static maps using
[`geopandas.GeoDataFrame.plot()`](http://geopandas.org/mapping.html), for
instance in lessons [2](../lesson-2/geopandas-an-introduction),
[3](../lesson-3/spatial-join), and [4](../lesson-4/reclassifying-data). We also
learnt that `geopandas.GeoDataFrame.plot()` uses the `matplotlib.pyplot`
library, and that [most of its arguments and options are accepted by
geopandas](https://matplotlib.org/stable/api/pyplot_summary.html).

To refresh our memory about the basics of plotting maps, let’s create a static
accessibility map of the Helsinki metropolitan area, that also shows roads and
metro lines (three layers, overlayed onto each other). Remember that the input
data sets need to be in the same coordinate system!


## Data

We will use three different data sets: 
- the travel time to the Helsinki railway station we used in [lesson
  4](../lesson-4/reclassifying-data), which is in `DATA_DIRECTORY /
"helsinki_region_travel_times_to_railway_station"`,
- the Helsinki Metro network, available via WFS from the city’s map services,
  and
- a simplified network of the most important roads in the metropolitan region,
  also available via WFS from the same endpoint.

```{code-cell}
import pathlib 
NOTEBOOK_PATH = pathlib.Path().resolve()
DATA_DIRECTORY = NOTEBOOK_PATH / "data"
```

```{code-cell}
import geopandas

accessibility_grid = geopandas.read_file(
    DATA_DIRECTORY
    / "helsinki_region_travel_times_to_railway_station"
    / "helsinki_region_travel_times_to_railway_station.gpkg"
)

WFS_BASE_URL = (
    "https://kartta.hel.fi/ws/geoserver/avoindata/wfs"
    "?service=wfs"
    "&version=2.0.0"
    "&request=GetFeature"
    "&srsName=EPSG:3879"
    "&typeName={layer:s}"
)

metro = (
    geopandas.read_file(
        WFS_BASE_URL.format(layer="avoindata:Seutukartta_liikenne_metro_rata")
    )
    .set_crs("EPSG:3879")
)
roads = (
    geopandas.read_file(
        WFS_BASE_URL.format(layer="avoindata:Seutukartta_liikenne_paatiet")
    )
    .set_crs("EPSG:3879")
)
```


:::{admonition} Coordinate reference systems
:class: attention

Remember that different geo-data frames need to be in same coordinate system
before plotting them in the same map. `geopandas.GeoDataFrame.plot()` does not
reproject data automatically.

You can always check it with a simple `assert` statement.
:::


```{code-cell}
:tags: ["raises-exception"]
assert accessibility_grid.crs == metro.crs == roads.crs, "Input data sets’ CRS differs"
```

If multiple data sets do not share a common CRS, first, figure out which CRS
they have assigned (if any!), then transform the data into a common reference
system:

```{code-cell}
accessibility_grid.crs
```

```{code-cell}
metro.crs
```

```{code-cell}
roads.crs
```

```{code-cell}
roads = roads.to_crs(accessibility_grid.crs)
metro = metro.to_crs(accessibility_grid.crs)
```

```{code-cell}
assert accessibility_grid.crs == metro.crs == roads.crs, "Input data sets’ CRS differs"
```


## Plotting a multi-layer map

:::{admonition} Check your understanding
:class: hint

Complete the next steps at your own pace (clear out the code cells first).
Make sure to revisit previous lessons if you feel unsure how to complete
a task. 

- Visualise a multi-layer map using the `geopandas.GeoDataFrame.plot()` method;
- first, plot the accessibility grid using a ‘quantiles’ classification scheme,
- then, add roads network and metro lines in the same plot (remember the `ax`
  parameter)
:::


Remember the following options that can be passed to `plot()`:
- style the polygon layer:
    - define a classification scheme using the `scheme` parameter
    - [change the colour map using
      `cmap`](https://matplotlib.org/stable/tutorials/colors/colormaps.html)
    - control the layer’s transparency the `alpha` parameter (`0` is fully
      transparent, `1` fully opaque)
- style the line layers:
    - adjust [the line
      colour](https://matplotlib.org/stable/api/colors_api.html) using the
      `color` parameter
    - change the `linewidth`, as needed

The layers have different extents (`roads` covers a much larger area). You can
use the axes’ (`ax`) methods `set_xlim()` and `set_ylim()` to set the horizontal
and vertical extents of the map (e.g., to a geo-data frame’s `total_bounds`).



```{code-cell}
ax = accessibility_grid.plot(
    figsize=(12, 8),
    
    column="pt_r_t",
    scheme="quantiles",
    cmap="Spectral",
    linewidth=0,
    alpha=0.8
)

metro.plot(
    ax=ax,
    color="orange",
    linewidth=2.5
)

roads.plot(
    ax=ax,
    color="grey",
    linewidth=0.8
)

minx, miny, maxx, maxy = accessibility_grid.total_bounds
ax.set_xlim(minx, maxx)
ax.set_ylim(miny, maxy)
```


## Adding a legend

To plot a legend for a map, add the `legend=True` parameter.

For figures without a classification `scheme`, the legend consists of a colour
gradient bar, the *legend title* (and other parameters) can be adjusted by
setting `legend_kwds` (see below). Find details on how to create and customise
a map legend at
[geopandas.org/mapping.html](https://geopandas.org/en/stable/docs/user_guide/mapping.html#creating-a-legend).


```{code-cell}
ax = accessibility_grid.plot(
    figsize=(12, 8),
    
    column="pt_r_t",
    cmap="Spectral",
    linewidth=0,
    alpha=0.8

    legend=True,
    legend_kwds={"label": "Travel time"})
)
```


#For figures that use a classification `scheme`, the 

% If plotting a map using a classification scheme, we get a different kind of ledend that shows the class values. In this case, we can control the position and title of the legend using matplotlib tools. We first need to access the [Legend object](https://matplotlib.org/3.3.2/api/legend_api.html#matplotlib.legend.Legend) and then change it's properties.
% 
% ```{code-cell} ipython3
% # Create one subplot. Control figure size in here.
% fig, ax = plt.subplots(figsize=(10,5))
% 
% # Visualize the travel times into 9 classes using "Quantiles" classification scheme
% grid.plot(ax=ax, 
%           column="car_r_t", 
%           linewidth=0.03, 
%           cmap="Spectral", 
%           scheme="quantiles", 
%           k=9, 
%           legend=True, 
%           )
% 
% # Re-position the legend and set a title
% ax.get_legend().set_bbox_to_anchor((1.3,1))
% ax.get_legend().set_title("Travel time (min)")
% 
% # Remove the empty white-space around the axes
% plt.tight_layout()
% ```
% 
% You can read more info about adjusting legends in the matplotlig [legend guide](https://matplotlib.org/tutorials/intermediate/legend_guide.html).
% 
% +++
% 
% ## Adding basemap from external source
% 
% It is often useful to add a basemap to your visualization that shows e.g. streets, placenames and other contextual information. This can be done easily by using ready-made background map tiles from different providers such as [OpenStreetMap](https://wiki.openstreetmap.org/wiki/Tiles) or [Stamen Design](http://maps.stamen.com). A Python library called [contextily](https://github.com/darribas/contextily) is a handy package that can be used to fetch geospatial raster files and add them to your maps. Map tiles are typically distributed in [Web Mercator projection (EPSG:3857)](http://spatialreference.org/ref/sr-org/epsg3857-wgs84-web-mercator-auxiliary-sphere/), hence **it is often necessary to reproject all the spatial data into** [Web Mercator](https://en.wikipedia.org/wiki/Web_Mercator_projection) before visualizing the data.
% 
% In this tutorial, we will see how to add a basemap underneath our previous visualization.
% 
% - Read in the travel time data:
% 
% ```{code-cell} ipython3
% import geopandas as gpd
% import matplotlib.pyplot as plt
% import contextily as ctx
% %matplotlib inline
% 
% # Filepaths
% grid_fp = "data/TravelTimes_to_5975375_RailwayStation.shp"
% 
% # Read data
% grid = gpd.read_file(grid_fp)
% grid.head(3)
% ```
% 
% Check the input crs:
% 
% ```{code-cell} ipython3
% print(grid.crs)
% ```
% 
% Reproject the layer to ESPG 3857 projection (Web Mercator):
% 
% ```{code-cell} ipython3
% # Reproject to EPSG 3857
% data = grid.to_crs(epsg=3857)
% print(data.crs)
% ```
% 
% Now the crs is `epsg:3857`. Also the coordinate values in the `geometry` column have changed:
% 
% ```{code-cell} ipython3
% data.head(2)
% ```
% 
% Next, we can plot our data using geopandas and add a basemap for our plot by using a function called `add_basemap()` from contextily:
% 
% ```{code-cell} ipython3
% # Control figure size in here
% fig, ax = plt.subplots(figsize=(12,8))
% 
% # Plot the data
% data.plot(ax=ax, column='pt_r_t', cmap='RdYlBu', linewidth=0, scheme="quantiles", k=9, alpha=0.6)
% 
% # Add basemap 
% ctx.add_basemap(ax)
% ```
% 
% As we can see, now the map has a background map that is by default using the Stamen Terrain background from [Stamen Design](http://maps.stamen.com/#terrain). 
% 
% There are also various other possible data sources and styles for background maps. 
% 
% Contextily's `tile_providers` contain a list of providers and styles that can be used to control the appearence of your background map:
% 
% ```{code-cell} ipython3
% dir(ctx.providers)
% ```
% 
% There are multiple style options for most of these providers, for example: 
% 
% ```{code-cell} ipython3
% ctx.providers.OpenStreetMap.keys()
% ```
% 
% It is possible to change the tile provider using the `source` -parameter in `add_basemap()` function. Let's see how we can change the bacground map as the basic OpenStreetMap background:
% 
% ```{code-cell} ipython3
% # Control figure size in here
% fig, ax = plt.subplots(figsize=(12,8))
% 
% # Plot the data
% data.plot(ax=ax, column='pt_r_t', cmap='RdYlBu', linewidth=0, scheme="quantiles", k=9, alpha=0.6)
% 
% # Add basemap with basic OpenStreetMap visualization
% ctx.add_basemap(ax, source=ctx.providers.OpenStreetMap.Mapnik)
% ```
% 
%  Let's take a subset of our data to see a bit better the background map characteristics:
% 
% ```{code-cell} ipython3
% # Control figure size in here
% fig, ax = plt.subplots(figsize=(12,8))
% 
% # Subset the data to seel only grid squares near the destination
% subset = data.loc[(data['pt_r_t']>=0) & (data['pt_r_t']<=15)]
% 
% # Plot the data from subset
% subset.plot(ax=ax, column='pt_r_t', cmap='RdYlBu', linewidth=0, scheme="quantiles", k=5, alpha=0.6)
% 
% # Add basemap with `OSM_A` style
% ctx.add_basemap(ax, source=ctx.providers.OpenStreetMap.Mapnik)
% ```
% 
% As we can see now our map has much more details in it as the zoom level of the background map is larger. By default `contextily` sets the zoom level automatically but it is possible to also control that manually using parameter `zoom`. The zoom level is by default specified as `auto` but you can control that by passing in [zoom level](https://wiki.openstreetmap.org/wiki/Zoom_levels) as numbers ranging typically from 1 to 19 (the larger the number, the more details your basemap will have).
% 
% - Let's reduce the level of detail from our map by passing `zoom=11`:
% 
% ```{code-cell} ipython3
% # Control figure size in here
% fig, ax = plt.subplots(figsize=(12,8))
% 
% # Plot the data from subset
% subset.plot(ax=ax, column='pt_r_t', cmap='RdYlBu', linewidth=0, scheme="quantiles", k=5, alpha=0.6)
% 
% # Add basemap with `OSM_A` style using zoom level of 11
% ctx.add_basemap(ax, zoom=11, source=ctx.providers.OpenStreetMap.Mapnik)
% ```
% 
% As we can see, the map has now less detail (a bit too blurry for such a small area).
% 
% We can also use `ax.set_xlim()` and `ax.set_ylim()` -parameters to crop our map without altering the data. The parameters takes as input the coordinates for minimum and maximum on both axis (x and y). We can also change / remove the contribution text by using parameter `attribution`
% 
% Let's add details about the data source, plot the original data, and crop the map:
% 
% ```{code-cell} ipython3
% credits = "Travel time data by Digital Geography Lab, Map Data © OpenStreetMap contributors"
% ```
% 
% ```{code-cell} ipython3
% # Control figure size in here
% fig, ax = plt.subplots(figsize=(12,8))
% 
% # Plot the data
% data.plot(ax=ax, column='pt_r_t', cmap='RdYlBu', linewidth=0, scheme="quantiles", k=9, alpha=0.6)
% 
% # Add basemap with `OSM_A` style using zoom level of 11 
% # Modify the attribution 
% ctx.add_basemap(ax, zoom=11, attribution=credits, source=ctx.providers.OpenStreetMap.Mapnik)
% 
% # Crop the figure
% ax.set_xlim(2760000, 2800000)
% ax.set_ylim(8430000, 8470000)
% ```
% 
% It is also possible to use many other map tiles from different [Tile Map Services](https://en.m.wikipedia.org/wiki/Tile_Map_Service) as the background map. A good list of different available sources can be found from [here](http://leaflet-extras.github.io/leaflet-providers/preview/). When using map tiles from different sources, it is necessary to parse a url address to the tile provider following a format defined by the provider. 
% 
% Next, we will see how to use map tiles provided by CartoDB. To do that we need to parse the url address following their [definition](https://github.com/CartoDB/basemap-styles#1-web-raster-basemaps) `'https://{s}.basemaps.cartocdn.com/{style}/{z}/{x}/{y}{scale}.png'` where:
% 
%  - {s}: one of the available subdomains, either [a,b,c,d]
%  - {z} : Zoom level. We support from 0 to 20 zoom levels in OSM tiling system.
%  - {x},{y}: Tile coordinates in OSM tiling system
%  - {scale}: OPTIONAL "@2x" for double resolution tiles
%  - {style}: Map style, possible value is one of:
%  
%     - light_all,
%     - dark_all,
%     - light_nolabels,
%     - light_only_labels,
%     - dark_nolabels,
%     - dark_only_labels,
%     - rastertiles/voyager,
%     - rastertiles/voyager_nolabels,
%     - rastertiles/voyager_only_labels,
%     - rastertiles/voyager_labels_under
%     
% - We will use this information to parse the parameters in a way that contextily wants them:
% 
% ```{code-cell} ipython3
% # Control figure size in here
% fig, ax = plt.subplots(figsize=(12,8))
% 
% # The formatting should follow: 'https://{s}.basemaps.cartocdn.com/{style}/{z}/{x}/{y}{scale}.png'
% # Specify the style to use
% style = "rastertiles/voyager"
% cartodb_url = 'https://a.basemaps.cartocdn.com/%s/{z}/{x}/{y}.png' % style
% 
% # Plot the data from subset
% subset.plot(ax=ax, column='pt_r_t', cmap='RdYlBu', linewidth=0, scheme="quantiles", k=5, alpha=0.6)
%     
% # Add basemap with `OSM_A` style using zoom level of 14 
% ctx.add_basemap(ax, zoom=14, attribution="", source=cartodb_url)
% 
% # Crop the figure
% ax.set_xlim(2770000, 2785000)
% ax.set_ylim(8435000, 8442500)
% ```
% 
% As we can see now we have yet again different kind of background map, now coming from CartoDB. 
% 
% Let's make a minor modification and change the style from `"rastertiles/voyager"` to `"dark_all"`:
% 
% ```{code-cell} ipython3
% # Control figure size in here
% fig, ax = plt.subplots(figsize=(12,8))
% 
% # The formatting should follow: 'https://{s}.basemaps.cartocdn.com/{style}/{z}/{x}/{y}{r}.png'
% # Specify the style to use
% style = "dark_all"
% cartodb_url = 'https://a.basemaps.cartocdn.com/%s/{z}/{x}/{y}.png' % style
% 
% # Plot the data from subset
% subset.plot(ax=ax, column='pt_r_t', cmap='RdYlBu', linewidth=0, scheme="quantiles", k=5, alpha=0.6)
% 
% # Add basemap with `OSM_A` style using zoom level of 14 
% ctx.add_basemap(ax, zoom=13, attribution="", source=cartodb_url)
% 
% # Crop the figure
% ax.set_xlim(2770000, 2785000)
% ax.set_ylim(8435000, 8442500)
% ```
% 
% Great! Now we have dark background map fetched from CartoDB. In a similar manner, you can use any map tiles from various other tile providers such as the ones listed in [leaflet-providers](http://leaflet-extras.github.io/leaflet-providers/preview/).
