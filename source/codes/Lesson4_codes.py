# -*- coding: utf-8 -*-
"""
Created on Thu Nov 17 09:08:58 2016

@author: hentenka
"""
import matplotlib
matplotlib.use('GTKAgg') 
import matplotlib.pyplot as plt

import gdal
import geopandas as gpd
from geopandas.tools import overlay
from fiona.crs import from_epsg

# Download datasets
# -----------------

# Download (and then extract) the data from this link:

# Overlay analysis
# ----------------

# The aim here is to make an overlay analysis where we select only specific polygon cells from the data
# based on the borders of municipality of Helsinki.

# File paths
border_fp = r"D:\KOODIT\Opetus\Automating-GIS-processes\AutoGIS-Sphinx\data\Helsinki_borders.shp"
grid_fp = r"D:\KOODIT\Opetus\Automating-GIS-processes\AutoGIS-Sphinx\data\TravelTimes_to_5975375_RailwayStation.shp"

# Read files
grid = gpd.read_file(grid_fp)
hel = gpd.read_file(border_fp)


# Let's check that the coordinate systems match
hel.crs
grid.crs

# They do 
# Let's see how our datasets look like, let's use the Helsinki municipality layer as our basemap and 
# plot the other layer on top of that
basemap = hel.plot()
grid[-3000:].plot(ax=basemap)

# Let's do an overlay analysis and select polygons from grid that intersect with our Helsinki layer
result = gpd.overlay(grid, hel, how='intersection')

# Let's plot our data and see what we have
result.plot(color="b")

# Cool! Now as a result we have only those grid cells included that intersect with the Helsinki borders 
# and the grid cells are clipped based on the boundary

# Whatabout the data attributes? Let's see what we have
result.head()

# Nice! Now we have attributes from both layers included.
# Let's see the length of the GeoDataFrame
len(result)

# And the original data
len(grid)    

# Fill empty geometries
result['geometry'] = result['geometry'].fillna()

# Let's save our result grid as a Json file that is another commonly used file 
# format nowadays for storing spatial data
resultfp = r"D:\KOODIT\Opetus\Automating-GIS-processes\AutoGIS-Sphinx\data\TravelTimes_to_5975375_RailwayStation_Helsinki.geojson"
result.to_file(resultfp, driver="GeoJSON")

# Data preparation
# ----------------

# File path
fp = r"C:\HY-Data\HENTENKA\KOODIT\Opetus\Automating-GIS-processes\AutoGIS-Sphinx\data\Corine2012_Uusimaa.shp"
data = gpd.read_file(fp)

# Drop Finnish columns
selected_cols = ['Level1', 'Level1Eng', 'Level2', 'Level2Eng',
       'Level3', 'Level3Eng', 'Luokka3', 'geometry']

# Select data
data = data[selected_cols]

# Check coordinate system information
data.crs

# Okey we can see that the units are in meters and we have a `UTM projection  <https://en.wikipedia.org/wiki/Universal_Transverse_Mercator_coordinate_system>`_

# Let's plot the data and use column 'Level3' as our color
data.plot(column='Level3', linewidth=0.05)

# Use tight layout and remove empty whitespace around our map
plt.tight_layout()

# Let's see what kind of values we have in 'Level3Eng' column
list(data['Level3Eng'].unique())

# Select lakes (i.e. 'waterbodies' in the data) and make a proper copy out of our data
lakes = data.ix[data['Level3Eng'] == 'Water bodies'].copy()
lakes.head()


# Calculations in DataFrames
# --------------------------


# Calculate the area of lakes
lakes['area'] = lakes.area

# The values are in square meters so let's change those into square kilometers
lakes['area_km2'] = lakes['area'] / 1000000

# What is the mean size of our lakes?
l_mean_size = lakes['area_km2'].mean()
l_mean_size

# Okey so the size of our lakes seem to be approximately 1.58 square kilometers

# Classifying data
# ----------------

# Let's classify our data into small and large lakes where the dividing limit (threshold) that we use is the average size of the lake
# First we need to create a function for our classification task

def binaryClassifier(row, source_col, output_col, threshold):
    # If area of input geometry is lower that the threshold value
    if row[source_col] < threshold:
        # Update the output column with value 0
        row[output_col] = 0
    # If area of input geometry is higher than the threshold value update with value 1
    else:
        row[output_col] = 1
    # Return the updated row
    return row

# We can use our custom function by using a Pandas / Geopandas function called ``.apply()``
# Let's create an empty column for our classification
lakes['small_big'] = None

# Let's apply our function
lakes = lakes.apply(binaryClassifier, source_col='area_km2', output_col='small_big', threshold=l_mean_size, axis=1)

# Note: There is also a way of doing this without a function but it might be easier to understand how the function works and doing
# more complicated criteria should definately be done in a function as it is much more human readable
# Let's give a value 0 for small lakes and value 1 for big lakes by using an alternative technique
lakes['small_big_alt'] = None
lakes.loc[lakes['area_km2'] < l_mean_size, 'small_big_alt'] = 0
lakes.loc[lakes['area_km2'] >= l_mean_size, 'small_big_alt'] = 1

