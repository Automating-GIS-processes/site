# -*- coding: utf-8 -*-
"""
Preparation of AutoGIS Lesson 2. Using functions.

Created on Mon Nov  6 07:55:16 2017

@author: Henrikki Tenkanen
"""
import geopandas as gpd
import pandas as pd
from shapely.geometry import Point, LineString
from fiona.crs import from_epsg

fp = r"C:\HY-DATA\HENTENKA\KOODIT\Opetus\Automating-GIS-processes\2017\data\Europe_borders.shp"

data = gpd.read_file(fp)

# Project to metric using World Equidistant Cylindrical where distances are represented correctly from the central longitude and latitude (target point)
# Here we specify our target location to be the coordinates of Helsinki (lon=24.9417 and lat=60.1666)
hki_lon = 24.9417
hki_lat = 60.1666

# Next we need to specify that we want to center our projection to Helsinki. We need to specify the +lat_0 and +lon_0 parameters in Proj4 string to do this.
equidistant_proj = "+proj=eqc +lat_ts=60 +lat_0={0} +lon_0={1} +x_0=0 +y_0=0 +ellps=WGS84 +datum=WGS84 +units=m +no_defs".format(hki_lat, hki_lon)
data = data.to_crs(equidistant_proj)

# Let's plot our map and see how it looks like
#data.plot(facecolor='white')

# Okey, from here we can see that indeed our map is now centered to Helsinki as the 0-position in both x and y is on top of Helsinki.

# Let's start our analysis by creating a Point object from Helsinki and insert it into a GeoPandas GeoSeries.
hki = gpd.GeoSeries([Point(hki_lon, hki_lat)], crs=from_epsg(4326))
# Let's convert this point to the same projection as our Europe data is. 
hki = hki.to_crs(equidistant_proj)
print(hki)

# Aha! So the Point coordinates of Helsinki are 0. This confirms us that the center point of our projection is indeed Helsinki.

# Next we need to calculate the centroids for all the Polygons of the Europen countries. 
data['centroid'] = data.centroid

# Now we can calculate the distances between the centroids and Helsinki
def calculateDistance(row, dest_geom, src_col='geometry', target_col='distance'):
    """
    Calculates the distance between a single Shapely Point geometry and a GeoDataFrame with Point geometries.
    
    Parameters
    ----------
    dest_geom : shapely.Point
        A single Shapely Point geometry to which the distances will be calculated to.
    src_col : str
        A name of the column that has the Shapely Point objects from where the distances will be calculated from.
    target_col : str
        A name of the target column where the result will be stored.
    """
    # Calculate the distances
    dist = row[src_col].distance(dest_geom)
    # Tranform into kilometers
    dist_km = dist/1000
    # Assign the distance to the original data
    row[target_col] = dist_km
    return row


# Before using our function, we need to get the Shapely point geometry from the re-projected Helsinki center point. We can use the ``get()`` function to retrieve a value from specific index (here index 0).
hki_geom = hki.get(0)

# Now we have a nice function that we can use with ``apply()`` function.
data = data.apply(calculateDistance, dest_geom=hki_geom, src_col='centroid', target_col='dist_to_Hki', axis=1)



