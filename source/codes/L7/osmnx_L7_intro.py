# -*- coding: utf-8 -*-
"""
L7 Introducing Osmnx for working with OpenStreetMap and routing. 

Created on Tue Dec  5 15:48:04 2017

@author: Henrikki Tenkanen
"""

# Working with OpenStreetMap data
# ===============================

# OpenStreetMap is a global crowdsourced dataset that contains a lot of information about the our built environment. It contains data about streets, buildings, and services to mention a few. 

# This week we will explore a new and exciting Python module called `osmnx <https://github.com/gboeing/osmnx>`__
# that can be used to retrieve, construct, analyze, and visualize street networks from OpenStreetMap. 
# It also offers a simple interface to do network routing based on walking and driving by car. 

# Download and visualize OpenStreetMap data with osmnx
# ----------------------------------------------------

# One useful feature that osmnx provides is an easy-to-use way of retrieving `OpenStreetMap <http://www.openstreetmap.org/>`__ data 
# (using `OverPass API <http://wiki.openstreetmap.org/wiki/Overpass_API>`__ ). 

# Let's see how we can download and visualize street network data from a district of Kamppi in Helsinki, Finland. 
# Osmnx makes it really easy to do that as it allows you to specify an address to retrieve the OpenStreetMap data around that area. 
# In fact, osmnx uses the same Nominatim Geocoding API to achieve this which we tested during the Lesson 2. 

# - Let's retrieve OpenStreetMap (OSM) data by specifying ``"Kamppi, Helsinki, Finland"`` as the address where the data should be downloaded. 
import osmnx as ox
import matplotlib.pyplot as plt

place_name = "Kamppi, Helsinki, Finland"
graph = ox.graph_from_place(place_name)
type(graph)

# Okey, as we can see the data that we retrieved is a special data object called ``networkx.classes.multidigraph.MultiDiGraph``. 
# What we can see here is that this data type belongs to a Python module called `networkx <https://networkx.github.io/documentation/stable/>`__
# that can be used to create, manipulate, and study the structure, dynamics, and functions of complex networks.
# Networkx module contains algorithms that can be used to calculate `shortest paths <https://networkx.github.io/documentation/networkx-1.10/reference/algorithms.shortest_paths.html>`__ 
# along networks using e.g. `Dijkstra's <https://en.wikipedia.org/wiki/Dijkstra%27s_algorithm>`__ or `A* algorithm <https://en.wikipedia.org/wiki/A*_search_algorithm>`__. 

# - Let's see how our street network looks like. It is easy to visualize the graph with osmnx with ``plot_graph()`` function. The function utilizes Matplotlib for visualizing the data, 
# hence as a result it returns a matplotlib figure and axis objects. 
fig, ax = ox.plot_graph(graph)

# Great! Now we can see that our graph contains the nodes (blue circles) and the edges (gray lines) that connects those nodes to each other. 

# It is also possible to retrieve other types of OSM data features with osmnx. 

# - Let's download the buildings with ``buildings_from_place()`` function and plot them on top of our street network in Kamppi. Let's also plot the Polygon that represents the area of Kamppi, 
# Helsinki that can be retrieved with ``gdf_from_place`` function.

area = ox.gdf_from_place(place_name)
buildings = ox.buildings_from_place(place_name)
type(area)
type(buildings)

# As a result we got the data as GeoDataFrames. Hence, we can plot them using the familiar ``plot()`` function of Geopandas. 
# As you might remember the street network data was not in GeoDataFrame. Luckily, osmnx provides a convenient function ``graph_to_gdfs()`` 
# that can convert the graph into two separate GeoDataFrames where the first one contains the information about the nodes and the second one 
# about the edges. 

# - Let's extract the nodes and edges from the graph as GeoDataFrames.
nodes, edges = ox.graph_to_gdfs(graph)
nodes.head()
edges.head()
type(edges)
                                                            
# Nice! Now, as we can see, we have our graph as GeoDataFrames and we can plot them using the same functions and tools as we have used before. 
# - Let's create a map out of the streets, buildings, and the area Polygon but let's exclude the nodes (to keep the figure clearer).

fig, ax = plt.subplots()
area.plot(ax=ax, facecolor='black')
edges.plot(ax=ax, linewidth=1, edgecolor='white')
buildings.plot(ax=ax, facecolor='khaki')

# Cool! Now we have a nice map where we have plotted the buildings, streets and the boundaries of the selected region of 'Kamppi' in Helsinki. Pretty easy, isn't it. 

# .. todo::
#
#    **Task**: Column ``highway`` in our ``edges`` GeoDataFrame contains information about the type of the street (such as ``primacy, cycleway or footway``). 
#      Select the streets that are walkable or that can be used with cycle and visualize only them with the buildings and the area polygon. Use different colors and line widths for the cycleways and footways.


# .. hint::
#
#     There are a few nice and convenient high-level functions in osmnx that can be used to produce nice maps directly just by using a single function that might be useful. 
#     If you are interested take a look of `this tutorial <https://github.com/gboeing/osmnx-examples/blob/master/notebooks/10-building-footprints.ipynb>`__. 
#     In the lesson we won't cover these, because we wanted to keep as much control to ourselves as possible, hence using lower-level functions. 