# Let's plot these lakes and see how they look like
lakes.plot(column='small_big', linewidth=0.05, cmap="seismic")
plt.tight_layout()

# Okey so it looks like they are correctly classified

# Simplifying geometries
# ----------------------

# What I want to do next is to only include the big lakes and simplify them slightly so that they are not as detailed

# Let's take only big lakes
big_lakes = lakes.ix[lakes['small_big'] == 1].copy()

# Let's see how they look
big_lakes.plot(linewidth=0.05, color='blue')
plt.tight_layout()

# The Polygons that are presented there are quite detailed, let's generalize them a bit

# Generalization can be done easily by using a Shapely function called ``.simplify()``. The ``tolerance`` parameter is adjusts how much
# geometries should be generalized. **The tolerance value is tied to the coordinate system of the geometries**.
# Thus, here the value we pass is 250 **meters**.
big_lakes['geom_gen'] = big_lakes.simplify(tolerance=250)

# Let's set the geometry to be our new column
big_lakes['geometry'] = big_lakes['geom_gen']

# Let's see how they look now
big_lakes.plot(linewidth=0.05, color='blue')
plt.tight_layout()

# Great! Now we can see that our Polygons have been simplified a bit that are good for visualizing larger areas

# Multicriteria data classification
# ---------------------------------

# Let's modify our binaryClassifier function a bit so that it classifies the data based on two columns
# Let's call it customClassifier2 as it takes into account two criteria

def customClassifier2(row, src_col1, src_col2, threshold1, threshold2, output_col):
    # 1. If the value in src_col1 is LOWER than the threshold1 value 
    # 2. AND the value in src_col2 is HIGHER than the threshold2 value, give value 1, otherwise give 0
    if row[src_col1] < threshold1 and row[src_col2] > threshold2:
        # Update the output column with value 0
        row[output_col] = 1
    # If area of input geometry is higher than the threshold value update with value 1
    else:
        row[output_col] = 0

    # Return the updated row
    return row

# Let's read our Travel Time data into memory now from JSON file that we prepared earlier

fp = r"/home/geo/TravelTimes_to_5975375_RailwayStation_Helsinki.geojson"

# Hide these
import os
fp = os.path.join(os.path.abspath('data'), "TravelTimes_to_5975375_RailwayStation_Helsinki.geojson")

acc = gpd.read_file(fp)

# Let's see what we have
acc.head(2)


# Okey we have plenty of different variables (see here describtion for all attributes) but what we are
# interested in are columns called pt_r_tt which is telling the time in minutes that it takes to reach city center
# from different parts of the city, and walk_d that tells the network distance by roads to reach city center
# from different parts of the city (almost equal to Euclidian distance). The NoData values are presented with value -1. Thus we need to remove those first
acc = acc.ix[acc['pt_r_tt'] >=0]


# Let's see what our CRS is
acc.crs

# Ah-ha! As you can see we don't have crs information was not included in the GeoJSON
# Thus, we need to define it
acc.crs = from_epsg(3067)


# Let's plot it and see how our data
import matplotlib.pyplot as plt

acc.plot(column="pt_r_tt", scheme="Fisher_Jenks", k=9, cmap="RdYlBu", linewidth=0)

# Okey so from this figure we can see that the travel times are lower in the south where 
# the city center is located but there are some areas of "good" accessibility also in some other areas
# (where the color is red)

# Let's also make a plot about walking distances
acc.plot(column="walk_d", scheme="Fisher_Jenks", k=9, cmap="RdYlBu", linewidth=0)

# Okey, from here we can see that the walking distances (along road network) reminds 
# more or less Euclidian distances

# Let's finally do our classification based on two criteria
# Let's find out grid cells where the travel time is lower or equal to 20 minutes but they are further away
# than 4 km (4000 meters)

# Let's create an empty column for our classification results called "Suitable_area"
acc["Suitable_area"] = None
acc = acc.apply(customClassifier2, src_col1='pt_r_tt', src_col2='walk_d', threshold1=20, threshold2=4000, output_col="Suitable_area", axis=1)

# Let's see what we got
acc.head()

# How many Polygons are suitable for us?
acc['Suitable_area'].value_counts()

# Okey so there seems to be nine suitable locations for us where we can try to find an appartment to buy
# Let's see where they are
acc.plot(column="Suitable_area", linewidth=0)

# A-haa, okey so we can see that suitable places for us using that criteria seems to be located in the 
# eastern part from city center. Actually, those locations are along the metro-line which makes them
# good locations in terms of travel time to city center as metro is a fast travel mode. 

# Task, try to change your classification criteria and see how your results change! What places would be
# suitable for you to buy an appartment in Helsinki region. You can also change the travel mode and see how 
# they change the results

 