# -*- coding: utf-8 -*-
"""
L7 Introducing Osmnx for working with OpenStreetMap and routing. 

Created on Tue Dec  5 15:48:04 2017

@author: Henrikki Tenkanen
"""

# This week we will explore a new and exciting Python module called `osmnx <https://github.com/gboeing/osmnx>`__
# that can be used to retrieve, construct, analyze, and visualize street networks from OpenStreetMap. 
# It also offers a simple interface to do network routing based on walking and driving by car. 

# OpenStreetMap is a global street 

# Downloading OpenStreetMap data with osmnx
# -----------------------------------------

# One useful feature that osmnx provides is an easy-to-use way of retrieving `OpenStreetMap <http://www.openstreetmap.org/>`__ data 
# (using `OverPass API <http://wiki.openstreetmap.org/wiki/Overpass_API>`__ ). 

# Let's see how we can download and visualize street network data from a district of Kamppi in Helsinki, Finland. 
# Osmnx makes it really easy to do that as it allows you to specify an address to retrieve the OpenStreetMap data around that area. 
# In fact, osmnx uses the same Nominatim Geocoding API to achieve this which we tested during the Lesson 2. 

# - Let's retrieve OpenStreetMap (OSM) data by specifying ``"Kamppi, Helsinki, Finland"`` as the address where the data should be downloaded. 
import osmnx as ox
import matplotlib.pyplot as plt

place_name = "Kamppi, Helsinki, Finland"
kamppi_streets = ox.graph_from_place(place_name)
type(kamppi_streets)

# Okey, as we can see the data that we retrieved is a special data object called ``networkx.classes.multidigraph.MultiDiGraph``. 
# What we can see here is that this data type belongs to a Python module called `networkx <https://networkx.github.io/documentation/stable/>`__
# that can be used to create, manipulate, and study the structure, dynamics, and functions of complex networks.
# Networkx module contains algorithms that can be used to calculate `shortest paths <https://networkx.github.io/documentation/networkx-1.10/reference/algorithms.shortest_paths.html>`__ 
# along networks using e.g. `Dijkstra's <https://en.wikipedia.org/wiki/Dijkstra%27s_algorithm>`__ or `A* algorithm <https://en.wikipedia.org/wiki/A*_search_algorithm>`__. 

# - Let's see how our street network looks like. It is easy to visualize the graph with osmnx with ``plot_graph()`` function. The function utilizes Matplotlib for visualizing the data, 
# hence as a result it returns a matplotlib figure and axis objects. 
fig, ax = ox.plot_graph(kamppi_streets)

# Great! Now we can see that our graph contains the nodes (blue circles) and the edges (gray lines) that connects those nodes to each other. 

# It is also possible to retrieve other types of OSM data features with osmnx. 

# - Let's download the buildings with ``buildings_from_place()`` function and plot them on top of our street network in Kamppi. Let's also plot the Polygon that represents the area of Kamppi, 
# Helsinki that can be retrieved with ``gdf_from_place`` function.

kamppi_area = ox.gdf_from_place(place_name)
kamppi_buildings = ox.buildings_from_place(place_name)
type(kamppi_area)
type(kamppi_buildings)

# As a result we got the data as GeoDataFrames. Hence, we can plot them using the familiar ``plot()`` function of Geopandas. 

# - Let's create a map out of these three layers that we have now. 

fig, ax = plt.subplots()
kamppi_area.plot(ax=ax, facecolor='gray')
ox.plot_graph(G=kamppi_streets, ax=ax)
kamppi_buildings.plot(ax=ax, facecolor='green')