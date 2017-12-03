# -*- coding: utf-8 -*-
"""
Created on Sun Dec  3 14:50:49 2017

@author: Henrikki Tenkanen
"""

import geopandas as gpd
from bokeh.plotting import save, figure
from bokeh.models import GeoJSONDataSource

addresses_fp = r'C:\HY-DATA\HENTENKA\KOODIT\Opetus\Automating-GIS-processes\2017\data\addresses.shp'
roads_fp = r'C:\HY-DATA\HENTENKA\KOODIT\Opetus\Automating-GIS-processes\2017\data\roads.shp'

# Read the data
addresses = gpd.read_file(addresses_fp)
roads = gpd.read_file(roads_fp)

# Reproject to the same projection
CRS = roads.crs
addresses = addresses.to_crs(crs=CRS)

# Convert GeoDataFrames into GeoJSONDataSource objects (similar to ColumnDataSource)
point_source = GeoJSONDataSource(geojson=addresses.to_json())
roads_source = GeoJSONDataSource(geojson=roads.to_json())

# Initialize our plot figure
p = figure(title="A test map")

# Add the lines to the map from our GeoJSONDataSource -object (it is important to specify the columns as 'xs' and 'ys')
p.multi_line('xs', 'ys', source=roads_source, color='gray', line_width=3)

# Add the lines to the map from our 'msource' ColumnDataSource -object
p.circle('x', 'y', source=point_source, color='black', size=6)

# Output filepath
outfp = r"C:\HY-DATA\HENTENKA\KOODIT\Opetus\Automating-GIS-processes\Test\Martta_Ex5\test_map.html"

# Save the map
save(p, outfp)

