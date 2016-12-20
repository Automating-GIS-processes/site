# -*- coding: utf-8 -*-
"""
Prepare travel time matrix layers for the lessons

Created on Sun Nov 20 12:17:04 2016

@author: tenkahen
"""
import gdal
import geopandas as gpd
from fiona.crs import from_epsg
import glob
import os
import pandas as pd

# For this classification we will be using a different dataset that represents the accessibility 
# (measured as travel times / distances) in Helsinki Region to city center
folder = r"D:\KOODIT\Opetus\Automating-GIS-processes\AutoGIS-Sphinx\data\Shopping_centers_accessibility_2013_2015"
fps = glob.glob(os.path.join(folder, "*Comparisons*.shp"))
ykr_fp = r"D:\KOODIT\Opetus\Automating-GIS-processes\AutoGIS-Sphinx\data\Shopping_centers_accessibility_2013_2015\YKD_ID_locations.txt"
ykr = pd.read_csv(ykr_fp, sep=';')

#fp = r"D:\KOODIT\Opetus\Automating-GIS-processes\AutoGIS-Sphinx\data\Shopping_centers_accessibility_2013_2015\TTM_Comparisons_5975375.shp"

for fp in fps:
    # Get Basename
    basename = os.path.basename(fp)
    
    # Parse the YKD_ID number
    ykr_id = int(basename.split('_')[-1][:-4])
    
    try:
        # Get the corresponding location name
        loc_name = ykr.loc[ykr['id'] == ykr_id, 'location'].values[0]
    except:
        loc_name = "NA"
        
    # Read the accessibility Shapefile
    acc = gpd.read_file(fp)
    
    # Select only data for year 2015
    cols = ['car_m_d_y', 'car_m_t_y', 'car_r_d', 'car_r_t', 'from_id', 'geometry', 'pt_m_d_y', 'pt_m_t_y',
           'pt_m_tt_y', 'pt_r_d', 'pt_r_t', 'pt_r_tt', 'to_id_y', 'walk_d_y', 'walk_t_y']
    acc = acc[cols]

    # Rename columns
    acc = acc.rename(columns={'car_m_d_y':'car_m_d', 'car_m_t_y': 'car_m_t', 'pt_m_d_y': 'pt_m_d', 'pt_m_t_y': 'pt_m_t', 'pt_m_tt_y': 'pt_m_tt', 'to_id_y': 'to_id', 'walk_d_y': 'walk_d', 'walk_t_y': 'walk_t'})
    
    # Reorder them
    order = ['from_id', 'to_id', 'walk_t','walk_d',
             'car_r_t', 'car_r_d', 'car_m_t', 'car_m_d',
             'pt_r_t', 'pt_r_tt', 'pt_r_d', 
             'pt_m_t', 'pt_m_tt', 'pt_m_d',
             'geometry']
         
    acc = acc[order]
    
    # Change the EPSG to 3067
    acc['geometry'] = acc['geometry'].to_crs(epsg=3067)
    acc.crs = from_epsg(3067)

    # Save to disk
    outfp = r"D:\KOODIT\Opetus\Automating-GIS-processes\AutoGIS-Sphinx\data\dataE4\TravelTimes_to_%s_%s.shp" % (ykr_id, loc_name)
    print(outfp)
    acc.to_file(outfp)
    
    # Save as csv file
    csvpath = outfp.replace(".shp", ".txt")
    
    # Drop geometry
    acc = acc.drop('geometry', axis=1)
    
    # Save
    acc.to_csv(csvpath, sep=';', index=False)
    

# GDAL EXE files are at C:\Program Files\Anaconda3\Library\bin

#import os
#import stat
#gdal_data = os.environ['GDAL_DATA']
#
#gcs_csv = os.path.join(gdal_data, 'gcs.csv')
