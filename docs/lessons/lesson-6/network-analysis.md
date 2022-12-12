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



# Network analysis in Python

Finding a shortest path using a specific street network is a common GIS problem
that has many practical applications. For example, navigation, one of those
‘every-day’ applications for which **routing** algorithms are used to find the
optimal route between two or more points.

Of course, the Python ecosystem has produced packages that can be used to
conduct network analyses, such as routing. The
[NetworkX](https://networkx.github.io/documentation/) package provides various
tools to analyse networks, and implements several different routing algorithms,
such as the
[Dijkstra’s](https://networkx.org/documentation/stable/reference/algorithms/generated/networkx.algorithms.shortest_paths.generic.shortest_path.html)
or the
[A\*](https://networkx.org/documentation/stable/reference/algorithms/shortest_paths.html#module-networkx.algorithms.shortest_paths.astar)
algorithms. Both are commonly used to find shortest paths along transport networks.

To be able to conduct network analysis, it is, of course, necessary to have a
network that is used for the analyses. The
[OSMnx](https://osmnx.readthedocs.io/) package enables us to retrieve routable
networks from OpenStreetMap for various transport modes (walking, cycling and
driving). OSMnx also wraps some of NetworkX’s functionality in a convenient way
for using it on OpenStreetMap data.

In the following section, we will use OSMnx to find the shortest path between
two points based on cyclable roads. With only the tiniest modifications, we can
then repeat the analysis for the walkable street network.



## Obtain a routable network

To download OpenStreetMap data that represents the street network, we can use
it’s
[`graph_from_place()`](https://osmnx.readthedocs.io/en/stable/osmnx.html#osmnx.graph.graph_from_place)
function. As parameters, it expects a place name and, optionally, a network
type.

```{code-cell}
import osmnx

graph = osmnx.graph_from_place("Kamppi, Helsinki, Finland", network_type="bike")
```

OSMnx’s graphs do not have a built-in method to plot them, but the package
comes with a function to do so:

```{code-cell}
osmnx.plot_graph(graph)
```

:::{admonition} Pro tip!
:class: hint

Sometimes the shortest path might go slightly outside the defined area of
interest. To account for this, we can fetch the network for a bit larger area
than the district of Kamppi, in case the shortest path is not completely inside
its boundaries. 
:::

```{code-cell}
# # Get the area of interest polygon
# place_polygon = osmnx.geocode_to_gdf(place_name)
# 
# # Re-project the polygon to a local projected CRS 
# place_polygon = place_polygon.to_crs(epsg=3067)
# 
# # Buffer a bit
# place_polygon["geometry"] = place_polygon.buffer(200)
# 
# # Re-project the polygon back to WGS84, as required by osmnx
# place_polygon = place_polygon.to_crs(epsg=4326)
# 
# # Retrieve the network
# graph = osmnx.graph_from_polygon(place_polygon["geometry"].values[0], network_type='bike')
```

Plot the graph:

```{code-cell}
# fig, ax = osmnx.plot_graph(graph)
```

Okey so now we have streets for the travel mode we specified earlier. Let's
have a colser look at the attributes of the street network. Easiest way to do
this is to convert the graph (nodes and edges) into GeoDataFrames.

Converting graph into a GeoDataFrame can be done with function
`graph_to_gdfs()` that we already used in previous tutorial. With parameters
`nodes` and `edges`, it is possible to control whether to retrieve both nodes
and edges from the graph. 

```{code-cell}
# # Retrieve only edges from the graph
# edges = osmnx.graph_to_gdfs(graph, nodes=False, edges=True)
```

```{code-cell}
# # Check columns
# edges.columns
```

```{code-cell}
# # Check crs
# edges.crs
```

Note that the CRS of the GeoDataFrame is be WGS84 (epsg: 4326).

```{code-cell}
# edges.head()
```

Okey, so we have quite many columns in our GeoDataFrame. Most of the columns
are fairly self-explanatory but the following table describes all of them.
Most of the attributes come directly from the OpenStreetMap, however, columns
`u` and `v` are Networkx specific ids. You can click on the links to get more
information about each attribute:


| Column                                                     | Description                 | Data type         |
|------------------------------------------------------------|-----------------------------|-------------------|
| [bridge](http://wiki.openstreetmap.org/wiki/Key:bridge)    | Bridge feature              | boolean           |
| geometry                                                   | Geometry of the feature     | Shapely.geometry  |
| [highway](http://wiki.openstreetmap.org/wiki/Key:highway)  | Tag for roads (road type)   | str / list        |
| [lanes](http://wiki.openstreetmap.org/wiki/Key:lanes)      | Number of lanes             | int (or nan)      |
| [lenght](http://wiki.openstreetmap.org/wiki/Key:length)    | Length of feature (meters)  | float             |
| [maxspeed](http://wiki.openstreetmap.org/wiki/Key:maxspeed)| maximum legal speed limit   | int /list         |
| [name](http://wiki.openstreetmap.org/wiki/Key:name)        | Name of the (street) element| str (or nan)      |
| [oneway](http://wiki.openstreetmap.org/wiki/Key:oneway)    | One way road                | boolean           |
| [osmid](http://wiki.openstreetmap.org/wiki/Node)           | Unique ids for the element  | list              |
| [u](http://ow.ly/bV8n30h7Ufm)                              | The first node of edge      | int               |
| [v](http://ow.ly/bV8n30h7Ufm)                              | The last node of edge       | int               |



Let's take a look what kind of features we have in the `highway` column:

```{code-cell}
# edges['highway'].value_counts()
```

I now we can confirm that as a result our street network indeed only contains
such streets where it is allowed to drive with a car as there are no e.g.
cycleways or footways included in the data.

As the data is in WGS84 format, we might want to reproject our data into a
metric system before proceeding to the shortest path analysis.  We can
re-project the graph from latitudes and longitudes to an appropriate UTM zone
using the
[project_graph()](https://osmnx.readthedocs.io/en/stable/osmnx.html#osmnx.projection.project_graph)
function from OSMnx. 

```{code-cell}
# # Project the data
# graph_proj = osmnx.project_graph(graph) 
```

```{code-cell}
# # Get Edges and Nodes
# nodes_proj, edges_proj = osmnx.graph_to_gdfs(graph_proj, nodes=True, edges=True)
```

```{code-cell}
# print("Coordinate system:", edges_proj.crs)
```

```{code-cell}
# edges_proj.head()
```

Okey, as we can see from the CRS the data is now in [UTM
projection](https://en.wikipedia.org/wiki/Universal_Transverse_Mercator_coordinate_system)
using zone 35 which is the one used for Finland, and indeed the orientation of
the map and the geometry values also confirm this.



Furthermore, we can check the epsg code of this projection using pyproj CRS:

```{code-cell}
# edges_proj.crs.to_epsg()
```

Indeed, the projection is now [WGS 84 / UTM zone 35N, EPSG:32635](https://epsg.io/32635).



## Analyzing the network properties

Now as we have seen some of the basic functionalities of OSMnx such as
downloading the data and converting data from graph to GeoDataFrame, we can
take a look some of the analytical features of omsnx. Osmnx includes many
useful functionalities to extract information about the network.

To calculate some of the basic street network measures we can use
[basic_stats()](https://osmnx.readthedocs.io/en/stable/osmnx.html#osmnx.stats.basic_stats)
function in OSMnx:

```{code-cell}
# # Calculate network statistics
# stats = osmnx.basic_stats(graph_proj)
# stats
```

To be able to extract the more advanced statistics (and some of the missing
ones above) from the street network, it is required to have information about
the coverage area of the network. Let's calculate the area of the [convex
hull](https://en.wikipedia.org/wiki/Convex_hull) of the street network and see
what we can get.


```{code-cell}
# # Get the Convex Hull of the network
# convex_hull = edges_proj.unary_union.convex_hull
# 
# # Show output
# convex_hull
```

Now we can use the Convex Hull above to calculate [extended statistics for the
network](https://osmnx.readthedocs.io/en/stable/osmnx.html#osmnx.stats.extended_stats).
As some of the metrics are produced separately for each node, they produce a
lot of output. Here, we combine the basic and extended statistics into one
pandas Series to keep things in more compact form.

```{code-cell}
# # Calculate the area
# area = convex_hull.area
# 
# # Calculate statistics with density information
# stats = osmnx.basic_stats(graph_proj, area=area)
# extended_stats = osmnx.extended_stats(graph_proj, ecc=True, cc=True)
#
# # Add extened statistics to the basic statistics
# for key, value in extended_stats.items():
#     stats[key] = value
#     
# # Convert the dictionary to a Pandas series for a nicer output
# pd.Series(stats)
```

As we can see, now we have a **LOT** of information about our street network
that can be used to understand its structure. We can for example see that the
average node density in our network is `149 nodes/km` and that the total edge
length of our network is almost 20 kilometers.

Furthermore, we can see that the [degree
centrality](https://en.wikipedia.org/wiki/Centrality) of our network is on
average `0.0326515`. Degree is a simple centrality measure that counts how many
neighbors a node has (here a fraction of nodes it is connected to). Another
interesting measure is the [PageRank](https://en.wikipedia.org/wiki/PageRank)
that measures the importance of specific node in the graph. Here we can see
that the most important node in our graph seem to a node with osmid `25416262`.
PageRank was the algorithm that Google first developed (Larry Page & Sergei
Brin) to order the search engine results and became famous for.

You can read the [Wikipedia article about different centrality
measures](https://en.wikipedia.org/wiki/Centrality) if you are interested what
the other centrality measures mean.



## Shortest path analysis

Let's now calculate the shortest path between two points using the [shortest
path function in
Networkx](https://networkx.github.io/documentation/networkx-1.10/reference/generated/networkx.algorithms.shortest_paths.generic.shortest_path.html#shortest-path). 



### Origin and destination points 

First we need to specify the source and target locations for our route. If you
are familiar with the Kamppi area, you can specify a custom placename as a
source location. Or, you can follow along and choose these points as the origin
and destination in the analysis:
- [Maria 01](https://nominatim.openstreetmap.org/ui/search.html?q=Maria+01) -
  and old hospital area and current startup hub.
- [ruttopuisto](https://nominatim.openstreetmap.org/ui/search.html?q=ruttopuisto),
  a park. Official name of this park is "Vanha kirkkopuisto", but nominatim
  is also able to geocode the nickname.

We could figure out the coordinates for these locations manually, and create
shapely points based on the coordinates.  However,  it is more handy to fetch
the location of our source destination directly from OSM:

```{code-cell}
# # Set place name
# placename = "Maria 01, Helsinki"
```

```{code-cell}
# # Geocode the place name
# geocoded_place = osmnx.geocode_to_gdf(placename)
```

```{code-cell}
# # Check the result
# geocoded_place
```

As output, we received the building footprint. From here, we can get the
centroid as the source location of our shortest path analysis. However, we
first need to project the data into the correct crs:

```{code-cell}
# # Re-project into the same CRS as the road network
# geocoded_place = geocoded_place.to_crs(edges_proj.crs)
```

```{code-cell}
# # Get centroid as shapely point
# origin = geocoded_place["geometry"].centroid.values[0]
```

```{code-cell}
# print(origin)
```

Great! Now we have defined the origin point for our network analysis. We can
repeat the same steps to retrieve central point of *ruttopuisto*-park as the
destination: 

```{code-cell}
# # Set place name
# placename = "ruttopuisto"
# 
# # Geocode the place name
# geocoded_place = osmnx.geocode_to_gdf(placename)
# 
# # Re-project into the same CRS as the road network
# geocoded_place = geocoded_place.to_crs(edges_proj.crs)
# 
# # Get centroid of the polygon as shapely point
# destination = geocoded_place["geometry"].centroid.values[0]
# 
# print(destination)
```

Now we have shapely points representing the origin and destination locations
for our network analysis. Next step is to find these points on the routable
network before the final routing.



### Nearest node

Let's now find the nearest graph nodes (and their node IDs) to these points
using OSMnx
[get_nearest_node](https://osmnx.readthedocs.io/en/stable/osmnx.html#osmnx.utils.get_nearest_node).
As a starting point, we have the two Shapely Point objects we just defined as
the origin and destination locations. 

According to the documentation of this function, we need to parse Point
coordinates as coordinate-tuples in this order: `latitude, longitude`(or `y,
x`). As our data is now projected to UTM projection, we need to specify with
`method` parameter that the function uses `'euclidean'` distances to calculate
the distance from the point to the closest node (with decimal derees, use
`'haversine'`, which determines the great-circle distances). The method
parameter is important if you want to know the actual distance between the
Point and the closest node which you can retrieve by specifying parameter
`return_dist=True`.

```{code-cell}
# # Get origin x and y coordinates
# orig_xy = (origin.y, origin.x)
# 
# # Get target x and y coordinates
# target_xy = (destination.y, destination.x)
```

```{code-cell}
# # Find the node in the graph that is closest to the origin point (here, we want to get the node id)
# orig_node_id = osmnx.get_nearest_node(graph_proj, orig_xy, method='euclidean')
# orig_node_id
```

```{code-cell}
# # Find the node in the graph that is closest to the target point (here, we want to get the node id)
# target_node_id = osmnx.get_nearest_node(graph_proj, target_xy, method='euclidean')
# target_node_id
```

Now we have the IDs for the closest nodes that were found from the graph to the
origin and target points that we specified. 

Let's retrieve the node information from the `nodes_proj` GeoDataFrame by
passing the ids to the `loc` indexer

```{code-cell}
# # Retrieve the rows from the nodes GeoDataFrame based on the node id (node id is the index label)
# orig_node = nodes_proj.loc[orig_node_id]
# target_node = nodes_proj.loc[target_node_id]
```

Let's also create a GeoDataFrame that contains these points

```{code-cell}
# # Create a GeoDataFrame from the origin and target points
# od_nodes = geopandas.GeoDataFrame([orig_node, target_node], geometry='geometry', crs=nodes_proj.crs)
# od_nodes.head()
```

Okay, as a result we got now the closest node IDs of our origin and target locations. As you can see, the `index` in this GeoDataFrame corresponds to the IDs that we found with `get_nearest_node()` function.



### Routing

Now we are ready to do the routing and find the shortest path between the
origin and target locations by using the `shortest_path()`
[function](https://networkx.github.io/documentation/networkx-1.10/reference/generated/networkx.algorithms.shortest_paths.generic.shortest_path.html)
of networkx.  With `weight` -parameter we can specify that `'length'` attribute
should be used as the cost impedance in the routing. If specifying the weight
parameter, NetworkX will use by default Dijkstra's algorithm to find the
optimal route. We need to specify the graph that is used for routing, and the
origin `ID` (*source*) and the target `ID` in between the shortest path will be
calculated:

```{code-cell}
# # Calculate the shortest path
# route = networkx.shortest_path(G=graph_proj, source=orig_node_id, target=target_node_id, weight='length')
# 
# # Show what we have
# print(route)
```

As a result we get a list of all the nodes that are along the shortest path. 

- We could extract the locations of those nodes from the `nodes_proj`
  GeoDataFrame and create a LineString presentation of the points, but luckily,
  OSMnx can do that for us and we can plot shortest path by using
  `plot_graph_route()` function:

```{code-cell}
# # Plot the shortest path
# fig, ax = osmnx.plot_graph_route(graph_proj, route)
```

Nice! Now we have the shortest path between our origin and target locations.
Being able to analyze shortest paths between locations can be valuable
information for many applications.  Here, we only analyzed the shortest paths
based on distance but quite often it is more useful to find the optimal routes
between locations based on the travelled time. Here, for example we could
calculate the time that it takes to cross each road segment by dividing the
length of the road segment with the speed limit and calculate the optimal
routes by taking into account the speed limits as well that might alter the
result especially on longer trips than here.



## Saving shortest paths to disk

Quite often you need to save the route into a file for further analysis and
visualization purposes, or at least have it as a GeoDataFrame object in Python.
Hence, let's continue still a bit and see how we can turn the route into a
linestring and save the shortest path geometry and related attributes into a
geopackage file.

- First we need to get the nodes that belong to the shortest path:

```{code-cell}
# # Get the nodes along the shortest path
# route_nodes = nodes_proj.loc[route]
# route_nodes
```

As we can see, now we have all the nodes that were part of the shortest path as a GeoDataFrame.

- Now we can create a LineString out of the Point geometries of the nodes:

```{code-cell}
# from shapely.geometry import LineString, Point
# 
# # Create a geometry for the shortest path
# route_line = LineString(list(route_nodes.geometry.values))
# route_line
```

Now we have the route as a LineString geometry. 

- Let's make a GeoDataFrame out of it having some useful information about our
  route such as a list of the osmids that are part of the route and the length
  of the route.

```{code-cell}
# # Create a GeoDataFrame
# route_geom = geopandas.GeoDataFrame([[route_line]], geometry='geometry', crs=edges_proj.crs, columns=['geometry'])
# 
# # Add a list of osmids associated with the route
# route_geom.loc[0, 'osmids'] = str(list(route_nodes['osmid'].values))
# 
# # Calculate the route length
# route_geom['length_m'] = route_geom.length
# 
# route_geom.head()
```

Now we have a GeoDataFrame that we can save to disk. Let's still confirm that
everything is ok by plotting our route on top of our street network and some
buildings, and plot also the origin and target points on top of our map.

- Get buildings:

```{code-cell}
# tags = {'building': True}
# buildings = osmnx.geometries_from_place(place_name, tags)
```

re-project buildings

```{code-cell}
# buildings_proj = buildings.to_crs(edges_proj.crs)
```

- Let's now plot the route and the street network elements to verify that
  everything is as it should:

```{code-cell}
# fig, ax = plt.subplots(figsize=(12,8))
# 
# # Plot edges and nodes
# edges_proj.plot(ax=ax, linewidth=0.75, color='gray')
# nodes_proj.plot(ax=ax, markersize=2, color='gray')
# 
# # Add buildings
# ax = buildings_proj.plot(ax=ax, facecolor='lightgray', alpha=0.7)
# 
# # Add the route
# ax = route_geom.plot(ax=ax, linewidth=2, linestyle='--', color='red')
# 
# # Add the origin and destination nodes of the route
# ax = od_nodes.plot(ax=ax, markersize=30, color='red')
# 
# # Add basemap
# ctx.add_basemap(ax, crs=buildings_proj.crs, source=ctx.providers.CartoDB.Positron)
```

Great everything seems to be in order! As you can see, now we have a full
control of all the elements of our map and we can use all the aesthetic
properties that matplotlib provides to modify how our map will look like. Now
we are almost ready to save our data into disk.



## Prepare data for saving to file

The data contain certain data types (such as `list` or `boolean`) that should
be converted into character strings prior to saving the data to file.Another
option would be to drop invalid columns.

```{code-cell}
# edges_proj.head()
```

```{code-cell}
# # Check if columns contain any list values
# (edges_proj.applymap(type) == list).any()
```

```{code-cell}
# # Columns with invalid values
# invalid_cols = ['lanes', 'maxspeed', 'name', 'oneway', 'osmid', "highway", "service"]
# 
# #  convert selected columns to string format
# edges_proj[invalid_cols] = edges_proj[invalid_cols].astype(str)
```

```{code-cell}
# # Check again if columns contain any list values
# (edges_proj.applymap(type) == list).any()
```

Now we can see that most of the attributes are of type `object` that quite
often (such as ours here) refers to a string type of data.

## Save the data:

```{code-cell}
# import os
# 
# # Parse the place name for the output file names (replace spaces with underscores and remove commas)
# place_name_out = place_name.replace(' ', '_').replace(',','')
# 
# # Output directory
# out_dir = "data"
# 
# # Create output fp for a geopackage
# out_fp = os.path.join(out_dir, f"OSM_{place_name_out}.gpkg")
# 
# # Save files
# edges_proj.to_file(out_fp, layer="streets", driver="GPKG")
# route_geom.to_file(out_fp, layer="route", driver="GPKG")
# nodes_proj.to_file(out_fp, layer="nodes", driver="GPKG")
# od_nodes.to_file(out_fp, layer="route_OD", driver="GPKG")
# buildings[['geometry', 'name', 'addr:street']].to_file(out_fp, layer="buildings", driver="GPKG")
```

Great, now we have saved all the data that was used to produce the maps into a geopackage.



## Advanced reading

Here we learned how to solve a simple routing task between origin and
destination points. What about if we have hundreads or thousands of origins?
This is the case if you want to explore the travel distances to a spesific
location across the whole city, for example, when analyzing the accessibility
of jobs and services (like in the Travel Time Matrix dataset used in previous
sections). 

Check out pyrosm documentation on [working with
graphs](https://pyrosm.readthedocs.io/en/latest/graphs.html#working-with-graphs)
for more advanced examples of network analysis in python. For example,
[pandana](https://udst.github.io/pandana/) is a fast and efficient python
library for creating aggretated network analysis in no time across large
networks, and pyrosm can be used for preparing the input data for such
analysis.
