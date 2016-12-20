# -*- coding: utf-8 -*-
"""
Prepare Helsinki municipality borders for the lesson

Created on Sun Nov 20 12:17:04 2016

@author: tenkahen
"""
import geopandas as gpd
from fiona.crs import from_epsg
# For this classification we will be using a different dataset that represents the accessibility 
# (measured as travel times / distances) in Helsinki Region to city center
fp = r"D:\KOODIT\Opetus\Automating-GIS-processes\AutoGIS-Sphinx\data\paituli_89425282\mml\hallintorajat_10k\2016\SuomenKuntajako_2016_10k.shp"

# Read the Shapefile
data = gpd.read_file(fp)

# Select Helsinki
hel = data.ix[data['NAMEFIN'] == 'Helsinki']

# Save to disk
outfp = r"D:\KOODIT\Opetus\Automating-GIS-processes\AutoGIS-Sphinx\data\Helsinki_borders.shp"
hel.to_file(outfp)

